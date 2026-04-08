# Backend README

## Overview

The backend is a FastAPI service for the outreach engine. It accepts outreach requests and sends messages through:
- Email via Mailgun
- SMS via Twilio
- WhatsApp via Twilio

It also stores message send attempts and status updates in a local SQLite database, and exposes webhook endpoints for provider delivery status updates.

## What the backend does

- Serves API endpoints for creating outreach requests (`/outreach` and `/outreach/{channel}`)
- Writes message records to a SQLite database (`outreach.db`)
- Sends email, SMS, and WhatsApp messages using provider-specific channel classes
- Receives Twilio and Mailgun webhook callbacks to update message delivery status
- Uses Pydantic models for request validation and response formatting

## Required libraries

The backend depends on the following Python packages:

- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `pydantic`
- `python-dotenv`
- `requests`
- `twilio`

Additional package dependencies may be pulled in by FastAPI, including `email-validator` and related packages.

## Setup instructions

1. Open a terminal in `backend/`
2. Create a virtual environment if you do not already have one:

```bash
python3 -m venv venv
```

3. Activate the virtual environment:

```bash
source venv/bin/activate
```

4. Install the required packages:

```bash
pip install fastapi uvicorn sqlalchemy python-dotenv requests twilio
```

5. Ensure the backend root contains a `.env` file with the required environment variables.

6. Run the backend:

```bash
uvicorn app.main:app --reload 
```

7. Verify the server is running by visiting:

```text
http://localhost:8000/
```
```
swagger Url 
http://localhost:8000/docs#/
```

## Environment variables

The backend loads environment variables from `backend/.env`. The following variables are used by the current implementation:

- `MAILGUN_DOMAIN`
- `MAILGUN_API_KEY`
- `MAILGUN_FROM_EMAIL`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `TWILIO_WHATSAPP_NUMBER`
- `TWILIO_STATUS_CALLBACK_URL`

## Database

- The backend uses SQLite and creates `backend/outreach.db` automatically when it starts.
- The SQLAlchemy models are defined in `backend/app/models/db_message.py`.
- The database engine is configured in `backend/app/db.py`.

## Key files and architecture

- `backend/app/main.py` — FastAPI app entrypoint and DB initialization
- `backend/app/api/routes.py` — outreach API endpoints
- `backend/app/api/webhooks.py` — webhook endpoints for Twilio and Mailgun
- `backend/app/channels/email.py` — Mailgun email send implementation
- `backend/app/channels/sms.py` — Twilio SMS send implementation
- `backend/app/channels/whatsapp.py` — Twilio WhatsApp send implementation
- `backend/app/services/outreach_service.py` — orchestration of outreach workflows
- `backend/app/models/message.py` — Pydantic request/response models
- `backend/app/models/db_message.py` — SQLAlchemy message record model

## Notes

- Do not commit credentials or secrets from `.env` to source control.
- If you test Twilio webhooks locally, use a tunnel such as `ngrok` and point `TWILIO_STATUS_CALLBACK_URL` to the public URL.
- Email and provider credentials must be valid for outgoing requests to succeed.
- The backend currently supports the three channels: `email`, `sms`, and `whatsapp`.
