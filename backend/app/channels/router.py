from app.channels.email import EmailChannel
from app.channels.sms import SMSChannel
from app.channels.whatsapp import WhatsAppChannel

def get_channel(channel_type: str):
    if channel_type == "email":
        return EmailChannel()
    elif channel_type == "sms":
        return SMSChannel()
    elif channel_type == "whatsapp":
        return WhatsAppChannel()
    else:
        raise ValueError(f"Unsupported channel: {channel_type}")