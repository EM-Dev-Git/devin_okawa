from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class MeetingInfo(BaseModel):
    id: str
    subject: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    organizer: Optional[str] = None
    participants: Optional[List[str]] = None

class TranscriptRequest(BaseModel):
    user_id: str
    meeting_id: str

class TranscriptResponse(BaseModel):
    meeting_id: str
    transcript_content: str
    meeting_info: Optional[MeetingInfo] = None

class MeetingListRequest(BaseModel):
    user_id: str
    limit: Optional[int] = 10

class MeetingListResponse(BaseModel):
    meetings: List[MeetingInfo]
    total_count: int

class CallRecordRequest(BaseModel):
    user_id: str
    limit: Optional[int] = 10

class CallRecordResponse(BaseModel):
    call_records: List[Dict[str, Any]]
    total_count: int
