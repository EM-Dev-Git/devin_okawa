"""
Base schema models for the FastAPI application
Following FastAPI official documentation patterns for Pydantic models
"""

from pydantic import BaseModel
from typing import Optional


class BaseResponse(BaseModel):
    """Base response model for API endpoints"""
    success: bool = True
    message: str = "Operation completed successfully"


class HealthResponse(BaseResponse):
    """Health check response model"""
    status: str
