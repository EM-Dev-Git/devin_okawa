from fastapi import FastAPI
from .routers import minutes
from .modules.logger import setup_logger
import logging

setup_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="議事録生成API",
    description="Azure OpenAIを使用してトランスクリプトから議事録を生成するAPI",
    version="1.0.0"
)

app.include_router(minutes.router)

@app.get("/")
async def root():
    """ルートエンドポイント"""
    logger.info("ルートエンドポイントアクセス")
    return {"message": "議事録生成API", "version": "1.0.0"}

@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    logger.info("議事録生成API 起動完了")

@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時の処理"""
    logger.info("議事録生成API 終了")
