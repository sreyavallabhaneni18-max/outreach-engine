from app.channels.base import BaseChannel

class WhatsAppChannel(BaseChannel):

    async def send(self, recipient: str, message: str):
        print(f"Sending WhatsApp to {recipient}: {message}")
        return "sent"