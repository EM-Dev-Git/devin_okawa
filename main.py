from fastapi import FastAPI
from routers import root, items
from utils.logger import LoggerConfig, get_app_logger

LoggerConfig.setup_logging()
logger = get_app_logger()

app = FastAPI(
    title="FastAPI Basic Application",
    description="A basic FastAPI application with modular structure",
    version="1.0.0"
)

app.include_router(root.router)
app.include_router(items.router)

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application starting up")

@app.on_event("shutdown") 
async def shutdown_event():
    logger.info("FastAPI application shutting down")
