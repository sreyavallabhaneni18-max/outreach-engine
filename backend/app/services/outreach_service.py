import asyncio
import logging
import uuid

from sqlalchemy.orm import Session

from app.channels.router import get_channel
from app.models.db_message import MessageRecord
from app.models.message import OutreachRequest
from app.utils.mailgun_utils import normalize_mailgun_message_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def get_provider_for_channel(channel: str) -> str:
    if channel == "email":
        return "mailgun"
    if channel in {"sms", "whatsapp"}:
        return "twilio"
    raise ValueError(f"Unsupported channel: {channel}")


def create_message_record(
    db: Session,
    request_id: str,
    channel: str,
    provider: str,
    recipient: str,
    message_body: str,
) -> MessageRecord:
    record = MessageRecord(
        request_id=request_id,
        channel=channel,
        provider=provider,
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
    status: str | None = None,
    provider_message_id: str | None = None,
    provider_status: str | None = None,
    retry_count: int | None = None,
    error: str | None = None,
) -> MessageRecord:
    if status is not None:
        record.status = status
    if provider_message_id is not None:
        record.provider_message_id = provider_message_id
    if provider_status is not None:
        record.provider_status = provider_status
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
    provider = get_provider_for_channel(channel)

    record = create_message_record(
        db=db,
        request_id=request_id,
        channel=channel,
        provider=provider,
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
                error_code = response.get("error_code")

                logger.error(
                    f"{channel} send failed (attempt {attempt + 1}) "
                    f"retryable={retryable}: "
                    f"{f'[{error_code}] ' if error_code else ''}{error}"
                )

                if not retryable or attempt == max_retries:
                    db_error = f"{error_code}: {error}" if error_code else error

                    update_message_record(
                        db,
                        record,
                        status="failed",
                        error=db_error,
                        retry_count=attempt,
                    )

                    return {
                        "channel": channel,
                        "status": "failed",
                        "error": error,
                        "error_code": error_code,
                        "message_id": record.id,
                    }

                await asyncio.sleep(2 ** attempt)
                continue

            provider_message_id = response.get("provider_message_id")
            provider_status = response.get("provider_status", "queued")

            if provider == "mailgun":
                provider_message_id = normalize_mailgun_message_id(provider_message_id)

            update_message_record(
                db,
                record,
                provider_message_id=provider_message_id,
                provider_status=provider_status,
                status="queued",
                error=None,
            )

            return {
                "channel": channel,
                "status": "queued",
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
                    "error_code": None,
                    "message_id": record.id,
                }

            await asyncio.sleep(2 ** attempt)

    update_message_record(
        db,
        record,
        status="failed",
        error="Retries exhausted",
        retry_count=max_retries,
    )
    return {
        "channel": channel,
        "status": "failed",
        "error": "Retries exhausted",
        "error_code": None,
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