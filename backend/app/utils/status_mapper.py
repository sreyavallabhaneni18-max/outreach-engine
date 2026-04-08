def map_twilio_status(provider_status: str) -> str:
    if not provider_status:
        return "queued"

    status = provider_status.lower()

    if status in {"queued", "accepted", "scheduled", "sending"}:
        return "queued"
    if status == "sent":
        return "sent"
    if status == "delivered":
        return "delivered"
    if status in {"failed", "undelivered", "canceled"}:
        return "failed"

    return "queued"


def map_mailgun_status(provider_status: str) -> str:
    if not provider_status:
        return "queued"

    status = provider_status.lower()

    if status in {"accepted", "queued"}:
        return "queued"
    if status in {"sent"}:
        return "sent"
    if status in {"delivered"}:
        return "delivered"
    if status in {"failed", "rejected", "complained", "unsubscribed"}:
        return "failed"

    return "queued"