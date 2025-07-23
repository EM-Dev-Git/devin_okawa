from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class MeetingHeader(BaseModel):
    title: str
    date: date
    location: Optional[str] = None
    participants: List[str]
    absent_members: Optional[List[str]] = []
    facilitator: Optional[str] = None

class MinutesRequest(BaseModel):
    transcript: str
    header: MeetingHeader

class MinutesResponse(BaseModel):
    id: int
    title: str
    date: date
    location: Optional[str]
    participants: str
    absent_members: Optional[str]
    facilitator: Optional[str]
    transcript: str
    formatted_minutes: str
    created_at: datetime

    class Config:
        from_attributes = True

class MinutesListResponse(BaseModel):
    id: int
    title: str
    date: date
    created_at: datetime

    class Config:
        from_attributes = True
