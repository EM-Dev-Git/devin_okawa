from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, MeetingMinutes
from ..schemas.graph import (
    MeetingRequest, TranscriptRequest, CallRecordsRequest,
    GraphTranscriptToMinutesRequest, MeetingResponse, TranscriptResponse,
    CallRecordsResponse, GraphMinutesResponse
)
from ..dependencies import get_current_active_user
from ..modules.graph_client import graph_service
from ..modules.transcript_processor import TranscriptProcessor
from ..modules.minutes_formatter import MeetingMinutesFormatter
from ..modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/graph", tags=["Microsoft Graph"])

transcript_processor = TranscriptProcessor()
minutes_formatter = MeetingMinutesFormatter()


@router.post("/meetings", response_model=MeetingResponse)
async def get_meetings(
    request: MeetingRequest,
    current_user: User = Depends(get_current_active_user)
):
    try:
        logger.info(f"Teams会議一覧取得開始: ユーザー {request.user_id}")
        
        meetings = await graph_service.get_online_meetings(request.user_id)
        
        logger.info(f"Teams会議一覧取得完了: {len(meetings)}件")
        return MeetingResponse(meetings=meetings, count=len(meetings))
        
    except Exception as e:
        logger.error(f"Teams会議一覧取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"会議一覧の取得中にエラーが発生しました: {str(e)}"
        )


@router.post("/transcript", response_model=TranscriptResponse)
async def get_transcript(
    request: TranscriptRequest,
    current_user: User = Depends(get_current_active_user)
):
    try:
        logger.info(f"トランスクリプト取得開始: 会議 {request.meeting_id}")
        
        transcript_data = await graph_service.get_meeting_transcript(
            request.meeting_id, 
            request.transcript_id
        )
        
        logger.info("トランスクリプト取得完了")
        return TranscriptResponse(
            metadata=transcript_data["metadata"],
            content=transcript_data["content"]
        )
        
    except Exception as e:
        logger.error(f"トランスクリプト取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"トランスクリプトの取得中にエラーが発生しました: {str(e)}"
        )


@router.post("/call-records", response_model=CallRecordsResponse)
async def get_call_records(
    request: CallRecordsRequest,
    current_user: User = Depends(get_current_active_user)
):
    try:
        logger.info(f"通話記録取得開始: {request.from_date} - {request.to_date}")
        
        call_records = await graph_service.get_call_records(
            request.from_date, 
            request.to_date
        )
        
        logger.info(f"通話記録取得完了: {len(call_records)}件")
        return CallRecordsResponse(call_records=call_records, count=len(call_records))
        
    except Exception as e:
        logger.error(f"通話記録取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"通話記録の取得中にエラーが発生しました: {str(e)}"
        )


@router.post("/transcript-to-minutes", response_model=GraphMinutesResponse)
async def convert_graph_transcript_to_minutes(
    request: GraphTranscriptToMinutesRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Graph トランスクリプトから議事録生成開始: 会議 {request.meeting_id}")
        
        transcript_data = await graph_service.get_meeting_transcript(
            request.meeting_id, 
            request.transcript_id
        )
        
        header = {
            "title": request.meeting_title,
            "date": transcript_data["metadata"].get("createdDateTime", "未設定"),
            "location": "Microsoft Teams",
            "participants": request.participants,
            "facilitator": request.facilitator
        }
        
        analysis_result = await transcript_processor.analyze_transcript(
            transcript_data["content"], 
            header
        )
        
        formatted_minutes = minutes_formatter.format_minutes(
            analysis_result["analysis"], 
            header
        )
        
        db_minutes = MeetingMinutes(
            title=request.meeting_title,
            transcript=transcript_data["content"],
            generated_minutes=formatted_minutes,
            user_id=current_user.id
        )
        
        db.add(db_minutes)
        db.commit()
        db.refresh(db_minutes)
        
        logger.info(f"Graph トランスクリプトから議事録生成完了: ID {db_minutes.id}")
        
        return GraphMinutesResponse(
            meeting_info=transcript_data["metadata"],
            transcript_content=transcript_data["content"],
            generated_minutes=formatted_minutes,
            created_at=db_minutes.created_at
        )
        
    except Exception as e:
        logger.error(f"Graph トランスクリプトから議事録生成エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"議事録生成中にエラーが発生しました: {str(e)}"
        )
