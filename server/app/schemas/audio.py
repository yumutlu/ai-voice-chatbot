from pydantic import BaseModel # type: ignore
from typing import Optional

class AudioTranscriptionResponse(BaseModel):
    text: str
    confidence: Optional[float]

class TextToSpeechRequest(BaseModel):
    text: str
    voice: str = "alloy"

class ChatResponse(BaseModel):
    message: str
    audio_url: Optional[str]