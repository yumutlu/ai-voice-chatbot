from openai import OpenAI # type: ignore
from fastapi import HTTPException # type: ignore
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def speech_to_text(self, audio_file) -> str:
        try:
            transcript = await self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            return transcript
        except Exception as e:
            logger.error(f"Error in speech to text conversion: {str(e)}")
            raise HTTPException(status_code=500, detail="Speech to text conversion failed")

    async def generate_chat_response(self, message: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": message}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in generating chat response: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate response")

    async def text_to_speech(self, text: str):
        try:
            response = await self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            return response
        except Exception as e:
            logger.error(f"Error in text to speech conversion: {str(e)}")
            raise HTTPException(status_code=500, detail="Text to speech conversion failed")