from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Channel(str, Enum):
    email = "email"
    sms = "sms"
    whatsapp = "whatsapp"

class OutreachRequest(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    message: str
    channels: List[Channel]

class ChannelResult(BaseModel):
    channel: Channel
    status: str

class OutreachResponse(BaseModel):
    results: List[ChannelResult]