from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime


class MeetingHeader(BaseModel):
    title: str
    date: date
    location: str
    participants: List[str]
    facilitator: str


class ActionItem(BaseModel):
    task: str
    assignee: str
    deadline: str


class AgendaItem(BaseModel):
    title: str
    discussion: str
    decisions: List[str]
    action_items: List[ActionItem]


class ProcessedTranscript(BaseModel):
    summary: str
    agenda_items: List[AgendaItem]
    next_meeting: str


class MinutesGenerateRequest(BaseModel):
    transcript: str
    header: MeetingHeader


class MinutesResponse(BaseModel):
    id: int
    title: str
    date: date
    location: str
    participants: str
    facilitator: str
    formatted_minutes: str
    created_at: datetime

    class Config:
        from_attributes = True


class MinutesListResponse(BaseModel):
    minutes: List[MinutesResponse]
    total_count: int
