from fastapi import APIRouter, HTTPException
from utils.logger import get_router_logger
from schemas.base import BaseResponse, HealthResponse
from modules.health import HealthService

logger = get_router_logger("root")
router = APIRouter()
health_service = HealthService()


@router.get("/", response_model=BaseResponse)
async def root():
    try:
        logger.info("Root endpoint accessed")
        response = BaseResponse(message="Hello World")
        logger.info(f"Successfully returning response: {response.dict()}")
        return response
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health", response_model=HealthResponse)
async def health_check():
    try:
        logger.info("Health check endpoint accessed")
        response = health_service.get_health_status()
        logger.info(f"Health check completed: {response.status}")
        return response
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")
