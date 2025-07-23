from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, users, minutes
from .modules.logger import setup_logger
from .config import settings

setup_logger()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Transcript Minutes API",
    description="トランスクリプトから議事録を自動生成するAPI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(minutes.router)


@app.get("/")
async def root():
    return {
        "message": "Transcript Minutes API",
        "version": "1.0.0",
        "description": "トランスクリプトから議事録を自動生成するAPI"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "transcript-minutes-api"}
