"""
Meeting minutes schema models for JSON input and text output
Following FastAPI official documentation patterns for Pydantic models
"""

from pydantic import BaseModel, Field


class MeetingMinutesInput(BaseModel):
    """Input schema for meeting minutes generation from JSON"""
    title: str = Field(..., description="Meeting title")
    date: str = Field(..., description="Meeting date")
    meeting_room: str = Field(..., description="Meeting room/location")
    attendees: str = Field(..., description="Meeting attendees")
    absentees: str = Field(..., description="Absent members")
    facility: str = Field(..., description="Meeting facilitator/chairperson")
    text: str = Field(..., description="Meeting transcript text")


class MeetingMinutesOutput(BaseModel):
    """Output schema for generated meeting minutes"""
    meeting_minutes_text: str = Field(..., description="Generated meeting minutes in text format")
