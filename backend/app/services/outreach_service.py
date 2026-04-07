import asyncio
import logging
import os
import uuid

import requests
from sqlalchemy.orm import Session
from twilio.rest import Client

from app.channels.router import get_channel
from app.models.db_message import MessageRecord
from app.models.message import OutreachRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_message_status(sid: str) -> str:
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )

    message = client.messages(sid).fetch()
    return message.status


def check_mailgun_status(message_id: str) -> str:
    domain = os.getenv("MAILGUN_DOMAIN")
    api_key = os.getenv("MAILGUN_API_KEY")

    response = requests.get(
        f"https://api.mailgun.net/v3/{domain}/events",
        auth=("api", api_key),
        params={
            "message-id": message_id,
            "limit": 10
        },
        timeout=10,
    )

    if response.status_code != 200:
        return "unknown"

    items = response.json().get("items", [])
    event_names = [item.get("event") for item in items]

    if "delivered" in event_names:
        return "delivered"
    if "failed" in event_names or "rejected" in event_names:
        return "failed"
    if "accepted" in event_names:
        return "pending"

    return "pending"


def get_recipient_for_channel(channel: str, request: OutreachRequest) -> str:
    if channel == "email":
        if not request.email:
            raise ValueError("Email is required for email channel")
        return str(request.email)

    if channel in {"sms", "whatsapp"}:
        if not request.phone:
            raise ValueError(f"Phone is required for {channel} channel")
        return request.phone

    raise ValueError(f"Unsupported channel: {channel}")


def create_message_record(
    db: Session,
    request_id: str,
    channel: str,
    recipient: str,
    message_body: str,
) -> MessageRecord:
    record = MessageRecord(
        request_id=request_id,
        channel=channel,
        recipient=recipient,
        message_body=message_body,
        status="queued",
        retry_count=0,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_message_record(
    db: Session,
    record: MessageRecord,
    *,
    status: str = None,
    provider_message_id: str = None,
    retry_count: int = None,
    error: str = None,
) -> MessageRecord:
    if status is not None:
        record.status = status
    if provider_message_id is not None:
        record.provider_message_id = provider_message_id
    if retry_count is not None:
        record.retry_count = retry_count
    if error is not None:
        record.error = error

    db.add(record)
    db.commit()
    db.refresh(record)
    return record


async def send_single_channel(
    channel: str,
    request: OutreachRequest,
    request_id: str,
    db: Session,
):
    max_retries = 2
    handler = get_channel(channel)
    recipient = get_recipient_for_channel(channel, request)

    record = create_message_record(
        db=db,
        request_id=request_id,
        channel=channel,
        recipient=recipient,
        message_body=request.message,
    )

    for attempt in range(max_retries + 1):
        try:
            logger.info(f"Sending {channel} to {recipient} (attempt {attempt + 1})")
            update_message_record(db, record, retry_count=attempt)

            response = await handler.send(recipient, request.message)

            if response.get("status") == "failed":
                retryable = response.get("retryable", False)
                error = response.get("error", "Send failed")

                logger.error(
                    f"{channel} send failed (attempt {attempt + 1}) "
                    f"retryable={retryable}: {error}"
                )

                if not retryable:
                    update_message_record(db, record, status="failed", error=error)
                    return {
                        "channel": channel,
                        "status": "failed",
                        "error": error,
                        "message_id": record.id,
                    }

                if attempt == max_retries:
                    update_message_record(db, record, status="failed", error=error)
                    return {
                        "channel": channel,
                        "status": "failed",
                        "error": error,
                        "message_id": record.id,
                    }

                await asyncio.sleep(2 ** attempt)
                continue

            if channel == "email":
                provider_message_id = response.get("id")

                update_message_record(
                    db,
                    record,
                    provider_message_id=provider_message_id,
                    status="accepted",
                    error=None,
                )

                if not provider_message_id:
                    update_message_record(db, record, status="pending")
                    return {
                        "channel": channel,
                        "status": "pending",
                        "message_id": record.id,
                    }

                await asyncio.sleep(2)
                status = check_mailgun_status(provider_message_id)
                logger.info(f"{channel} polled status: {status}")

                if status == "delivered":
                    update_message_record(db, record, status="success", error=None)
                    return {
                        "channel": channel,
                        "status": "success",
                        "message_id": record.id,
                    }

                if status == "failed":
                    if attempt == max_retries:
                        update_message_record(
                            db,
                            record,
                            status="failed",
                            error="Mailgun delivery failed after retries",
                        )
                        return {
                            "channel": channel,
                            "status": "failed",
                            "error": "Mailgun delivery failed after retries",
                            "message_id": record.id,
                        }

                    logger.warning(f"{channel} delivery failed, retrying...")
                    await asyncio.sleep(2 ** attempt)
                    continue

                update_message_record(db, record, status="pending")
                return {
                    "channel": channel,
                    "status": "pending",
                    "message_id": record.id,
                }

            sid = response.get("sid")

            if not sid:
                update_message_record(
                    db,
                    record,
                    status="failed",
                    error="Provider did not return message SID",
                )
                return {
                    "channel": channel,
                    "status": "failed",
                    "error": "Provider did not return message SID",
                    "message_id": record.id,
                }

            update_message_record(
                db,
                record,
                provider_message_id=sid,
                status="accepted",
                error=None,
            )

            await asyncio.sleep(2)
            status = check_message_status(sid)
            logger.info(f"{channel} polled status: {status}")

            if status == "delivered":
                update_message_record(db, record, status="success", error=None)
                return {
                    "channel": channel,
                    "status": "success",
                    "message_id": record.id,
                }

            if status in ["failed", "undelivered"]:
                if attempt == max_retries:
                    update_message_record(
                        db,
                        record,
                        status="failed",
                        error=f"{channel} delivery failed after retries",
                    )
                    return {
                        "channel": channel,
                        "status": "failed",
                        "error": f"{channel} delivery failed after retries",
                        "message_id": record.id,
                    }

                logger.warning(f"{channel} delivery failed, retrying...")
                await asyncio.sleep(2 ** attempt)
                continue

            update_message_record(db, record, status="pending")
            return {
                "channel": channel,
                "status": "pending",
                "message_id": record.id,
            }

        except Exception as e:
            logger.error(f"Unexpected error sending {channel}: {str(e)}")

            if attempt == max_retries:
                update_message_record(
                    db,
                    record,
                    status="failed",
                    error=str(e),
                    retry_count=attempt,
                )
                return {
                    "channel": channel,
                    "status": "failed",
                    "error": str(e),
                    "message_id": record.id,
                }

            await asyncio.sleep(2 ** attempt)

    update_message_record(db, record, status="failed", error="Retries exhausted")
    return {
        "channel": channel,
        "status": "failed",
        "error": "Retries exhausted",
        "message_id": record.id,
    }


async def process_outreach(request: OutreachRequest, db: Session):
    request_id = str(uuid.uuid4())
    channels = []

    if request.email:
        channels.append("email")

    if request.phone:
        channels.append("sms")
        channels.append("whatsapp")

    if not channels:
        raise ValueError("At least one of email or phone must be provided")

    tasks = [
        send_single_channel(channel, request, request_id, db)
        for channel in channels
    ]

    results = await asyncio.gather(*tasks)

    return {
        "request_id": request_id,
        "results": results,
    }