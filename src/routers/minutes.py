from fastapi import APIRouter, HTTPException
from ..schemas.transcript import TranscriptRequest
from ..schemas.minutes import MinutesResponse
from ..modules.transcript_processor import TranscriptProcessor
import logging

router = APIRouter(prefix="/minutes", tags=["議事録"])
processor = TranscriptProcessor()
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=MinutesResponse)
async def generate_minutes(request: TranscriptRequest):
    """トランスクリプトから議事録を生成"""
    try:
        logger.info("議事録生成リクエスト受信")
        result = await processor.process_transcript(request)
        return result
    except Exception as e:
        logger.error(f"議事録生成API エラー: {e}")
        raise HTTPException(status_code=500, detail="議事録生成に失敗しました")

@router.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "healthy", "service": "minutes-api"}
