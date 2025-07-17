from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from .routers.minutes import router as minutes_router
from .routers.auth import router as auth_router, login_router
from .modules.logger_config import setup_logger
from .middleware.auth import SessionAuthenticationMiddleware
from .config import settings
import logging

setup_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Meeting Minutes Generator",
    description="Azure OpenAI powered meeting minutes generation system with session-based authentication",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionAuthenticationMiddleware)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret_key,
    max_age=settings.session_expire_hours * 3600
)

app.include_router(auth_router)
app.include_router(login_router)
app.include_router(minutes_router)

@app.get("/")
async def root():
    return {"message": "Meeting Minutes Generator API", "status": "running", "auth": "required"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "meeting-minutes-generator"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Meeting Minutes Generator API server with application-wide authentication")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
