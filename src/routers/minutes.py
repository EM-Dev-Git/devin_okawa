from fastapi import APIRouter, HTTPException, Depends
from src.schemas.transcript import TranscriptRequest
from src.schemas.minutes import MinutesResponse
from src.schemas.auth import UserResponse
from src.modules.transcript_processor import TranscriptProcessor
from src.dependencies.auth import get_current_active_user
import logging

router = APIRouter(prefix="/minutes", tags=["議事録"])
processor = TranscriptProcessor()
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=MinutesResponse)
async def generate_minutes(
    request: TranscriptRequest,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """トランスクリプトから議事録を生成"""
    try:
        logger.info(f"議事録生成リクエスト受信 (ユーザー: {current_user.username})")
        result = await processor.process_transcript(request)
        return result
    except Exception as e:
        logger.error(f"議事録生成API エラー: {e} (ユーザー: {current_user.username})")
        raise HTTPException(status_code=500, detail="議事録生成に失敗しました")

@router.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "healthy", "service": "minutes-api"}
