


from pydantic import BaseModel, Field
from typing import Optional


class MeetingMinutesInput(BaseModel):
    title: str = Field(..., description="Meeting title")  # 会議タイトル
    date: str = Field(..., description="Meeting date")  # 会議日時
    meeting_room: str = Field(..., description="Meeting room/location")  # 会議室/場所
    attendees: str = Field(..., description="Meeting attendees")  # 参加者
    absentees: str = Field(..., description="Absent members")  # 欠席者
    facility: str = Field(..., description="Meeting facilitator/chairperson")  # 司会者/ファシリティ
    text: str = Field(..., description="Meeting transcript text")  # 会議文字起こしテキスト
    
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="OpenAI generation temperature (0.0-2.0)")  # 生成温度
    top_p: Optional[float] = Field(1.0, ge=0.0, le=1.0, description="OpenAI nucleus sampling parameter (0.0-1.0)")  # Top-pサンプリング
    model: Optional[str] = Field("gpt-4", description="OpenAI model to use")  # 使用モデル
    max_tokens: Optional[int] = Field(2000, ge=1, le=4096, description="Maximum tokens for response")  # 最大トークン数


class MeetingMinutesOutput(BaseModel):
    meeting_minutes_text: str = Field(..., description="Generated meeting minutes in text format")  # 生成された議事録テキスト
