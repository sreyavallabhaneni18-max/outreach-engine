from datetime import datetime
from sqlalchemy.orm import Session

from app.models.db_message import MessageRecord
from app.utils.mailgun_utils import normalize_mailgun_message_id
from app.utils.status_mapper import map_mailgun_status, map_twilio_status


def update_message_status(
    db: Session,
    *,
    provider: str,
    provider_message_id: str,
    provider_status: str,
    error: str | None = None,
) -> MessageRecord | None:
    if provider == "mailgun":
        provider_message_id = normalize_mailgun_message_id(provider_message_id)

    record = (
        db.query(MessageRecord)
        .filter(
            MessageRecord.provider == provider,
            MessageRecord.provider_message_id == provider_message_id,
        )
        .first()
    )

    if not record:
        print(
            f"No message record found for provider={provider}, "
            f"provider_message_id={provider_message_id}"
        )
        return None

    if provider == "twilio":
        normalized_status = map_twilio_status(provider_status)
    elif provider == "mailgun":
        normalized_status = map_mailgun_status(provider_status)
    else:
        normalized_status = "queued"

    now = datetime.utcnow()

    record.provider_status = provider_status
    record.status = normalized_status
    record.error = error
    record.last_status_update_at = now

    if normalized_status == "sent" and record.sent_at is None:
        record.sent_at = now
    elif normalized_status == "delivered" and record.delivered_at is None:
        record.delivered_at = now
    elif normalized_status == "failed" and record.failed_at is None:
        record.failed_at = now

    db.add(record)
    db.commit()
    db.refresh(record)
    return record