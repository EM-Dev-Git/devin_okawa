from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models import User, MeetingMinutes
from ..schemas.graph import MeetingInfo, MeetingTranscript, GraphMinutesRequest, GraphMinutesResponse
from ..modules.graph_client import graph_client
from ..modules.transcript_processor import TranscriptProcessor
from ..modules.minutes_formatter import MinutesFormatter
from ..dependencies import get_current_user
from ..modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/graph", tags=["Microsoft Graph"])


@router.get("/meetings", response_model=List[MeetingInfo])
async def get_teams_meetings(
    days_back: int = 7,
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Teams会議一覧取得開始: ユーザー={current_user.username}, 過去{days_back}日")
    
    try:
        meetings = await graph_client.get_meetings(days_back=days_back)
        
        meeting_infos = []
        for meeting in meetings:
            meeting_infos.append(MeetingInfo(
                id=meeting['id'],
                subject=meeting['subject'],
                start_time=datetime.fromisoformat(meeting['start_time'].replace('Z', '+00:00')) if meeting['start_time'] else datetime.now(),
                end_time=datetime.fromisoformat(meeting['end_time'].replace('Z', '+00:00')) if meeting['end_time'] else datetime.now(),
                organizer=meeting['organizer']
            ))
        
        logger.info(f"Teams会議一覧取得完了: {len(meeting_infos)}件")
        return meeting_infos
        
    except Exception as e:
        logger.error(f"Teams会議取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Teams会議の取得に失敗しました: {str(e)}"
        )


@router.get("/meetings/{meeting_id}/transcript", response_model=MeetingTranscript)
async def get_meeting_transcript(
    meeting_id: str,
    current_user: User = Depends(get_current_user)
):
    logger.info(f"会議トランスクリプト取得開始: 会議ID={meeting_id}, ユーザー={current_user.username}")
    
    try:
        transcript_data = await graph_client.get_meeting_transcript(meeting_id)
        
        if not transcript_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された会議のトランスクリプトが見つかりません"
            )
        
        meeting_transcript = MeetingTranscript(
            meeting_id=transcript_data['meeting_id'],
            meeting_subject=transcript_data['meeting_subject'],
            segments=transcript_data['segments'],
            duration_minutes=transcript_data['duration_minutes']
        )
        
        logger.info(f"会議トランスクリプト取得完了: 会議ID={meeting_id}")
        return meeting_transcript
        
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
    current_user: User = Depends(get_current_user)
):
    logger.info(f"会議トランスクリプト一覧取得開始: 会議ID={meeting_id}, ユーザー={current_user.username}")
    
    try:
        transcripts = await graph_client.get_meeting_transcripts_list(meeting_id)
        
        logger.info(f"会議トランスクリプト一覧取得完了: 会議ID={meeting_id}, {len(transcripts)}件")
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


@router.post("/meetings/{meeting_id}/generate-minutes", response_model=GraphMinutesResponse)
async def generate_minutes_from_graph_meeting(
    meeting_id: str,
    request: GraphMinutesRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Graph会議から議事録生成開始: 会議ID={meeting_id}, ユーザー={current_user.username}")
    
    try:
        transcript_data = await graph_client.get_meeting_transcript(meeting_id)
        
        if not transcript_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された会議のトランスクリプトが見つかりません"
            )
        
        transcript_text = transcript_data['transcript_text']
        
        if not transcript_text or transcript_text.strip() == '':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="トランスクリプトが空です"
            )
        
        processor = TranscriptProcessor()
        formatter = MinutesFormatter()
        
        processed_data = await processor.process_transcript(transcript_text)
        formatted_minutes = await formatter.format_minutes(
            processed_data,
            title=request.title or transcript_data['meeting_subject']
        )
        
        db_minutes = MeetingMinutes(
            title=request.title or transcript_data['meeting_subject'],
            transcript=transcript_text,
            generated_minutes=formatted_minutes,
            user_id=current_user.id
        )
        
        db.add(db_minutes)
        db.commit()
        db.refresh(db_minutes)
        
        response = GraphMinutesResponse(
            meeting_id=meeting_id,
            meeting_subject=transcript_data['meeting_subject'],
            transcript=transcript_text,
            generated_minutes=formatted_minutes,
            created_at=db_minutes.created_at
        )
        
        logger.info(f"Graph会議から議事録生成完了: 会議ID={meeting_id}, 議事録ID={db_minutes.id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Graph会議から議事録生成エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"議事録の生成に失敗しました: {str(e)}"
        )
