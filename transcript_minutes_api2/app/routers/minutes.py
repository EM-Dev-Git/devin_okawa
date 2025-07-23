from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.minutes import MinutesGenerateRequest, MinutesResponse, MinutesListResponse
from ..modules.transcript_processor import transcript_processor
from ..modules.minutes_formatter import minutes_formatter
from ..models import User, MeetingMinutes
from ..dependencies import get_current_user
from ..modules.logger import get_logger

router = APIRouter(prefix="/minutes", tags=["議事録"])
logger = get_logger(__name__)

@router.post("/generate", response_model=MinutesResponse)
async def generate_minutes(
    request: MinutesGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録生成開始: ユーザー {current_user.user_id}")
    
    try:
        processed_data = await transcript_processor.process_transcript(request.transcript)
        formatted_minutes = minutes_formatter.format_minutes(processed_data, request.header)
        
        participants_str = "、".join(request.header.participants) if request.header.participants else ""
        
        meeting_minutes = MeetingMinutes(
            user_id=current_user.id,
            title=request.header.title,
            date=request.header.date,
            location=request.header.location,
            participants=participants_str,
            absent_members="",
            facilitator=request.header.facilitator,
            transcript=request.transcript,
            formatted_minutes=formatted_minutes
        )
        
        db.add(meeting_minutes)
        db.commit()
        db.refresh(meeting_minutes)
        
        logger.info(f"議事録生成成功: ID {meeting_minutes.id}")
        return meeting_minutes
        
    except Exception as e:
        logger.error(f"議事録生成エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"議事録生成に失敗しました: {str(e)}"
        )

@router.get("/", response_model=MinutesListResponse)
async def get_minutes_list(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録一覧取得: ユーザー {current_user.user_id}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    total_count = db.query(MeetingMinutes).filter(
        MeetingMinutes.user_id == current_user.id
    ).count()
    
    logger.info(f"議事録一覧取得成功: {len(minutes)}件")
    return MinutesListResponse(minutes=minutes, total_count=total_count)

@router.get("/{minutes_id}", response_model=MinutesResponse)
async def get_minutes(
    minutes_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録取得: ID {minutes_id}, ユーザー {current_user.user_id}")
    
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
    
    logger.info(f"議事録取得成功: ID {minutes_id}")
    return minutes

@router.delete("/{minutes_id}")
async def delete_minutes(
    minutes_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"議事録削除開始: ID {minutes_id}, ユーザー {current_user.user_id}")
    
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
    
    logger.info(f"議事録削除成功: ID {minutes_id}")
    return {"message": "議事録を削除しました"}
