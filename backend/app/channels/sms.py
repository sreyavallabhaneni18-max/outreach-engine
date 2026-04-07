import os
from twilio.rest import Client
from app.channels.base import BaseChannel


class SMSChannel(BaseChannel):

    async def send(self, recipient: str, message: str):
        try:
            client = Client(
                os.getenv("TWILIO_ACCOUNT_SID"),
                os.getenv("TWILIO_AUTH_TOKEN")
            )

            msg = client.messages.create(
                body=message,
                from_=os.getenv("TWILIO_PHONE_NUMBER"),
                to=recipient
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