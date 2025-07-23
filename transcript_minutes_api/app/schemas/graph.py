from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MeetingInfo(BaseModel):
    id: str
    subject: str
    organizer: str
    start_time: datetime
    end_time: datetime
    participants: List[str]


class TranscriptSegment(BaseModel):
    speaker: str
    content: str
    timestamp: datetime


class MeetingTranscript(BaseModel):
    meeting_id: str
    meeting_subject: str
    transcript_segments: List[TranscriptSegment]
    duration_minutes: int


class GraphAuthRequest(BaseModel):
    tenant_id: str
    client_id: str
    client_secret: str


class GraphMeetingListResponse(BaseModel):
    meetings: List[MeetingInfo]
    total_count: int


class GraphTranscriptResponse(BaseModel):
    meeting_id: str
    transcript: MeetingTranscript
    status: str
