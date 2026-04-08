from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.db_message import MessageRecord
from app.models.message import Channel, OutreachRequest, OutreachResponse
from app.services.outreach_service import process_outreach, send_single_channel
import uuid

router = APIRouter()

#sends all channels 
@router.post("/outreach", response_model=OutreachResponse)
async def send_outreach(
    request: OutreachRequest,
    db: Session = Depends(get_db),
):
    try:
        return await process_outreach(request, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

#sens specific single channel 
@router.post("/outreach/{channel}", response_model=OutreachResponse)
async def send_single(
    channel: str,
    request: OutreachRequest,
    db: Session = Depends(get_db),
):
    if channel not in {"email", "sms", "whatsapp"}:
        raise HTTPException(status_code=400, detail="Unsupported channel")

    request_id = str(uuid.uuid4())

    try:
        result = await send_single_channel(channel, request, request_id, db)

        return {
            "request_id": request_id,
            "results": [result],
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/messages/{request_id}")
def get_messages_by_request_id(
    request_id: str,
    db: Session = Depends(get_db),
):
    records = (
        db.query(MessageRecord)
        .filter(MessageRecord.request_id == request_id)
        .all()
    )

    return {
        "request_id": request_id,
        "messages": [
            {
                "id": record.id,
                "channel": record.channel,
                "provider": record.provider,
                "recipient": record.recipient,
                "provider_message_id": record.provider_message_id,
                "provider_status": record.provider_status,
                "status": record.status,
                "retry_count": record.retry_count,
                "error": record.error,
                "sent_at": record.sent_at,
                "delivered_at": record.delivered_at,
                "failed_at": record.failed_at,
                "last_status_update_at": record.last_status_update_at,
                "created_at": record.created_at,
                "updated_at": record.updated_at,
            }
            for record in records
        ],
    }