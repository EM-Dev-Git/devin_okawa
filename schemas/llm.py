


from pydantic import BaseModel, Field


class MeetingMinutesInput(BaseModel):
    title: str = Field(..., description="Meeting title")  # 会議タイトル
    date: str = Field(..., description="Meeting date")  # 会議日時
    meeting_room: str = Field(..., description="Meeting room/location")  # 会議室/場所
    attendees: str = Field(..., description="Meeting attendees")  # 参加者
    absentees: str = Field(..., description="Absent members")  # 欠席者
    facility: str = Field(..., description="Meeting facilitator/chairperson")  # 司会者/ファシリティ
    text: str = Field(..., description="Meeting transcript text")  # 会議文字起こしテキスト


class MeetingMinutesOutput(BaseModel):
    meeting_minutes_text: str = Field(..., description="Generated meeting minutes in text format")  # 生成された議事録テキスト
