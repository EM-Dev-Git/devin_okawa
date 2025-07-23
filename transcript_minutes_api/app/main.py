from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .config import settings
from .database import engine, Base
from .modules.logger import LoggerConfig
from .routers import auth, users, minutes, graph

@asynccontextmanager
async def lifespan(app: FastAPI):
    LoggerConfig.setup_logging()
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="議事録作成API",
    description="トランスクリプトから議事録を自動生成するAPI",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(minutes.router)
app.include_router(graph.router)

@app.get("/")
async def root():
    return {"message": "議事録作成API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
