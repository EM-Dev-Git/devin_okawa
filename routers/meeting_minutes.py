"""
Meeting minutes router for JSON to text conversion
Single endpoint for meeting minutes generation
"""

from fastapi import APIRouter, HTTPException
from utils.logger import get_router_logger
from schemas.meeting_minutes import MeetingMinutesInput, MeetingMinutesOutput
from modules.meeting_minutes import MeetingMinutesService

logger = get_router_logger("meeting_minutes")
router = APIRouter(prefix="/meeting-minutes", tags=["meeting-minutes"])
meeting_service = MeetingMinutesService()


@router.post("/generate", response_model=MeetingMinutesOutput)
async def generate_meeting_minutes(input_data: MeetingMinutesInput):
    """
    Generate text format meeting minutes from JSON input
    
    Takes structured JSON data and converts it to formatted Japanese meeting minutes text.
    
    Args:
        input_data: Meeting information including participants, goals, progress, and solutions
        
    Returns:
        MeetingMinutesOutput: Generated meeting minutes in text format
    """
    try:
        logger.info(f"Received meeting minutes generation request for: {input_data.title}")
        
        result = meeting_service.generate_meeting_minutes(input_data)
        
        if result.success:
            logger.info("Meeting minutes generated successfully")
        else:
            logger.warning(f"Meeting minutes generation failed: {result.message}")
            
        return result
        
    except Exception as e:
        logger.error(f"Error in meeting minutes endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate meeting minutes: {str(e)}"
        )
