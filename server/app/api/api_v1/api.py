from fastapi import APIRouter # type: ignore
from app.api.api_v1.endpoints import chat, audio

router = APIRouter()

router.include_router(chat.router, prefix="/chat", tags=["chat"])
router.include_router(audio.router, prefix="/audio", tags=["audio"])