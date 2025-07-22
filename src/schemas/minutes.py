from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MinutesOutput(BaseModel):
    meeting_title: str
    meeting_date: datetime
    participants: List[str]
    summary: str
    key_points: List[str]
    action_items: List[str]
    next_meeting: Optional[datetime] = None
    generated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
