from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, MeetingMinutes
from ..schemas.minutes import TranscriptRequest, MinutesResponse
from ..dependencies import get_current_active_user
from ..modules.transcript_processor import TranscriptProcessor
from ..modules.minutes_formatter import MeetingMinutesFormatter
from ..modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/minutes", tags=["議事録"])

transcript_processor = TranscriptProcessor()
minutes_formatter = MeetingMinutesFormatter()


@router.post("/generate", response_model=MinutesResponse)
async def generate_minutes(
    request: TranscriptRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"議事録生成開始: ユーザー {current_user.username}")
        
        header = request.header.dict()
        
        analysis_result = await transcript_processor.analyze_transcript(
            request.transcript, 
            header
        )
        
        formatted_minutes = minutes_formatter.format_minutes(
            analysis_result["analysis"], 
            header
        )
        
        db_minutes = MeetingMinutes(
            title=header["title"],
            transcript=request.transcript,
            generated_minutes=formatted_minutes,
            user_id=current_user.id
        )
        
        db.add(db_minutes)
        db.commit()
        db.refresh(db_minutes)
        
        logger.info(f"議事録生成完了: ID {db_minutes.id}")
        return db_minutes
        
    except Exception as e:
        logger.error(f"議事録生成エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"議事録生成中にエラーが発生しました: {str(e)}"
        )


@router.get("/", response_model=List[MinutesResponse])
async def get_user_minutes(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"ユーザー議事録一覧取得: {current_user.username}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.user_id == current_user.id
    ).order_by(MeetingMinutes.created_at.desc()).all()
    
    logger.info(f"議事録一覧取得完了: {len(minutes)}件")
    return minutes


@router.get("/{minutes_id}", response_model=MinutesResponse)
async def get_minutes(
    minutes_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録取得: ID {minutes_id}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.id == minutes_id,
        MeetingMinutes.user_id == current_user.id
    ).first()
    
    if not minutes:
        logger.warning(f"存在しない議事録へのアクセス: ID {minutes_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="議事録が見つかりません"
        )
    
    logger.info(f"議事録取得完了: ID {minutes_id}")
    return minutes


@router.delete("/{minutes_id}")
async def delete_minutes(
    minutes_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録削除開始: ID {minutes_id}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.id == minutes_id,
        MeetingMinutes.user_id == current_user.id
    ).first()
    
    if not minutes:
        logger.warning(f"存在しない議事録の削除試行: ID {minutes_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="議事録が見つかりません"
        )
    
    db.delete(minutes)
    db.commit()
    
    logger.info(f"議事録削除完了: ID {minutes_id}")
    return {"message": "議事録が正常に削除されました"}
