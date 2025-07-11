from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ActionItem(BaseModel):
    task: str = Field(..., description="タスク内容")
    assignee: str = Field(..., description="担当者")
    due_date: Optional[str] = Field(None, description="期限")

class MinutesOutput(BaseModel):
    meeting_title: str = Field(..., description="会議タイトル")
    meeting_date: datetime = Field(..., description="会議日時")
    participants: List[str] = Field(..., description="参加者")
    summary: str = Field(..., description="会議要約")
    key_points: List[str] = Field(..., description="主要ポイント")
    decisions: List[str] = Field(..., description="決定事項")
    action_items: List[ActionItem] = Field(..., description="アクションアイテム")
    next_meeting: Optional[str] = Field(None, description="次回会議予定")
    generated_at: datetime = Field(default_factory=datetime.now, description="生成日時")
    
    class Config:
        json_schema_extra = {
            "example": {
                "meeting_title": "週次進捗会議",
                "meeting_date": "2025-01-11T09:00:00",
                "participants": ["田中", "佐藤", "鈴木"],
                "summary": "今週の進捗状況と来週の計画について議論",
                "key_points": ["プロジェクトA進捗80%", "課題Bの解決策検討"],
                "decisions": ["来週までにプロトタイプ完成"],
                "action_items": [
                    {
                        "task": "プロトタイプ作成",
                        "assignee": "田中",
                        "due_date": "2025-01-18"
                    }
                ],
                "next_meeting": "2025-01-18T09:00:00"
            }
        }
