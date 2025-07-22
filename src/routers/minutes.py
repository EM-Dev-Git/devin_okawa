from fastapi import APIRouter, HTTPException, Depends
from src.schemas.transcript import TranscriptInput
from src.schemas.minutes import MinutesOutput
from src.modules.minutes_generator import MinutesGenerator
from src.dependencies.auth import get_current_user
import logging

router = APIRouter(prefix="/api/v1/minutes", tags=["minutes"])
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=MinutesOutput)
async def generate_meeting_minutes(
    transcript_data: TranscriptInput,
    current_user: dict = Depends(get_current_user)
):
    try:
        logger.info(f"Received request to generate minutes for: {transcript_data.meeting_title} by user: {current_user['username']}")
        
        generator = MinutesGenerator()
        minutes = generator.generate_minutes(transcript_data)
        
        logger.info("Minutes generation request completed successfully")
        return minutes
        
    except Exception as e:
        logger.error(f"Error generating meeting minutes: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate meeting minutes: {str(e)}"
        )
