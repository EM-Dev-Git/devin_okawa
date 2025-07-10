import logging
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
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


@router.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "message": "Application is running"}
