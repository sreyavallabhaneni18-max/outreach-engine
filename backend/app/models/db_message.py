from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db import Base


class MessageRecord(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, index=True, nullable=False)
    channel = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    message_body = Column(Text, nullable=False)

    provider_message_id = Column(String, nullable=True, index=True)

    status = Column(String, nullable=False, default="queued")
    retry_count = Column(Integer, nullable=False, default=0)
    error = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )