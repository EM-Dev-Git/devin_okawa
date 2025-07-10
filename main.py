from fastapi import FastAPI
from routers import root
from utils.logger import LoggerConfig, get_app_logger

LoggerConfig.setup_logging()
logger = get_app_logger()

app = FastAPI()

app.include_router(root.router)

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application starting up")

@app.on_event("shutdown") 
async def shutdown_event():
    logger.info("FastAPI application shutting down")
