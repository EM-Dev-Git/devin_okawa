from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import auth, minutes
from src.config import settings
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI議事録生成アプリケーション with OAuth2認証",
    debug=settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(minutes.router)

@app.get("/")
async def root():
    return {
        "message": "FastAPI Meeting Minutes Generator with OAuth2 Authentication",
        "status": "running",
        "version": settings.app_version
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "meeting-minutes-generator",
        "version": settings.app_version
    }

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info("Application startup completed")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown completed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
