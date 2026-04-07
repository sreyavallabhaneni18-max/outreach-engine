from app.channels.base import BaseChannel

class SMSChannel(BaseChannel):

    async def send(self, recipient: str, message: str):
        print(f"Sending SMS to {recipient}: {message}")
        return "sent"