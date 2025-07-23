from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, MeetingMinutes
from ..schemas.graph import (
    GraphMeetingRequest, GraphTranscriptRequest, GraphCallRecordsRequest,
    GraphTranscriptToMinutesRequest, GraphMeetingResponse, GraphTranscriptResponse,
    GraphCallRecordsResponse, GraphMinutesResponse
)
from ..schemas.minutes import MeetingHeader
from ..dependencies import get_current_user
from ..modules.graph_client import graph_service
from ..modules.transcript_processor import transcript_processor
from ..modules.minutes_formatter import minutes_formatter
from ..modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/graph", tags=["Microsoft Graph"])


@router.post("/meetings", response_model=GraphMeetingResponse)
async def get_meetings(
    request: GraphMeetingRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        logger.info(f"Graph会議一覧取得: ユーザー {request.user_id}")
        
        meetings = await graph_service.get_online_meetings(request.user_id)
        
        logger.info(f"Graph会議一覧取得完了: {len(meetings)}件")
        return GraphMeetingResponse(meetings=meetings)
        
    except Exception as e:
        logger.error(f"Graph会議一覧取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"会議一覧の取得に失敗しました: {str(e)}"
        )


@router.post("/transcript", response_model=GraphTranscriptResponse)
async def get_transcript(
    request: GraphTranscriptRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        logger.info(f"Graphトランスクリプト取得: 会議ID {request.meeting_id}")
        
        transcript = await graph_service.get_meeting_transcript(request.user_id, request.meeting_id)
        
        logger.info(f"Graphトランスクリプト取得完了: 会議ID {request.meeting_id}")
        return GraphTranscriptResponse(transcript=transcript, meeting_id=request.meeting_id)
        
    except Exception as e:
        logger.error(f"Graphトランスクリプト取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"トランスクリプトの取得に失敗しました: {str(e)}"
        )


@router.post("/call-records", response_model=GraphCallRecordsResponse)
async def get_call_records(
    request: GraphCallRecordsRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        logger.info(f"Graph通話記録取得: ユーザー {request.user_id}")
        
        call_records = await graph_service.get_call_records(request.user_id, request.limit)
        
        logger.info(f"Graph通話記録取得完了: {len(call_records)}件")
        return GraphCallRecordsResponse(call_records=call_records)
        
    except Exception as e:
        logger.error(f"Graph通話記録取得エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"通話記録の取得に失敗しました: {str(e)}"
        )


@router.post("/transcript-to-minutes", response_model=GraphMinutesResponse)
async def convert_graph_transcript_to_minutes(
    request: GraphTranscriptToMinutesRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Graph議事録変換開始: 会議ID {request.meeting_id}")
        
        transcript = await graph_service.get_meeting_transcript(request.user_id, request.meeting_id)
        
        if not transcript:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された会議のトランスクリプトが見つかりません"
            )
        
        header = MeetingHeader(
            title=request.title,
            date=request.date,
            location=request.location,
            participants=request.participants,
            facilitator=request.facilitator
        )
        
        processed_data = await transcript_processor.process_transcript(transcript)
        formatted_minutes = minutes_formatter.format_minutes(processed_data, header)
        
        db_minutes = MeetingMinutes(
            title=request.title,
            transcript=transcript,
            generated_minutes=formatted_minutes,
            user_id=current_user.id
        )
        
        db.add(db_minutes)
        db.commit()
        db.refresh(db_minutes)
        
        logger.info(f"Graph議事録変換完了: 会議ID {request.meeting_id}")
        return GraphMinutesResponse(
            meeting_id=request.meeting_id,
            generated_minutes=formatted_minutes,
            title=request.title
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Graph議事録変換エラー: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"議事録変換に失敗しました: {str(e)}"
        )
