from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, MeetingMinutes
from ..schemas.graph import MeetingInfo, MeetingTranscript, GraphMinutesRequest, GraphMinutesResponse
from ..schemas.minutes import Minutes
from ..dependencies import get_current_active_user
from ..modules.graph_client import graph_client
from ..modules.transcript_processor import transcript_processor
from ..modules.minutes_formatter import minutes_formatter
from ..modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/graph", tags=["Microsoft Graph"])


@router.get("/meetings", response_model=List[MeetingInfo])
async def get_meetings(
    days_back: int = 7,
    current_user: User = Depends(get_current_active_user)
):
    logger.info(f"Teams会議一覧取得開始: {current_user.username}")
    
    try:
        meetings = await graph_client.get_meetings(days_back=days_back)
        
        meeting_list = []
        for meeting in meetings:
            meeting_list.append(MeetingInfo(
                id=meeting['id'],
                subject=meeting['subject'],
                start_time=meeting['start_time'],
                end_time=meeting['end_time'],
                organizer=meeting['organizer']
            ))
        
        logger.info(f"Teams会議一覧取得完了: {len(meeting_list)}件")
        return meeting_list
        
    except Exception as e:
        logger.error(f"Teams会議一覧取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Teams会議の取得に失敗しました: {str(e)}"
        )


@router.get("/meetings/{meeting_id}/transcript", response_model=MeetingTranscript)
async def get_meeting_transcript(
    meeting_id: str,
    current_user: User = Depends(get_current_active_user)
):
    logger.info(f"会議トランスクリプト取得開始: {meeting_id} by {current_user.username}")
    
    try:
        transcript_data = await graph_client.get_meeting_transcript(meeting_id)
        
        if not transcript_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された会議のトランスクリプトが見つかりません"
            )
        
        transcript = MeetingTranscript(
            meeting_id=transcript_data['meeting_id'],
            meeting_subject=transcript_data['meeting_subject'],
            segments=transcript_data['segments'],
            duration_minutes=transcript_data['duration_minutes']
        )
        
        logger.info(f"会議トランスクリプト取得完了: {meeting_id}")
        return transcript
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"会議トランスクリプト取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"トランスクリプトの取得に失敗しました: {str(e)}"
        )


@router.get("/meetings/{meeting_id}/transcripts")
async def get_meeting_transcripts_list(
    meeting_id: str,
    current_user: User = Depends(get_current_active_user)
):
    logger.info(f"会議トランスクリプト一覧取得開始: {meeting_id} by {current_user.username}")
    
    try:
        transcripts = await graph_client.get_meeting_transcripts_list(meeting_id)
        
        logger.info(f"会議トランスクリプト一覧取得完了: {len(transcripts)}件")
        return {
            "meeting_id": meeting_id,
            "transcripts": transcripts,
            "count": len(transcripts)
        }
        
    except Exception as e:
        logger.error(f"会議トランスクリプト一覧取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"トランスクリプト一覧の取得に失敗しました: {str(e)}"
        )


@router.post("/meetings/{meeting_id}/generate-minutes", response_model=Minutes)
async def generate_minutes_from_graph(
    meeting_id: str,
    request: GraphMinutesRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Graph会議議事録生成開始: {meeting_id} by {current_user.username}")
    
    try:
        transcript_data = await graph_client.get_meeting_transcript(meeting_id)
        
        if not transcript_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された会議のトランスクリプトが見つかりません"
            )
        
        title = request.title or transcript_data['meeting_subject']
        transcript_text = transcript_data['transcript_text']
        
        processed_data = await transcript_processor.process_transcript(
            transcript_text, 
            title
        )
        
        formatted_minutes = minutes_formatter.format_minutes(processed_data)
        
        db_minutes = MeetingMinutes(
            title=title,
            transcript=transcript_text,
            generated_minutes=formatted_minutes,
            user_id=current_user.id
        )
        
        db.add(db_minutes)
        db.commit()
        db.refresh(db_minutes)
        
        logger.info(f"Graph会議議事録生成完了: {db_minutes.id}")
        return db_minutes
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Graph会議議事録生成エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"議事録生成中にエラーが発生しました: {str(e)}"
        )
