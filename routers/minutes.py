from fastapi import APIRouter, HTTPException
from schemas.transcript import TranscriptInput
from schemas.minutes import MinutesOutput
from modules.minutes_generator import MinutesGenerator
import logging

router = APIRouter(prefix="/api/v1/minutes", tags=["minutes"])
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=MinutesOutput)
async def generate_meeting_minutes(transcript_data: TranscriptInput):
    try:
        logger.info(f"Received request to generate minutes for: {transcript_data.meeting_title}")
        
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
