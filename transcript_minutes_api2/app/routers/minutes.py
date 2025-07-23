from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, MeetingMinutes
from ..schemas.minutes import MinutesCreate, Minutes, MinutesResponse
from ..dependencies import get_current_active_user
from ..modules.transcript_processor import transcript_processor
from ..modules.minutes_formatter import minutes_formatter
from ..modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/minutes", tags=["議事録"])


@router.post("/generate", response_model=Minutes)
async def generate_minutes(
    minutes_data: MinutesCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録生成開始: {minutes_data.title} by {current_user.username}")
    
    try:
        processed_data = await transcript_processor.process_transcript(
            minutes_data.transcript, 
            minutes_data.title
        )
        
        formatted_minutes = minutes_formatter.format_minutes(processed_data)
        
        db_minutes = MeetingMinutes(
            title=minutes_data.title,
            transcript=minutes_data.transcript,
            generated_minutes=formatted_minutes,
            user_id=current_user.id
        )
        
        db.add(db_minutes)
        db.commit()
        db.refresh(db_minutes)
        
        logger.info(f"議事録生成完了: {db_minutes.id}")
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
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    logger.info(f"議事録一覧取得: {current_user.username}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    response_minutes = []
    for minute in minutes:
        summary = minutes_formatter.extract_summary(minute.generated_minutes)
        response_minutes.append(MinutesResponse(
            id=minute.id,
            title=minute.title,
            generated_minutes=minute.generated_minutes,
            created_at=minute.created_at,
            summary=summary
        ))
    
    logger.info(f"議事録一覧取得完了: {len(response_minutes)}件")
    return response_minutes


@router.get("/{minutes_id}", response_model=Minutes)
async def get_minutes(
    minutes_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録取得: {minutes_id} by {current_user.username}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.id == minutes_id,
        MeetingMinutes.user_id == current_user.id
    ).first()
    
    if not minutes:
        logger.warning(f"議事録が見つかりません: {minutes_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="議事録が見つかりません"
        )
    
    logger.info(f"議事録取得完了: {minutes_id}")
    return minutes


@router.delete("/{minutes_id}")
async def delete_minutes(
    minutes_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録削除開始: {minutes_id} by {current_user.username}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.id == minutes_id,
        MeetingMinutes.user_id == current_user.id
    ).first()
    
    if not minutes:
        logger.warning(f"削除対象の議事録が見つかりません: {minutes_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="議事録が見つかりません"
        )
    
    db.delete(minutes)
    db.commit()
    
    logger.info(f"議事録削除完了: {minutes_id}")
    return {"message": "議事録が正常に削除されました"}
