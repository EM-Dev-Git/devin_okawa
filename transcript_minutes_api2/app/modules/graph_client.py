import asyncio
from typing import List, Optional
from datetime import datetime, timedelta
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from ..config import settings
from ..modules.logger import get_logger

logger = get_logger(__name__)


class GraphClient:
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        try:
            if not all([settings.graph_tenant_id, settings.graph_client_id, settings.graph_client_secret]):
                logger.warning("Microsoft Graph認証情報が設定されていません")
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
            
            logger.info("Microsoft Graph クライアント初期化完了")
            
        except Exception as e:
            logger.error(f"Microsoft Graph クライアント初期化エラー: {str(e)}")
            self.client = None
    
    async def get_meetings(self, days_back: int = 7) -> List[dict]:
        if not self.client:
            raise Exception("Microsoft Graph クライアントが初期化されていません")
        
        try:
            start_time = datetime.now() - timedelta(days=days_back)
            start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            
            logger.info(f"過去{days_back}日間の会議を取得中...")
            
            events = await self.client.me.events.get(
                query_parameters={
                    '$filter': f"start/dateTime ge '{start_time_str}'",
                    '$select': 'id,subject,start,end,organizer',
                    '$orderby': 'start/dateTime desc'
                }
            )
            
            meetings = []
            if events and events.value:
                for event in events.value:
                    if event.subject and 'meeting' in event.subject.lower():
                        meetings.append({
                            'id': event.id,
                            'subject': event.subject,
                            'start_time': event.start.date_time if event.start else None,
                            'end_time': event.end.date_time if event.end else None,
                            'organizer': event.organizer.email_address.name if event.organizer and event.organizer.email_address else 'Unknown'
                        })
            
            logger.info(f"会議取得完了: {len(meetings)}件")
            return meetings
            
        except Exception as e:
            logger.error(f"会議取得エラー: {str(e)}")
            raise Exception(f"会議の取得に失敗しました: {str(e)}")
    
    async def get_meeting_transcript(self, meeting_id: str) -> Optional[dict]:
        if not self.client:
            raise Exception("Microsoft Graph クライアントが初期化されていません")
        
        try:
            logger.info(f"会議のトランスクリプト取得中: {meeting_id}")
            
            call_records = await self.client.communications.call_records.get(
                query_parameters={
                    '$filter': f"id eq '{meeting_id}'",
                    '$expand': 'sessions($expand=segments)'
                }
            )
            
            if not call_records or not call_records.value:
                logger.warning(f"会議記録が見つかりません: {meeting_id}")
                return None
            
            transcript_segments = []
            total_duration = 0
            
            for call_record in call_records.value:
                if call_record.sessions:
                    for session in call_record.sessions:
                        if session.segments:
                            for segment in session.segments:
                                if hasattr(segment, 'media') and segment.media:
                                    for media in segment.media:
                                        if hasattr(media, 'streams'):
                                            for stream in media.streams:
                                                if hasattr(stream, 'audio_codec'):
                                                    transcript_segments.append({
                                                        'speaker': getattr(stream, 'caller_id', 'Unknown'),
                                                        'content': getattr(stream, 'transcript', ''),
                                                        'timestamp': getattr(segment, 'start_date_time', datetime.now())
                                                    })
                                
                                if hasattr(segment, 'duration'):
                                    total_duration += segment.duration
            
            if not transcript_segments:
                logger.warning(f"トランスクリプトが見つかりません: {meeting_id}")
                return {
                    'meeting_id': meeting_id,
                    'meeting_subject': 'Unknown Meeting',
                    'segments': [],
                    'duration_minutes': 0,
                    'transcript_text': 'トランスクリプトが利用できません。'
                }
            
            transcript_text = '\n'.join([
                f"[{segment['timestamp'].strftime('%H:%M:%S')}] {segment['speaker']}: {segment['content']}"
                for segment in transcript_segments
            ])
            
            result = {
                'meeting_id': meeting_id,
                'meeting_subject': call_records.value[0].organizer.user.display_name if call_records.value[0].organizer else 'Unknown Meeting',
                'segments': transcript_segments,
                'duration_minutes': total_duration // 60 if total_duration else 0,
                'transcript_text': transcript_text
            }
            
            logger.info(f"トランスクリプト取得完了: {len(transcript_segments)}セグメント")
            return result
            
        except Exception as e:
            logger.error(f"トランスクリプト取得エラー: {str(e)}")
            return {
                'meeting_id': meeting_id,
                'meeting_subject': 'Error Meeting',
                'segments': [],
                'duration_minutes': 0,
                'transcript_text': f'トランスクリプト取得エラー: {str(e)}'
            }
    
    async def get_meeting_transcripts_list(self, meeting_id: str) -> List[dict]:
        if not self.client:
            raise Exception("Microsoft Graph クライアントが初期化されていません")
        
        try:
            logger.info(f"会議のトランスクリプト一覧取得中: {meeting_id}")
            
            transcripts = await self.client.communications.online_meetings.by_online_meeting_id(meeting_id).transcripts.get()
            
            transcript_list = []
            if transcripts and transcripts.value:
                for transcript in transcripts.value:
                    transcript_list.append({
                        'id': transcript.id,
                        'created_date_time': transcript.created_date_time,
                        'meeting_id': meeting_id,
                        'content_url': getattr(transcript, 'transcript_content_url', None)
                    })
            
            logger.info(f"トランスクリプト一覧取得完了: {len(transcript_list)}件")
            return transcript_list
            
        except Exception as e:
            logger.error(f"トランスクリプト一覧取得エラー: {str(e)}")
            raise Exception(f"トランスクリプト一覧の取得に失敗しました: {str(e)}")


graph_client = GraphClient()
