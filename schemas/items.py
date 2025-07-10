"""
Item-related schema models
Example schemas following FastAPI documentation patterns
"""

from pydantic import BaseModel
from typing import Optional, List


class ItemBase(BaseModel):
    """Base item model"""
    name: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """Schema for creating new items"""
    pass


class ItemResponse(ItemBase):
    """Schema for item responses"""
    id: int
    
    class Config:
        from_attributes = True
