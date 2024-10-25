from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks # type: ignore
from app.services.openai_service import OpenAIService
from app.schemas.audio import AudioTranscriptionResponse, TextToSpeechRequest
import tempfile
import os

router = APIRouter()
openai_service = OpenAIService()

@router.post("/transcribe", response_model=AudioTranscriptionResponse)
async def transcribe_audio(audio: UploadFile = File(...)):
    if not audio.filename.endswith(('.mp3', '.wav', '.m4a')):
        raise HTTPException(status_code=400, detail="Unsupported audio format")

    try:
        transcript = await openai_service.speech_to_text(audio.file)
        return AudioTranscriptionResponse(text=transcript, confidence=0.9)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/synthesize")
async def synthesize_speech(request: TextToSpeechRequest):
    try:
        audio_response = await openai_service.text_to_speech(request.text)
        
        # Save the audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(audio_response.content)
            return {"audio_url": f"/audio/stream/{os.path.basename(temp_file.name)}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))