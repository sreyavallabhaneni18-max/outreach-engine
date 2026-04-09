import os
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from app.channels.base import BaseChannel


class WhatsAppChannel(BaseChannel):
    async def send(self, recipient: str, message: str):
        try:
            client = Client(
                os.getenv("TWILIO_ACCOUNT_SID"),
                os.getenv("TWILIO_AUTH_TOKEN")
            )

            msg = client.messages.create(
                body=message,
                from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
                to=f"whatsapp:{recipient}",
                status_callback=os.getenv("TWILIO_STATUS_CALLBACK_URL"),
            )

            return {
                "status": "queued",
                "provider": "twilio",
                "provider_message_id": msg.sid,
                "provider_status": msg.status,
                "retryable": False,
            }

        except TwilioRestException as e:
            retryable = getattr(e, "status", None) is not None and e.status >= 500

            return {
                "status": "failed",
                "provider": "twilio",
                "error": e.msg or str(e),
                "error_code": str(e.code) if getattr(e, "code", None) else None,
                "retryable": retryable,
            }

        except Exception as e:
            return {
                "status": "failed",
                "provider": "twilio",
                "error": str(e),
                "error_code": None,
                "retryable": True,
            }