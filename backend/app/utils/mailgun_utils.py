def normalize_mailgun_message_id(value: str | None) -> str | None:
    if not value:
        return value
    return value.strip().strip("<>").strip()