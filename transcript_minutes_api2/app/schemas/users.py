from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    user_id: str
    email: Optional[str] = None


class UserCreate(BaseModel):
    user_id: str
    password: str
    email: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
