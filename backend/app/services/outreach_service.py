import asyncio
import logging
import os
from twilio.rest import Client

from app.models.message import OutreachRequest
from app.channels.router import get_channel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_message_status(sid):
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )

    message = client.messages(sid).fetch()
    return message.status


async def send_single_channel(channel, request):
    max_retries = 2

    for attempt in range(max_retries + 1):
        try:
            handler = get_channel(channel)
            recipient = request.email if channel == "email" else request.phone

            logger.info(f"Sending {channel} to {recipient} (attempt {attempt + 1})")

            response = await handler.send(recipient, request.message)

            # if send itself failed
            if response.get("status") == "failed":
                raise Exception(response.get("error", "Send failed"))

            sid = response["sid"]

            # wait before polling
            await asyncio.sleep(2)

            status = check_message_status(sid)

            logger.info(f"{channel} polled status: {status}")

            # success case
            if status == "delivered":
                return {
                    "channel": channel,
                    "status": "success"
                }

            # retry only on real failure
            if status in ["failed", "undelivered"]:
                logger.warning(f"{channel} failed delivery, retrying...")

            else:
                # still pending → don't retry
                return {
                    "channel": channel,
                    "status": "pending"
                }

        except Exception as e:
            logger.error(f"Error sending {channel}: {str(e)}")

            if attempt == max_retries:
                return {
                    "channel": channel,
                    "status": "failed",
                    "error": str(e)
                }

        # exponential backoff
        await asyncio.sleep(2 ** attempt)

    return {
        "channel": channel,
        "status": "failed"
    }


async def process_outreach(request: OutreachRequest):
    tasks = [
        send_single_channel(channel, request)
        for channel in request.channels
    ]

    results = await asyncio.gather(*tasks)

    return {"results": results}