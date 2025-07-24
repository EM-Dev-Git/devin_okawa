from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, MeetingMinutes
from ..schemas.minutes import MinutesCreate, MinutesResponse, MinutesListResponse
from ..dependencies import get_current_active_user
from ..modules.transcript_processor import transcript_processor
from ..modules.minutes_formatter import minutes_formatter
from ..modules.logger import get_logger

router = APIRouter(prefix="/minutes", tags=["minutes"])
logger = get_logger(__name__)


@router.post("/generate", response_model=MinutesResponse)
async def generate_minutes(
    minutes_data: MinutesCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Minutes generation request: {minutes_data.title} by {current_user.username}")
    
    try:
        raw_minutes = await transcript_processor.process_transcript(
            minutes_data.transcript, 
            minutes_data.title
        )
        
        formatted_minutes = minutes_formatter.format_minutes(
            raw_minutes,
            {"title": minutes_data.title}
        )
        
        db_minutes = MeetingMinutes(
            user_id=current_user.id,
            title=minutes_data.title,
            transcript=minutes_data.transcript,
            generated_minutes=formatted_minutes
        )
        
        db.add(db_minutes)
        db.commit()
        db.refresh(db_minutes)
        
        logger.info(f"Minutes generated successfully: {db_minutes.id}")
        return db_minutes
        
    except Exception as e:
        logger.error(f"Minutes generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"議事録生成中にエラーが発生しました: {str(e)}"
        )


@router.get("/", response_model=List[MinutesListResponse])
async def get_user_minutes(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Minutes list request by: {current_user.username}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.user_id == current_user.id
    ).order_by(MeetingMinutes.created_at.desc()).all()
    
    return minutes


@router.get("/{minutes_id}", response_model=MinutesResponse)
async def get_minutes(
    minutes_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Minutes detail request: {minutes_id} by {current_user.username}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.id == minutes_id,
        MeetingMinutes.user_id == current_user.id
    ).first()
    
    if not minutes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Minutes not found"
        )
    
    return minutes


@router.delete("/{minutes_id}")
async def delete_minutes(
    minutes_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Minutes deletion request: {minutes_id} by {current_user.username}")
    
    minutes = db.query(MeetingMinutes).filter(
        MeetingMinutes.id == minutes_id,
        MeetingMinutes.user_id == current_user.id
    ).first()
    
    if not minutes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Minutes not found"
        )
    
    db.delete(minutes)
    db.commit()
    
    logger.info(f"Minutes deleted successfully: {minutes_id}")
    return {"message": "Minutes deleted successfully"}
