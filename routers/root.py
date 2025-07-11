from fastapi import APIRouter, HTTPException
from utils.logger import get_router_logger

logger = get_router_logger("root")
router = APIRouter()


@router.get("/")
async def root():
    try:
        logger.info("Root endpoint accessed")
        response = {"message": "Hello World"}
        logger.info(f"Successfully returning response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
