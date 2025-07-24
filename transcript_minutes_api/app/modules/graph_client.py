from msgraph import GraphServiceClient
from azure.identity import ClientSecretCredential
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime, timedelta
from ..config import settings
from ..schemas.graph import GraphMeeting, GraphTranscript, GraphTranscriptContent

logger = logging.getLogger(__name__)


class GraphClientManager:
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        try:
            if not all([settings.graph_tenant_id, settings.graph_client_id, settings.graph_client_secret]):
                logger.warning("Microsoft Graph credentials not configured")
                return
            
            credential = ClientSecretCredential(
                tenant_id=settings.graph_tenant_id,
                client_id=settings.graph_client_id,
                client_secret=settings.graph_client_secret
            )
            
            self.client = GraphServiceClient(
                credentials=credential,
                scopes=['https://graph.microsoft.com/.default']
            )
            
            logger.info("Microsoft Graph client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Microsoft Graph client: {str(e)}")
            self.client = None
    
    async def get_meetings(self, days_back: int = 7) -> List[GraphMeeting]:
        if not self.client:
            raise Exception("Microsoft Graph client not initialized")
        
        try:
            start_time = datetime.now() - timedelta(days=days_back)
            start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            
            filter_query = f"start/dateTime ge '{start_time_str}'"
            
            events = await self.client.me.events.get(
                filter=filter_query,
                select=['id', 'subject', 'start', 'end', 'organizer', 'attendees'],
                top=50
            )
            
            meetings = []
            if events and events.value:
                for event in events.value:
                    participants = []
                    if event.attendees:
                        participants = [attendee.email_address.address for attendee in event.attendees if attendee.email_address]
                    
                    meeting = GraphMeeting(
                        id=event.id,
                        subject=event.subject or "無題の会議",
                        start_time=datetime.fromisoformat(event.start.date_time.replace('Z', '+00:00')),
                        end_time=datetime.fromisoformat(event.end.date_time.replace('Z', '+00:00')),
                        organizer=event.organizer.email_address.address if event.organizer and event.organizer.email_address else "不明",
                        participants=participants
                    )
                    meetings.append(meeting)
            
            logger.info(f"Retrieved {len(meetings)} meetings from Microsoft Graph")
            return meetings
            
        except Exception as e:
            logger.error(f"Failed to retrieve meetings: {str(e)}")
            raise Exception(f"会議の取得に失敗しました: {str(e)}")
    
    async def get_meeting_transcript(self, meeting_id: str) -> Optional[GraphTranscriptContent]:
        if not self.client:
            raise Exception("Microsoft Graph client not initialized")
        
        try:
            transcripts = await self.client.me.online_meetings.item(meeting_id).transcripts.get()
            
            if not transcripts or not transcripts.value:
                logger.warning(f"No transcripts found for meeting {meeting_id}")
                return None
            
            transcript = transcripts.value[0]
            
            transcript_content = await self.client.me.online_meetings.item(meeting_id).transcripts.item(transcript.id).content.get()
            
            if not transcript_content:
                logger.warning(f"No transcript content found for meeting {meeting_id}")
                return None
            
            content_text = transcript_content.decode('utf-8') if isinstance(transcript_content, bytes) else str(transcript_content)
            
            speakers = self._extract_speakers_from_transcript(content_text)
            duration = self._calculate_duration_from_transcript(content_text)
            
            return GraphTranscriptContent(
                transcript_id=transcript.id,
                content=content_text,
                speakers=speakers,
                duration_minutes=duration
            )
            
        except Exception as e:
            logger.error(f"Failed to retrieve transcript for meeting {meeting_id}: {str(e)}")
            raise Exception(f"トランスクリプトの取得に失敗しました: {str(e)}")
    
    async def get_meeting_transcripts(self, meeting_id: str) -> List[GraphTranscript]:
        if not self.client:
            raise Exception("Microsoft Graph client not initialized")
        
        try:
            transcripts = await self.client.me.online_meetings.item(meeting_id).transcripts.get()
            
            result = []
            if transcripts and transcripts.value:
                for transcript in transcripts.value:
                    graph_transcript = GraphTranscript(
                        id=transcript.id,
                        meeting_id=meeting_id,
                        content="",
                        created_datetime=datetime.fromisoformat(transcript.created_date_time.replace('Z', '+00:00')),
                        meeting_organizer=None
                    )
                    result.append(graph_transcript)
            
            logger.info(f"Retrieved {len(result)} transcripts for meeting {meeting_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to retrieve transcripts for meeting {meeting_id}: {str(e)}")
            raise Exception(f"トランスクリプト一覧の取得に失敗しました: {str(e)}")
    
    def _extract_speakers_from_transcript(self, content: str) -> List[str]:
        speakers = set()
        lines = content.split('\n')
        
        for line in lines:
            if ':' in line:
                speaker = line.split(':')[0].strip()
                if speaker and not speaker.startswith('[') and len(speaker) < 50:
                    speakers.add(speaker)
        
        return list(speakers)
    
    def _calculate_duration_from_transcript(self, content: str) -> Optional[int]:
        try:
            lines = content.split('\n')
            timestamps = []
            
            for line in lines:
                if '[' in line and ']' in line:
                    timestamp_part = line[line.find('[')+1:line.find(']')]
                    if ':' in timestamp_part:
                        timestamps.append(timestamp_part)
            
            if len(timestamps) >= 2:
                start_time = timestamps[0]
                end_time = timestamps[-1]
                
                start_minutes = self._parse_timestamp_to_minutes(start_time)
                end_minutes = self._parse_timestamp_to_minutes(end_time)
                
                if start_minutes is not None and end_minutes is not None:
                    return max(1, end_minutes - start_minutes)
            
            return None
            
        except Exception:
            return None
    
    def _parse_timestamp_to_minutes(self, timestamp: str) -> Optional[int]:
        try:
            parts = timestamp.split(':')
            if len(parts) >= 2:
                hours = int(parts[0]) if len(parts) > 2 else 0
                minutes = int(parts[-2])
                return hours * 60 + minutes
            return None
        except (ValueError, IndexError):
            return None


graph_client = GraphClientManager()
