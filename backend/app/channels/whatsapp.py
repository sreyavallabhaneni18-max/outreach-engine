import os
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
                to=f"whatsapp:{recipient}"
            )

            return {
                "sid": msg.sid,
                "status": msg.status
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }