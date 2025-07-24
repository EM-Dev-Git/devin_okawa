from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class GraphMeeting(BaseModel):
    id: str
    subject: str
    start_time: datetime
    end_time: datetime
    organizer: str
    participants: List[str]


class GraphTranscript(BaseModel):
    id: str
    meeting_id: str
    content: str
    created_datetime: datetime
    meeting_organizer: Optional[str] = None


class GraphTranscriptContent(BaseModel):
    transcript_id: str
    content: str
    speakers: List[str]
    duration_minutes: Optional[int] = None


class GraphMeetingResponse(BaseModel):
    meetings: List[GraphMeeting]
    total_count: int


class GraphTranscriptResponse(BaseModel):
    transcripts: List[GraphTranscript]
    total_count: int


class GraphMinutesRequest(BaseModel):
    meeting_id: str
    transcript_id: Optional[str] = None
    custom_prompt: Optional[str] = None


class GraphMinutesResponse(BaseModel):
    meeting_id: str
    transcript_id: str
    generated_minutes: str
    created_at: datetime
    processing_time_seconds: float
