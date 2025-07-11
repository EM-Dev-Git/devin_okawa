from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import llm
from utils.logger import LoggerConfig, get_app_logger
from config import settings

LoggerConfig.setup_logging()
logger = get_app_logger()

app = FastAPI(
    title=settings.app_name,  # アプリケーション名
    description=settings.app_description,  # アプリケーション説明
    version=settings.app_version,  # バージョン番号
    debug=settings.debug  # デバッグモードフラグ
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # 許可するオリジンのリスト
    allow_credentials=settings.cors_allow_credentials,  # 認証情報送信許可フラグ
    allow_methods=settings.cors_allow_methods.split(","),  # 許可するHTTPメソッド
    allow_headers=settings.cors_allow_headers.split(",") if settings.cors_allow_headers != "*" else ["*"],  # 許可するHTTPヘッダー
)

app.include_router(llm.router)

@app.on_event("startup")
async def startup_event():
    logger.info(f"FastAPI application '{settings.app_name}' starting up")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Server will run on {settings.host}:{settings.port}")

@app.on_event("shutdown") 
async def shutdown_event():
    logger.info(f"FastAPI application '{settings.app_name}' shutting down")
