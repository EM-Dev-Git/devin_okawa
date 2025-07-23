from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ActionItem(BaseModel):
    task: str
    assignee: str
    deadline: str


class AgendaItem(BaseModel):
    title: str
    discussion: str
    decisions: List[str] = []
    action_items: List[ActionItem] = []


class MeetingHeader(BaseModel):
    title: str
    date: str
    location: str
    participants: List[str]
    facilitator: str


class TranscriptRequest(BaseModel):
    transcript: str
    header: MeetingHeader


class MinutesResponse(BaseModel):
    id: int
    title: str
    generated_minutes: str
    created_at: datetime

    class Config:
        from_attributes = True


class MinutesCreate(BaseModel):
    title: str
    transcript: str
    generated_minutes: str
