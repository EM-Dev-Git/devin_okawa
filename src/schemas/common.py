from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BaseResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None
    timestamp: datetime = datetime.now()

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
    timestamp: datetime = datetime.now()
