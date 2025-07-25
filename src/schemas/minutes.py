from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MinutesResponse(BaseModel):
    id: str = Field(..., description="議事録ID")
    title: str = Field(..., description="会議タイトル")
    content: str = Field(..., description="議事録内容")
    created_at: datetime = Field(..., description="作成日時")
    participants: Optional[list[str]] = Field(None, description="参加者リスト")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "minutes_001",
                "title": "週次定例会議",
                "content": "## 議事録\n\n### 議題1\n...",
                "created_at": "2025-01-24T10:00:00Z",
                "participants": ["田中", "佐藤", "鈴木"]
            }
        }
    }
