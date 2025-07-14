from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ActionItem(BaseModel):
    task: str
    assignee: str
    due_date: Optional[str] = None

class MinutesOutput(BaseModel):
    meeting_title: str
    meeting_date: datetime
    participants: List[str]
    summary: str
    key_points: List[str]
    decisions: List[str]
    action_items: List[ActionItem]
    next_meeting: Optional[str] = None
