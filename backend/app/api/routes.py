import asyncio
import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db import SessionLocal, get_db
from app.models.db_message import MessageRecord
from app.models.message import OutreachRequest, OutreachResponse
from app.services.outreach_service import process_outreach, send_single_channel
from app.services.status_stream_service import status_stream_service

router = APIRouter()


# sends all channels
@router.post("/outreach", response_model=OutreachResponse)
async def send_outreach(
    request: OutreachRequest,
    db: Session = Depends(get_db),
):
    try:
        return await process_outreach(request, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# sends specific single channel
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


@router.get("/outreach/{request_id}/stream")
async def stream_outreach_status(request_id: str):
    async def event_generator():
        queue = await status_stream_service.subscribe(request_id)

        db = SessionLocal()
        try:
            records = (
                db.query(MessageRecord)
                .filter(MessageRecord.request_id == request_id)
                .all()
            )

            initial_payload = {
                "request_id": request_id,
                "results": [
                    {
                        "channel": record.channel,
                        "status": record.status,
                        "error": record.error,
                        "message_id": record.id,
                        "provider": record.provider,
                        "provider_status": record.provider_status,
                    }
                    for record in records
                ],
            }

            yield f"data: {json.dumps(initial_payload, default=str)}\n\n"

            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data, default=str)}\n\n"

        except asyncio.CancelledError:
            pass
        finally:
            db.close()
            status_stream_service.unsubscribe(request_id, queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )