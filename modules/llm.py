"""
Meeting minutes business logic module
Converts JSON input to formatted text meeting minutes
"""

from utils.logger import get_logger
from schemas.llm import MeetingMinutesInput, MeetingMinutesOutput
from modules.prompt import MeetingMinutesPrompt
from typing import List

logger = get_logger("fastapi_app.modules.meeting_minutes")


class MeetingMinutesService:
    """Service class for meeting minutes generation operations"""
    
    def generate_meeting_minutes(self, input_data: MeetingMinutesInput) -> MeetingMinutesOutput:
        """
        Generate formatted text meeting minutes from JSON input
        
        Args:
            input_data: Meeting minutes input data
            
        Returns:
            MeetingMinutesOutput: Generated meeting minutes in text format
        """
        logger.info(f"Generating meeting minutes for: {input_data.title}")
        
        try:
            meeting_text = MeetingMinutesPrompt.format_meeting_minutes_text(input_data)
            
            logger.info("Meeting minutes generated successfully")
            return MeetingMinutesOutput(
                meeting_minutes_text=meeting_text
            )
            
        except Exception as e:
            logger.error(f"Error generating meeting minutes: {str(e)}")
            raise Exception(f"Failed to generate meeting minutes: {str(e)}")
