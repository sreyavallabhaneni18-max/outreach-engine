import json
import os
import requests

from app.channels.base import BaseChannel


class EmailChannel(BaseChannel):
    async def send(self, recipient: str, message: str):
        domain = os.getenv("MAILGUN_DOMAIN")
        api_key = os.getenv("MAILGUN_API_KEY")
        from_email = os.getenv("MAILGUN_FROM_EMAIL")

        try:
            response = requests.post(
                f"https://api.mailgun.net/v3/{domain}/messages",
                auth=("api", api_key),
                data={
                    "from": from_email,
                    "to": recipient,
                    "subject": "TalentFlow Outreach",
                    "text": message,
                },
            )

            if response.status_code >= 400:
                error_message = "Email send failed"

                try:
                    error_json = response.json()
                    error_message = error_json.get("message", error_message)
                except Exception:
                    error_message = response.text or error_message

                retryable = response.status_code >= 500

                return {
                    "status": "failed",
                    "provider": "mailgun",
                    "error": error_message,
                    "retryable": retryable,
                }

            data = response.json()

            return {
                "status": "queued",
                "provider": "mailgun",
                "provider_message_id": data.get("id"),
                "provider_status": "queued",
                "retryable": False,
            }

        except requests.RequestException as e:
            return {
                "status": "failed",
                "provider": "mailgun",
                "error": str(e),
                "retryable": True,
            }