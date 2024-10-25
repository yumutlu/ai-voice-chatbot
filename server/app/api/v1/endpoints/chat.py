from fastapi import APIRouter, HTTPException # type: ignore
from app.services.openai_service import OpenAIService
from app.schemas.chat import ChatRequest, ChatResponse
from typing import Optional

router = APIRouter()
openai_service = OpenAIService()

@router.post("/", response_model=ChatResponse)
async def process_chat(chat_request: ChatRequest):
    try:
        # Generate text response
        text_response = await openai_service.generate_chat_response(chat_request.message)
        
        # Generate audio response if requested
        audio_url = None
        if chat_request.generate_audio:
            audio_response = await openai_service.text_to_speech(text_response)
            # Handle audio response storage/streaming
            audio_url = "/audio/response.mp3"  # Placeholder URL
            
        return ChatResponse(
            message=text_response,
            audio_url=audio_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))