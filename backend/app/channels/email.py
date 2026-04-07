import os
import requests
from app.channels.base import BaseChannel


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

            print("MAILGUN STATUS:", response.status_code)
            print("MAILGUN RESPONSE:", response.text)

            if response.status_code == 200:
                body = response.json()
                return {
                    "status": "queued",
                    "id": body.get("id"),
                    "retryable": False,
                }

            # Permanent client-side failures: do not retry
            if response.status_code in [400, 401, 403, 404]:
                return {
                    "status": "failed",
                    "error": response.text,
                    "retryable": False,
                }

            # Provider-side / transient failures: retry
            if response.status_code >= 500:
                return {
                    "status": "failed",
                    "error": response.text,
                    "retryable": True,
                }

            return {
                "status": "failed",
                "error": response.text,
                "retryable": False,
            }

        except requests.Timeout:
            return {
                "status": "failed",
                "error": "Mailgun request timed out",
                "retryable": True,
            }

        except requests.RequestException as e:
            return {
                "status": "failed",
                "error": str(e),
                "retryable": True,
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "retryable": False,
            }