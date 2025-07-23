from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import engine
from .models import Base
from .routers import auth, users, minutes
from .modules.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("アプリケーション開始")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("アプリケーション終了")


app = FastAPI(
    title="Meeting Minutes API",
    description="トランスクリプトから議事録を自動生成するAPI",
    version="1.0.0",
    lifespan=lifespan
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
        "message": "Meeting Minutes API",
        "version": "1.0.0",
        "description": "トランスクリプトから議事録を自動生成するAPI"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
