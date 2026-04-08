import os
import requests

from app.channels.base import BaseChannel
from app.utils.mailgun_utils import normalize_mailgun_message_id


class EmailChannel(BaseChannel):
    async def send(self, recipient: str, message: str):
        try:
            domain = os.getenv("MAILGUN_DOMAIN")
            api_key = os.getenv("MAILGUN_API_KEY")
            from_email = os.getenv("MAILGUN_FROM_EMAIL")

            response = requests.post(
                f"https://api.mailgun.net/v3/{domain}/messages",
                auth=("api", api_key),
                data={
                    "from": f"Mailgun Sandbox <{from_email}>",
                    "to": recipient,
                    "subject": "Outreach Message",
                    "text": message,
                },
                timeout=10,
            )

            if response.status_code == 200:
                body = response.json()
                provider_message_id = normalize_mailgun_message_id(body.get("id"))

                return {
                    "status": "queued",
                    "provider": "mailgun",
                    "provider_message_id": provider_message_id,
                    "retryable": False,
                }

            if response.status_code in [400, 401, 403, 404]:
                return {
                    "status": "failed",
                    "provider": "mailgun",
                    "error": response.text,
                    "retryable": False,
                }

            if response.status_code >= 500:
                return {
                    "status": "failed",
                    "provider": "mailgun",
                    "error": response.text,
                    "retryable": True,
                }

            return {
                "status": "failed",
                "provider": "mailgun",
                "error": response.text,
                "retryable": False,
            }

        except requests.Timeout:
            return {
                "status": "failed",
                "provider": "mailgun",
                "error": "Mailgun request timed out",
                "retryable": True,
            }

        except requests.RequestException as e:
            return {
                "status": "failed",
                "provider": "mailgun",
                "error": str(e),
                "retryable": True,
            }

        except Exception as e:
            return {
                "status": "failed",
                "provider": "mailgun",
                "error": str(e),
                "retryable": False,
            }