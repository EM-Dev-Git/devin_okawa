from openai import AzureOpenAI
from typing import Optional
import logging
from src.config import settings

logger = logging.getLogger(__name__)

class AzureOpenAIClient:
    def __init__(self, 
                 azure_openai_api_key: Optional[str] = None,
                 azure_openai_endpoint: Optional[str] = None,
                 azure_openai_model: Optional[str] = None,
                 azure_openai_version: Optional[str] = None):
        
        self.azure_openai_api_key = azure_openai_api_key or settings.azure_openai_api_key
        self.azure_openai_endpoint = azure_openai_endpoint or settings.azure_openai_endpoint
        self.azure_openai_model = azure_openai_model or settings.azure_openai_model
        self.azure_openai_version = azure_openai_version or settings.azure_openai_version
        
        if not all([self.azure_openai_api_key, self.azure_openai_endpoint, self.azure_openai_model]):
            raise ValueError("Azure OpenAI configuration is incomplete")
        
        self.client = AzureOpenAI(
            api_key=self.azure_openai_api_key,
            api_version=self.azure_openai_version,
            azure_endpoint=self.azure_openai_endpoint
        )
    
    def generate_minutes(self, prompt: str) -> str:
        """Azure OpenAI APIを使用して議事録を生成"""
        try:
            logger.info("Generating minutes using Azure OpenAI")
            
            response = self.client.chat.completions.create(
                model=self.azure_openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは会議の議事録を作成する専門家です。提供されたトランスクリプトから、構造化された議事録を作成してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            logger.info("Successfully generated minutes")
            return content
            
        except Exception as e:
            logger.error(f"Error generating minutes: {str(e)}")
            raise
