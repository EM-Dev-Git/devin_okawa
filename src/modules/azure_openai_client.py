from openai import AzureOpenAI
from src.config import settings
import logging

class AzureOpenAIClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_version,
            azure_endpoint=settings.azure_openai_endpoint
        )
        self.model = settings.azure_openai_model
        self.logger = logging.getLogger(__name__)
    
    async def generate_minutes(self, transcript: str) -> str:
        """トランスクリプトから議事録を生成"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "あなたは議事録作成の専門家です。"},
                    {"role": "user", "content": f"以下のトランスクリプトから議事録を作成してください:\n{transcript}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"議事録生成エラー: {e}")
            raise
