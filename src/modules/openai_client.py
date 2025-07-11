import openai
import logging
from src.config import settings
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        if settings.openai_api_key:
            self.client = openai.OpenAI(api_key=settings.openai_api_key)
        else:
            self.client = None
            logger.warning("OpenAI API key not configured - fallback mode will be used")
        
    def generate_minutes(self, prompt: str) -> str:
        if not self.client:
            raise ValueError("OpenAI API key not configured")
            
        try:
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは会議の議事録作成の専門家です。"
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=settings.openai_max_tokens,
                temperature=settings.openai_temperature
            )
            
            logger.info("OpenAI API call successful")
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
