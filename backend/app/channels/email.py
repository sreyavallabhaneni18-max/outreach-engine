from app.channels.base import BaseChannel

class EmailChannel(BaseChannel):

    async def send(self, recipient: str, message: str):
        print(f"Sending EMAIL to {recipient}: {message}")
        return "sent"