from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from app.core.config import settings
from app.middleware.rate_limit import RateLimiter
from app.api.v1.api import router as api_v1_router # type: ignore

app = FastAPI(title=settings.PROJECT_NAME)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
rate_limiter = RateLimiter(requests_per_minute=60)
app.middleware("http")(rate_limiter)

# Include API router
app.include_router(api_v1_router, prefix=settings.API_V1_STR)