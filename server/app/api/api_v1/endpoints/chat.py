from fastapi import APIRouter, HTTPException # type: ignore
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def create_chat(chat_request: ChatRequest):
    try:
        return ChatResponse(
            message="Echo: " + chat_request.message,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))