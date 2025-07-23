from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class GraphMeetingRequest(BaseModel):
    user_id: str


class GraphTranscriptRequest(BaseModel):
    user_id: str
    meeting_id: str


class GraphCallRecordsRequest(BaseModel):
    user_id: str
    limit: int = 10


class GraphTranscriptToMinutesRequest(BaseModel):
    user_id: str
    meeting_id: str
    title: str
    date: str
    location: str = "Microsoft Teams"
    participants: List[str] = []
    facilitator: str = "未指定"


class GraphMeetingResponse(BaseModel):
    meetings: List[Dict[str, Any]]


class GraphTranscriptResponse(BaseModel):
    transcript: Optional[str]
    meeting_id: str


class GraphCallRecordsResponse(BaseModel):
    call_records: List[Dict[str, Any]]


class GraphMinutesResponse(BaseModel):
    meeting_id: str
    generated_minutes: str
    title: str
