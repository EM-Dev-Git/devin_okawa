from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TranscriptInput(BaseModel):
    meeting_title: str = Field(..., description="会議タイトル")
    meeting_date: datetime = Field(..., description="会議日時")
    participants: list[str] = Field(..., description="参加者リスト")
    transcript_text: str = Field(..., min_length=10, description="会議トランスクリプト")
    meeting_duration: Optional[int] = Field(None, description="会議時間（分）")
    
    class Config:
        json_schema_extra = {
            "example": {
                "meeting_title": "週次進捗会議",
                "meeting_date": "2025-01-11T09:00:00",
                "participants": ["田中", "佐藤", "鈴木"],
                "transcript_text": "おはようございます。今週の進捗について...",
                "meeting_duration": 30
            }
        }
