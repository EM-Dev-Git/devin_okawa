from azure.identity import ClientSecretCredential
import httpx
import json
from typing import Dict, Any, List, Optional
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
            logger.info(f"ユーザー {user_id} のオンライン会議取得開始")
            
            access_token = await self.get_access_token()
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/users/{user_id}/onlineMeetings",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"オンライン会議取得成功: {len(data.get('value', []))}件")
                    return data.get('value', [])
                else:
                    logger.error(f"オンライン会議取得エラー: {response.status_code} - {response.text}")
                    raise Exception(f"Graph API エラー: {response.status_code}")

        except Exception as e:
            logger.error(f"オンライン会議取得エラー: {str(e)}")
            raise Exception(f"会議取得エラー: {str(e)}")

    async def get_meeting_transcript(self, meeting_id: str, transcript_id: str) -> Dict[str, Any]:
        try:
            logger.info(f"会議 {meeting_id} のトランスクリプト {transcript_id} 取得開始")
            
            access_token = await self.get_access_token()
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/communications/onlineMeetings/{meeting_id}/transcripts/{transcript_id}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    transcript_metadata = response.json()
                    
                    content_response = await client.get(
                        f"{self.base_url}/communications/onlineMeetings/{meeting_id}/transcripts/{transcript_id}/content",
                        headers=headers
                    )
                    
                    if content_response.status_code == 200:
                        transcript_content = content_response.text
                        
                        result = {
                            "metadata": transcript_metadata,
                            "content": transcript_content
                        }
                        
                        logger.info("トランスクリプト取得成功")
                        return result
                    else:
                        logger.error(f"トランスクリプト内容取得エラー: {content_response.status_code}")
                        raise Exception(f"トランスクリプト内容取得エラー: {content_response.status_code}")
                else:
                    logger.error(f"トランスクリプトメタデータ取得エラー: {response.status_code}")
                    raise Exception(f"トランスクリプトメタデータ取得エラー: {response.status_code}")

        except Exception as e:
            logger.error(f"トランスクリプト取得エラー: {str(e)}")
            raise Exception(f"トランスクリプト取得エラー: {str(e)}")

    async def get_call_records(self, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        try:
            logger.info(f"通話記録取得開始: {from_date} - {to_date}")
            
            access_token = await self.get_access_token()
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            filter_query = f"startDateTime ge {from_date} and startDateTime le {to_date}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/communications/callRecords",
                    headers=headers,
                    params={"$filter": filter_query}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"通話記録取得成功: {len(data.get('value', []))}件")
                    return data.get('value', [])
                else:
                    logger.error(f"通話記録取得エラー: {response.status_code} - {response.text}")
                    raise Exception(f"通話記録取得エラー: {response.status_code}")

        except Exception as e:
            logger.error(f"通話記録取得エラー: {str(e)}")
            raise Exception(f"通話記録取得エラー: {str(e)}")


    async def get_meeting_transcripts_list(self, meeting_id: str) -> List[Dict[str, Any]]:
        try:
            logger.info(f"会議 {meeting_id} のトランスクリプト一覧取得開始")
            
            access_token = await self.get_access_token()
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/communications/onlineMeetings/{meeting_id}/transcripts",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"トランスクリプト一覧取得成功: {len(data.get('value', []))}件")
                    return data.get('value', [])
                else:
                    logger.error(f"トランスクリプト一覧取得エラー: {response.status_code} - {response.text}")
                    raise Exception(f"Graph API エラー: {response.status_code}")

        except Exception as e:
            logger.error(f"トランスクリプト一覧取得エラー: {str(e)}")
            raise Exception(f"トランスクリプト一覧取得エラー: {str(e)}")


graph_service = GraphTranscriptService()
