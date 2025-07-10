import logging
from fastapi import FastAPI
from routers import root

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(root.router)

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application starting up")

@app.on_event("shutdown") 
async def shutdown_event():
    logger.info("FastAPI application shutting down")
