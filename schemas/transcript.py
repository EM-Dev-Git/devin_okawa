from pydantic import BaseModel
from typing import List
from datetime import datetime

class TranscriptInput(BaseModel):
    meeting_title: str
    meeting_date: datetime
    participants: List[str]
    transcript_text: str
