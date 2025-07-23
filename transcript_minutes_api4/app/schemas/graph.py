from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class MeetingRequest(BaseModel):
    user_id: str


class TranscriptRequest(BaseModel):
    meeting_id: str
    transcript_id: str


class CallRecordsRequest(BaseModel):
    from_date: str
    to_date: str


class GraphTranscriptToMinutesRequest(BaseModel):
    meeting_id: str
    transcript_id: str
    meeting_title: str
    participants: List[str] = []
    facilitator: str = "未設定"


class MeetingResponse(BaseModel):
    meetings: List[Dict[str, Any]]
    count: int


class TranscriptResponse(BaseModel):
    metadata: Dict[str, Any]
    content: str


class CallRecordsResponse(BaseModel):
    call_records: List[Dict[str, Any]]
    count: int


class GraphMinutesResponse(BaseModel):
    meeting_info: Dict[str, Any]
    transcript_content: str
    generated_minutes: str
    created_at: datetime
