from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MinutesBase(BaseModel):
    title: str
    transcript: str


class MinutesCreate(MinutesBase):
    pass


class MinutesUpdate(BaseModel):
    title: Optional[str] = None
    transcript: Optional[str] = None


class Minutes(MinutesBase):
    id: int
    generated_minutes: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MinutesResponse(BaseModel):
    id: int
    title: str
    generated_minutes: str
    created_at: datetime
    summary: Optional[str] = None

    class Config:
        from_attributes = True
