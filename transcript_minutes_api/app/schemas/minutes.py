from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MinutesCreate(BaseModel):
    title: str
    transcript: str


class MinutesUpdate(BaseModel):
    title: Optional[str] = None
    transcript: Optional[str] = None


class MinutesResponse(BaseModel):
    id: int
    user_id: int
    title: str
    transcript: str
    generated_minutes: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MinutesListResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True
