"""
Health check business logic module
Following FastAPI official documentation patterns for separating business logic
"""

from utils.logger import get_logger
from schemas.base import HealthResponse
import platform
import sys

logger = get_logger("fastapi_app.modules.health")


class HealthService:
    """Service class for health check operations"""
    
    @staticmethod
    def get_health_status() -> HealthResponse:
        """
        Get application health status
        
        Returns:
            HealthResponse: Health status information
        """
        logger.info("Performing health check")
        
        return HealthResponse(
            status="healthy",
            message=f"Application running on Python {sys.version_info.major}.{sys.version_info.minor} ({platform.system()})"
        )
