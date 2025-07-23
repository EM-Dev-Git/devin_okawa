from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, MeetingMinutes
from ..schemas.minutes import TranscriptRequest, MinutesResponse
from ..dependencies import get_current_user
from ..modules.transcript_processor import transcript_processor
from ..modules.minutes_formatter import minutes_formatter
from ..modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/minutes", tags=["議事録生成"])


@router.post("/generate", response_model=MinutesResponse, status_code=status.HTTP_201_CREATED)
async def generate_minutes(
    request: TranscriptRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"議事録生成開始: ユーザー {current_user.username}, 会議 {request.header.title}")
        
        processed_data = await transcript_processor.process_transcript(request.transcript)
        
        formatted_minutes = minutes_formatter.format_minutes(processed_data, request.header)
        
        db_minutes = MeetingMinutes(
            title=request.header.title,
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
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"議事録生成に失敗しました: {str(e)}"
        )


@router.get("/", response_model=List[MinutesResponse])
async def get_user_minutes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"ユーザー議事録一覧取得: {current_user.username}")
    minutes = db.query(MeetingMinutes).filter(MeetingMinutes.user_id == current_user.id).all()
    return minutes


@router.get("/{minutes_id}", response_model=MinutesResponse)
async def get_minutes_by_id(
    minutes_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録取得: ID {minutes_id}, ユーザー {current_user.username}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.id == minutes_id,
        MeetingMinutes.user_id == current_user.id
    ).first()
    
    if not minutes:
        logger.warning(f"議事録が見つかりません: ID {minutes_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="議事録が見つかりません"
        )
    
    return minutes


@router.delete("/{minutes_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_minutes(
    minutes_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録削除: ID {minutes_id}, ユーザー {current_user.username}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.id == minutes_id,
        MeetingMinutes.user_id == current_user.id
    ).first()
    
    if not minutes:
        logger.warning(f"削除対象の議事録が見つかりません: ID {minutes_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="議事録が見つかりません"
        )
    
    db.delete(minutes)
    db.commit()
    
    logger.info(f"議事録削除完了: ID {minutes_id}")
