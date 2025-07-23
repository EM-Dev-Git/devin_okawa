from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import engine, Base
from .routers import auth, users, minutes, graph
from .modules.logger import LoggerConfig, get_logger
from .config import settings

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    LoggerConfig.setup_logging()
    logger.info("アプリケーション開始")
    
    Base.metadata.create_all(bind=engine)
    logger.info("データベーステーブル作成完了")
    
    yield
    
    logger.info("アプリケーション終了")


app = FastAPI(
    title="Meeting Minutes API v3",
    description="トランスクリプトから議事録を生成するAPI（Microsoft Graph SDK統合版）",
    version="3.0.0",
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
app.include_router(graph.router)


@app.get("/")
async def root():
    logger.info("ルートエンドポイントアクセス")
    return {
        "message": "Meeting Minutes API v3",
        "description": "トランスクリプトから議事録を生成するAPI（Microsoft Graph SDK統合版）",
        "version": "3.0.0",
        "endpoints": {
            "auth": "/auth",
            "users": "/users", 
            "minutes": "/minutes",
            "graph": "/graph",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    logger.info("ヘルスチェックアクセス")
    return {"status": "healthy", "version": "3.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
