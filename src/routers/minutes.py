from fastapi import APIRouter, HTTPException, Depends
from src.schemas.transcript import TranscriptInput
from src.schemas.minutes import MinutesOutput
from src.modules.minutes_generator import MinutesGenerator
from src.auth.dependencies import get_current_active_user
from src.auth.models import User
import logging

router = APIRouter(prefix="/api/v1/minutes", tags=["minutes"])
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=MinutesOutput)
async def generate_meeting_minutes(
    transcript_data: TranscriptInput,
    current_user: User = Depends(get_current_active_user)
):
    try:
        logger.info(f"User {current_user.username} requested minutes generation for: {transcript_data.meeting_title}")
        
        generator = MinutesGenerator()
        minutes = generator.generate_minutes(transcript_data)
        
        logger.info(f"Minutes generation completed for user: {current_user.username}")
        return minutes
        
    except Exception as e:
        logger.error(f"Error generating meeting minutes for user {current_user.username}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate meeting minutes: {str(e)}"
        )
