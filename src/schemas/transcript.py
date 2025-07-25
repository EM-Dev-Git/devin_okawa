from pydantic import BaseModel, Field
from typing import Optional

class TranscriptRequest(BaseModel):
    content: str = Field(..., description="トランスクリプト内容")
    meeting_title: Optional[str] = Field(None, description="会議タイトル")
    participants: Optional[list[str]] = Field(None, description="参加者リスト")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "content": "会議のトランスクリプト内容...",
                "meeting_title": "週次定例会議",
                "participants": ["田中", "佐藤", "鈴木"]
            }
        }
    }
