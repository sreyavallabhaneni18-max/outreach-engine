from fastapi import APIRouter
from app.models.message import OutreachRequest, OutreachResponse
from app.services.outreach_service import process_outreach

router = APIRouter()

@router.post("/outreach", response_model=OutreachResponse)
async def send_outreach(request: OutreachRequest):
    return await process_outreach(request)