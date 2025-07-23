from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.graph import (
    TranscriptRequest, TranscriptResponse, MeetingListRequest, 
    MeetingListResponse, CallRecordRequest, CallRecordResponse, MeetingInfo
)
from ..modules.graph_client import graph_service
from ..modules.logger import get_logger
from ..dependencies import get_current_user

router = APIRouter(prefix="/graph", tags=["Microsoft Graph"])
logger = get_logger(__name__)

@router.get("/meetings", response_model=MeetingListResponse)
async def get_meetings(
    user_id: str,
    limit: int = 10,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"会議一覧取得開始: ユーザー {current_user.user_id}")
    
    try:
        meetings_data = await graph_service.get_online_meetings(user_id)
        
        meetings = []
        for meeting in meetings_data:
            meeting_info = MeetingInfo(
                id=meeting.get("id", ""),
                subject=meeting.get("subject"),
                start_time=meeting.get("startDateTime"),
                end_time=meeting.get("endDateTime"),
                organizer=meeting.get("organizer", {}).get("identity", {}).get("user", {}).get("displayName"),
                participants=[
                    participant.get("identity", {}).get("user", {}).get("displayName", "")
                    for participant in meeting.get("participants", {}).get("attendees", [])
                    if participant.get("identity", {}).get("user")
                ]
            )
            meetings.append(meeting_info)
        
        logger.info(f"会議一覧取得成功: {len(meetings)}件")
        return MeetingListResponse(meetings=meetings, total_count=len(meetings))
        
    except Exception as e:
        logger.error(f"会議一覧取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"会議一覧の取得に失敗しました: {str(e)}"
        )

@router.post("/transcript", response_model=TranscriptResponse)
async def get_transcript(
    request: TranscriptRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"トランスクリプト取得開始: ユーザー {current_user.user_id}, 会議ID {request.meeting_id}")
    
    try:
        transcript_content = await graph_service.get_meeting_transcript(
            request.user_id, request.meeting_id
        )
        
        if not transcript_content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された会議のトランスクリプトが見つかりません"
            )
        
        logger.info(f"トランスクリプト取得成功: 会議ID {request.meeting_id}")
        return TranscriptResponse(
            meeting_id=request.meeting_id,
            transcript_content=transcript_content
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"トランスクリプト取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"トランスクリプトの取得に失敗しました: {str(e)}"
        )

@router.get("/call-records", response_model=CallRecordResponse)
async def get_call_records(
    user_id: str,
    limit: int = 10,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"通話記録取得開始: ユーザー {current_user.user_id}")
    
    try:
        call_records = await graph_service.get_call_records(user_id, limit)
        
        logger.info(f"通話記録取得成功: {len(call_records)}件")
        return CallRecordResponse(
            call_records=call_records,
            total_count=len(call_records)
        )
        
    except Exception as e:
        logger.error(f"通話記録取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"通話記録の取得に失敗しました: {str(e)}"
        )

@router.post("/transcript-to-minutes")
async def transcript_to_minutes(
    request: TranscriptRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Graph経由議事録生成開始: ユーザー {current_user.user_id}, 会議ID {request.meeting_id}")
    
    try:
        transcript_content = await graph_service.get_meeting_transcript(
            request.user_id, request.meeting_id
        )
        
        if not transcript_content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された会議のトランスクリプトが見つかりません"
            )
        
        from ..modules.transcript_processor import transcript_processor
        from ..modules.minutes_formatter import minutes_formatter
        from ..schemas.minutes import MeetingHeader
        from datetime import date
        
        header = MeetingHeader(
            title=f"会議 {request.meeting_id}",
            date=date.today(),
            location="Microsoft Teams",
            participants=[],
            facilitator=""
        )
        
        processed_data = await transcript_processor.process_transcript(transcript_content)
        formatted_minutes = minutes_formatter.format_minutes(processed_data, header)
        
        from ..models import MeetingMinutes
        
        meeting_minutes = MeetingMinutes(
            user_id=current_user.id,
            title=header.title,
            date=header.date,
            location=header.location,
            participants="",
            absent_members="",
            facilitator=header.facilitator,
            transcript=transcript_content,
            formatted_minutes=formatted_minutes
        )
        
        db.add(meeting_minutes)
        db.commit()
        db.refresh(meeting_minutes)
        
        logger.info(f"Graph経由議事録生成成功: ID {meeting_minutes.id}")
        
        return {
            "id": meeting_minutes.id,
            "title": meeting_minutes.title,
            "formatted_minutes": meeting_minutes.formatted_minutes,
            "created_at": meeting_minutes.created_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Graph経由議事録生成エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"議事録生成に失敗しました: {str(e)}"
        )
