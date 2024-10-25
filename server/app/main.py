from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from app.core.config import settings

app = FastAPI(
    title="AI Voice Chatbot API",
    description="Backend API for AI Voice Chatbot",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Voice Chatbot API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}