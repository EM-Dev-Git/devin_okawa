from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MeetingInfo(BaseModel):
    id: str
    subject: str
    start_time: datetime
    end_time: datetime
    organizer: str


class TranscriptSegment(BaseModel):
    speaker: str
    content: str
    timestamp: datetime


class MeetingTranscript(BaseModel):
    meeting_id: str
    meeting_subject: str
    segments: List[TranscriptSegment]
    duration_minutes: int


class GraphMinutesRequest(BaseModel):
    meeting_id: str
    title: Optional[str] = None


class GraphMinutesResponse(BaseModel):
    meeting_id: str
    meeting_subject: str
    transcript: str
    generated_minutes: str
    created_at: datetime
