from azure.identity import ClientSecretCredential
from typing import Optional, List, Dict, Any
import httpx
import json
from ..config import settings
from .logger import get_logger

logger = get_logger(__name__)

class GraphTranscriptService:
    def __init__(self):
        self.credential = None
        self.base_url = "https://graph.microsoft.com/v1.0"
    
    def _get_credential(self):
        if self.credential is None:
            try:
                self.credential = ClientSecretCredential(
                    tenant_id=settings.microsoft_tenant_id,
                    client_id=settings.microsoft_client_id,
                    client_secret=settings.microsoft_client_secret
                )
            except Exception as e:
                logger.error(f"Microsoft Graph認証情報の初期化エラー: {str(e)}")
                raise Exception(f"Microsoft Graph認証情報が正しく設定されていません: {str(e)}")
        return self.credential
    
    async def get_access_token(self) -> str:
        try:
            credential = self._get_credential()
            token = credential.get_token("https://graph.microsoft.com/.default")
            logger.info("Microsoft Graph アクセストークン取得成功")
            return token.token
        except Exception as e:
            logger.error(f"Microsoft Graph アクセストークン取得エラー: {str(e)}")
            raise Exception(f"認証エラー: {str(e)}")
    
    async def get_online_meetings(self, user_id: str) -> List[Dict[str, Any]]:
        try:
            token = await self.get_access_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}/users/{user_id}/onlineMeetings"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                meetings = data.get("value", [])
                
                logger.info(f"オンライン会議取得成功: {len(meetings)}件")
                return meetings
                
        except Exception as e:
            logger.error(f"オンライン会議取得エラー: {str(e)}")
            raise Exception(f"会議取得エラー: {str(e)}")
    
    async def get_meeting_transcript(self, user_id: str, meeting_id: str) -> Optional[str]:
        try:
            token = await self.get_access_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}/users/{user_id}/onlineMeetings/{meeting_id}/transcripts"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                transcripts = data.get("value", [])
                
                if not transcripts:
                    logger.warning(f"会議 {meeting_id} のトランスクリプトが見つかりません")
                    return None
                
                transcript_id = transcripts[0]["id"]
                content_url = f"{url}/{transcript_id}/content"
                
                content_response = await client.get(content_url, headers=headers)
                content_response.raise_for_status()
                
                transcript_content = content_response.text
                logger.info(f"トランスクリプト取得成功: 会議ID {meeting_id}")
                return transcript_content
                
        except Exception as e:
            logger.error(f"トランスクリプト取得エラー: {str(e)}")
            raise Exception(f"トランスクリプト取得エラー: {str(e)}")
    
    async def get_call_records(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            token = await self.get_access_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}/communications/callRecords"
            params = {
                "$filter": f"organizer/user/id eq '{user_id}'",
                "$top": limit,
                "$orderby": "startDateTime desc"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                call_records = data.get("value", [])
                
                logger.info(f"通話記録取得成功: {len(call_records)}件")
                return call_records
                
        except Exception as e:
            logger.error(f"通話記録取得エラー: {str(e)}")
            raise Exception(f"通話記録取得エラー: {str(e)}")

graph_service = GraphTranscriptService()
