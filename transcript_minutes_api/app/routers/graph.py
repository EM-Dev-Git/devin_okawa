from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..dependencies import get_current_user
from ..models import User
from ..schemas.graph import (
    MeetingInfo, 
    MeetingTranscript, 
    GraphMeetingListResponse,
    GraphTranscriptResponse
)
from ..modules.graph_client import graph_client
from ..modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/graph", tags=["Microsoft Graph"])


@router.get("/meetings", response_model=GraphMeetingListResponse)
async def get_meetings(
    days_back: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"User {current_user.username} requesting meetings for last {days_back} days")
    
    if not graph_client.is_configured():
        logger.error("Microsoft Graph client not configured")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Microsoft Graph integration not configured. Please contact administrator."
        )
    
    try:
        meetings = await graph_client.get_meetings(days_back=days_back)
        
        response = GraphMeetingListResponse(
            meetings=meetings,
            total_count=len(meetings)
        )
        
        logger.info(f"Successfully retrieved {len(meetings)} meetings for user {current_user.username}")
        return response
        
    except Exception as e:
        logger.error(f"Error retrieving meetings for user {current_user.username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve meetings from Microsoft Graph"
        )


@router.get("/meetings/{meeting_id}/transcript", response_model=GraphTranscriptResponse)
async def get_meeting_transcript(
    meeting_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"User {current_user.username} requesting transcript for meeting {meeting_id}")
    
    if not graph_client.is_configured():
        logger.error("Microsoft Graph client not configured")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Microsoft Graph integration not configured. Please contact administrator."
        )
    
    try:
        transcript = await graph_client.get_meeting_transcript(meeting_id)
        
        if not transcript:
            logger.warning(f"No transcript found for meeting {meeting_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transcript not found for meeting {meeting_id}"
            )
        
        response = GraphTranscriptResponse(
            meeting_id=meeting_id,
            transcript=transcript,
            status="success"
        )
        
        logger.info(f"Successfully retrieved transcript for meeting {meeting_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving transcript for meeting {meeting_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve transcript from Microsoft Graph"
        )


@router.get("/meetings/{meeting_id}/transcripts")
async def get_meeting_transcripts_list(
    meeting_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"User {current_user.username} requesting transcript list for meeting {meeting_id}")
    
    if not graph_client.is_configured():
        logger.error("Microsoft Graph client not configured")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Microsoft Graph integration not configured. Please contact administrator."
        )
    
    try:
        transcripts = await graph_client.get_meeting_transcripts_list(meeting_id)
        
        logger.info(f"Successfully retrieved {len(transcripts)} transcripts for meeting {meeting_id}")
        return {
            "meeting_id": meeting_id,
            "transcripts": transcripts,
            "total_count": len(transcripts)
        }
        
    except Exception as e:
        logger.error(f"Error retrieving transcript list for meeting {meeting_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve transcript list from Microsoft Graph"
        )


@router.get("/status")
async def get_graph_status(
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.username} checking Graph API status")
    
    return {
        "configured": graph_client.is_configured(),
        "service": "Microsoft Graph API",
        "status": "available" if graph_client.is_configured() else "not_configured"
    }
