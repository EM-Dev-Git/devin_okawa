from fastapi import APIRouter, HTTPException, Depends
from src.schemas.transcript import TranscriptInput
from src.schemas.minutes import MinutesOutput
from src.modules.minutes_generator import MinutesGenerator
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/minutes", tags=["minutes"])

def get_minutes_generator() -> MinutesGenerator:
    return MinutesGenerator()

@router.post("/generate", response_model=MinutesOutput)
async def generate_meeting_minutes(
    transcript_data: TranscriptInput,
    generator: MinutesGenerator = Depends(get_minutes_generator)
):
    try:
        logger.info(f"Received minutes generation request: {transcript_data.meeting_title}")
        
        minutes = generator.generate_minutes(transcript_data)
        
        logger.info("Minutes generation request completed successfully")
        return minutes
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        logger.error(f"Internal server error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "minutes-generator"}
