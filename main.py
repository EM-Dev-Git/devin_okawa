from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import root, llm
from utils.logger import LoggerConfig, get_app_logger
from config import settings

LoggerConfig.setup_logging()
logger = get_app_logger()

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods.split(","),
    allow_headers=settings.cors_allow_headers.split(",") if settings.cors_allow_headers != "*" else ["*"],
)

app.include_router(root.router)
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
