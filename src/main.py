from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.minutes import router as minutes_router
from .modules.logger_config import setup_logger
import logging

setup_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Meeting Minutes Generator",
    description="Azure OpenAI powered meeting minutes generation system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(minutes_router)

@app.get("/")
async def root():
    return {"message": "Meeting Minutes Generator API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "meeting-minutes-generator"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Meeting Minutes Generator API server")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
