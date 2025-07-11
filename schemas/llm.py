"""
Meeting minutes schema models for JSON input and text output
Following FastAPI official documentation patterns for Pydantic models
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ParticipantProgress(BaseModel):
    """Individual participant progress information"""
    name: str = Field(..., description="Participant name")
    previous_achievement_rate: int = Field(..., ge=0, le=100, description="Previous day achievement rate (0-100%)")
    progress_status: str = Field(..., description="Current progress status")
    issues: str = Field(..., description="Current issues or problems")


class ParticipantGoal(BaseModel):
    """Individual participant goal information"""
    name: str = Field(..., description="Participant name")
    goal_content: str = Field(..., description="Today's business goal content")


class ParticipantSolution(BaseModel):
    """Individual participant solution information"""
    name: str = Field(..., description="Participant name")
    solution_content: str = Field(..., description="Problem solution content")


class MeetingMinutesInput(BaseModel):
    """Input schema for meeting minutes generation from JSON"""
    title: str = Field(..., description="Meeting title")
    date: str = Field(..., description="Meeting date")
    location: str = Field(..., description="Meeting location")
    participants: List[str] = Field(..., description="List of participant names")
    absent_members: List[str] = Field(default=[], description="List of absent member names")
    facilitator: str = Field(..., description="Meeting facilitator/chairperson")
    
    participant_goals: List[ParticipantGoal] = Field(..., description="Today's business goals by participant")
    
    participant_progress: List[ParticipantProgress] = Field(..., description="Current progress and issues by participant")
    
    participant_solutions: List[ParticipantSolution] = Field(..., description="Problem solutions by participant")


class MeetingMinutesOutput(BaseModel):
    """Output schema for generated meeting minutes"""
    meeting_minutes_text: str = Field(..., description="Generated meeting minutes in text format")
