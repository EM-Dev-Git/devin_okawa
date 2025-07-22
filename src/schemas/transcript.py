from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TranscriptInput(BaseModel):
    meeting_title: str
    meeting_date: datetime
    participants: List[str]
    transcript_text: str
    additional_notes: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
