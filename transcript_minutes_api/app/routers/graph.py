from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime
import time

from ..database import get_db
from ..dependencies import get_current_user
from ..models import User, MeetingMinutes
from ..schemas.graph import (
    GraphMeetingResponse, GraphTranscriptResponse, GraphMinutesRequest, 
    GraphMinutesResponse, GraphTranscriptContent
)
from ..modules.graph_client import graph_client
from ..modules.transcript_processor import TranscriptProcessor
from ..modules.minutes_formatter import MinutesFormatter

router = APIRouter(prefix="/graph", tags=["Microsoft Graph"])
logger = logging.getLogger(__name__)


@router.get("/meetings", response_model=GraphMeetingResponse)
async def get_meetings(
    days_back: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        meetings = await graph_client.get_meetings(days_back=days_back)
        
        return GraphMeetingResponse(
            meetings=meetings,
            total_count=len(meetings)
        )
        
    except Exception as e:
        logger.error(f"Failed to get meetings for user {current_user.username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"会議の取得に失敗しました: {str(e)}"
        )


@router.get("/meetings/{meeting_id}/transcript", response_model=GraphTranscriptContent)
async def get_meeting_transcript(
    meeting_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        transcript = await graph_client.get_meeting_transcript(meeting_id)
        
        if not transcript:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された会議のトランスクリプトが見つかりません"
            )
        
        return transcript
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get transcript for meeting {meeting_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"トランスクリプトの取得に失敗しました: {str(e)}"
        )


@router.get("/meetings/{meeting_id}/transcripts", response_model=GraphTranscriptResponse)
async def get_meeting_transcripts(
    meeting_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        transcripts = await graph_client.get_meeting_transcripts(meeting_id)
        
        return GraphTranscriptResponse(
            transcripts=transcripts,
            total_count=len(transcripts)
        )
        
    except Exception as e:
        logger.error(f"Failed to get transcripts for meeting {meeting_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"トランスクリプト一覧の取得に失敗しました: {str(e)}"
        )


@router.post("/meetings/{meeting_id}/generate-minutes", response_model=GraphMinutesResponse)
async def generate_minutes_from_graph_meeting(
    meeting_id: str,
    request: GraphMinutesRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    start_time = time.time()
    
    try:
        transcript_content = await graph_client.get_meeting_transcript(meeting_id)
        
        if not transcript_content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された会議のトランスクリプトが見つかりません"
            )
        
        processor = TranscriptProcessor()
        formatter = MinutesFormatter()
        
        processed_data = await processor.process_transcript(transcript_content.content)
        
        custom_prompt = request.custom_prompt or "以下のトランスクリプトから議事録を作成してください。"
        formatted_minutes = await formatter.format_minutes(processed_data, custom_prompt)
        
        meeting_minutes = MeetingMinutes(
            user_id=current_user.id,
            title=f"Graph会議議事録 - {meeting_id[:8]}",
            transcript=transcript_content.content,
            generated_minutes=formatted_minutes
        )
        
        db.add(meeting_minutes)
        db.commit()
        db.refresh(meeting_minutes)
        
        processing_time = time.time() - start_time
        
        logger.info(f"Generated minutes for Graph meeting {meeting_id} for user {current_user.username}")
        
        return GraphMinutesResponse(
            meeting_id=meeting_id,
            transcript_id=transcript_content.transcript_id,
            generated_minutes=formatted_minutes,
            created_at=meeting_minutes.created_at,
            processing_time_seconds=round(processing_time, 2)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate minutes for Graph meeting {meeting_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"議事録の生成に失敗しました: {str(e)}"
        )
