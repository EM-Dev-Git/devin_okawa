from .azure_openai_client import AzureOpenAIClient
from ..schemas.transcript import TranscriptRequest
from ..schemas.minutes import MinutesResponse
import uuid
from datetime import datetime
import logging

class TranscriptProcessor:
    def __init__(self):
        self.openai_client = AzureOpenAIClient()
        self.logger = logging.getLogger(__name__)
    
    async def process_transcript(self, request: TranscriptRequest) -> MinutesResponse:
        """トランスクリプトを処理して議事録を生成"""
        self.logger.info(f"トランスクリプト処理開始: {request.meeting_title}")
        
        try:
            minutes_content = await self.openai_client.generate_minutes(request.content)
            
            response = MinutesResponse(
                id=f"minutes_{uuid.uuid4().hex[:8]}",
                title=request.meeting_title or "議事録",
                content=minutes_content,
                created_at=datetime.utcnow(),
                participants=request.participants
            )
            
            self.logger.info(f"議事録生成完了: {response.id}")
            return response
            
        except Exception as e:
            self.logger.error(f"トランスクリプト処理エラー: {e}")
            raise
