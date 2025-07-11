


from fastapi import APIRouter, HTTPException
from utils.logger import get_router_logger
from schemas.llm import MeetingMinutesInput, MeetingMinutesOutput
from modules.llm import MeetingMinutesService

logger = get_router_logger("llm")
router = APIRouter(prefix="/llm/call", tags=["llm"])
meeting_service = MeetingMinutesService()


@router.post("/minutes", response_model=MeetingMinutesOutput)
async def generate_meeting_minutes(input_data: MeetingMinutesInput):
    # input_data: 参加者、目標、進捗、解決策を含む会議情報
    try:
        logger.info(f"Received meeting minutes generation request for: {input_data.title}")
        
        result = meeting_service.generate_meeting_minutes(input_data)
        
        logger.info("Meeting minutes generated successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error in meeting minutes endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate meeting minutes: {str(e)}"
        )
