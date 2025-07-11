from fastapi import APIRouter, HTTPException
from utils.logger import get_router_logger
from schemas.llm import MeetingMinutesInput, MeetingMinutesOutput
from modules.llm import MeetingMinutesService

logger = get_router_logger("llm")  # LLMルーター用ロガー
router = APIRouter(prefix="/llm/call", tags=["llm"])  # APIルーターの設定
meeting_service = MeetingMinutesService()  # 議事録サービスインスタンス


@router.post("/minutes", response_model=MeetingMinutesOutput)
async def generate_meeting_minutes(input_data: MeetingMinutesInput):
    try:
        logger.info(f"Received meeting minutes generation request for: {input_data.title}")
        logger.info(f"OpenAI parameters - model: {input_data.model}, temperature: {input_data.temperature}, top_p: {input_data.top_p}, max_tokens: {input_data.max_tokens}")
        
        result = meeting_service.generate_meeting_minutes(input_data)
        
        logger.info("Meeting minutes generated successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error in meeting minutes endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate meeting minutes: {str(e)}"
        )
