from app.models.message import OutreachRequest
from app.channels.router import get_channel

async def process_outreach(request: OutreachRequest):
    results = []

    for channel in request.channels:
        try:
            handler = get_channel(channel)

            recipient = request.email if channel == "email" else request.phone

            status = await handler.send(recipient, request.message)

            results.append({
                "channel": channel,
                "status": status
            })

        except Exception as e:
            results.append({
                "channel": channel,
                "status": "failed",
                "error": str(e)
            })

    return {"results": results}