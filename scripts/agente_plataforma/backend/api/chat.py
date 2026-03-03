from fastapi import APIRouter
from pydantic import BaseModel
from services.adk_service import run_orchestrator

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/")
async def chat(request: ChatRequest):
    response = await run_orchestrator(
        session_id=request.session_id,
        message=request.message
    )

    return response
