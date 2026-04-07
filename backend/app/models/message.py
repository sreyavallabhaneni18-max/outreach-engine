from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class Channel(str, Enum):
    email = "email"
    sms = "sms"
    whatsapp = "whatsapp"


class OutreachRequest(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    message: str


class ChannelResult(BaseModel):
    channel: Channel
    status: str
    error: Optional[str] = None
    message_id: Optional[int] = None


class OutreachResponse(BaseModel):
    request_id: str
    results: List[ChannelResult]