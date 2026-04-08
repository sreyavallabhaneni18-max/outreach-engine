from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.message_status_service import update_message_status
from app.utils.mailgun_utils import normalize_mailgun_message_id

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/twilio/status")
async def twilio_status_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    form = await request.form()

    print("TWILIO WEBHOOK HIT")
    print(dict(form))

    message_sid = form.get("MessageSid")
    message_status = form.get("MessageStatus")
    error_code = form.get("ErrorCode")
    error_message = form.get("ErrorMessage")

    if not message_sid or not message_status:
        raise HTTPException(status_code=400, detail="Missing Twilio webhook fields")

    error = error_message or error_code

    update_message_status(
        db,
        provider="twilio",
        provider_message_id=message_sid,
        provider_status=message_status,
        error=error,
    )

    return {"ok": True}


@router.post("/mailgun/events")
async def mailgun_events_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    payload = await request.json()

    print("MAILGUN WEBHOOK HIT")
    print(payload)

    if "event-data" not in payload:
        return {"ok": True, "message": "Test webhook received"}

    event_data = payload.get("event-data", {})
    provider_status = event_data.get("event")

    provider_message_id = (
        event_data.get("message", {})
        .get("headers", {})
        .get("message-id")
    )
    provider_message_id = normalize_mailgun_message_id(provider_message_id)

    delivery_status = event_data.get("delivery-status", {})
    description = delivery_status.get("description")

    print("MAILGUN provider_status:", provider_status)
    print("MAILGUN provider_message_id:", provider_message_id)

    if not provider_status:
        raise HTTPException(status_code=400, detail="Missing Mailgun event")

    if not provider_message_id:
        return {"ok": True, "warning": "No provider_message_id found"}

    update_message_status(
        db,
        provider="mailgun",
        provider_message_id=provider_message_id,
        provider_status=provider_status,
        error=description,
    )

    return {"ok": True}