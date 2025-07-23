from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.minutes import MinutesRequest, MinutesResponse, MinutesListResponse
from ..modules.transcript_processor import transcript_processor
from ..modules.minutes_formatter import minutes_formatter
from ..dependencies import get_current_user
from ..models import User, MeetingMinutes
from ..modules.logger import get_logger

router = APIRouter(prefix="/minutes", tags=["議事録"])
logger = get_logger(__name__)

@router.post("/generate", response_model=MinutesResponse)
async def generate_minutes(
    request: MinutesRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録生成開始: {current_user.user_id} - {request.header.title}")
    
    try:
        raw_minutes = await transcript_processor.process_transcript(
            request.transcript, request.header
        )
        
        formatted_minutes = minutes_formatter.format_minutes(raw_minutes, request.header)
        
        participants_str = "、".join(request.header.participants)
        absent_str = "、".join(request.header.absent_members) if request.header.absent_members else ""
        
        db_minutes = MeetingMinutes(
            user_id=current_user.id,
            title=request.header.title,
            date=request.header.date,
            location=request.header.location,
            participants=participants_str,
            absent_members=absent_str,
            facilitator=request.header.facilitator,
            transcript=request.transcript,
            formatted_minutes=formatted_minutes
        )
        
        db.add(db_minutes)
        db.commit()
        db.refresh(db_minutes)
        
        logger.info(f"議事録生成完了: {current_user.user_id} - ID:{db_minutes.id}")
        return db_minutes
        
    except Exception as e:
        logger.error(f"議事録生成エラー: {current_user.user_id} - {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"議事録生成に失敗しました: {str(e)}"
        )

@router.get("/", response_model=List[MinutesListResponse])
async def get_minutes_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録一覧取得: {current_user.user_id}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.user_id == current_user.id
    ).order_by(MeetingMinutes.created_at.desc()).all()
    
    return minutes

@router.get("/{minutes_id}", response_model=MinutesResponse)
async def get_minutes(
    minutes_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録取得: {current_user.user_id} - ID:{minutes_id}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.id == minutes_id,
        MeetingMinutes.user_id == current_user.id
    ).first()
    
    if not minutes:
        logger.warning(f"議事録が見つかりません: {current_user.user_id} - ID:{minutes_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="議事録が見つかりません"
        )
    
    return minutes

@router.delete("/{minutes_id}")
async def delete_minutes(
    minutes_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録削除: {current_user.user_id} - ID:{minutes_id}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.id == minutes_id,
        MeetingMinutes.user_id == current_user.id
    ).first()
    
    if not minutes:
        logger.warning(f"削除対象の議事録が見つかりません: {current_user.user_id} - ID:{minutes_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="議事録が見つかりません"
        )
    
    db.delete(minutes)
    db.commit()
    
    logger.info(f"議事録削除完了: {current_user.user_id} - ID:{minutes_id}")
    return {"message": "議事録を削除しました"}
