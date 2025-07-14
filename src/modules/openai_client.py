import openai
import logging
from src.config import settings
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        if not settings.openai_api_key or settings.openai_api_key == "your_actual_openai_api_key_here" or settings.openai_api_key == "your_openai_api_key_here":
            self.client = None
            logger.warning("OpenAI API key not configured or using placeholder - fallback mode will be used")
        else:
            self.client = openai.OpenAI(
                api_key=settings.openai_api_key,
                timeout=settings.openai_timeout
            )
        
    def generate_minutes(self, prompt: str) -> str:
        if not self.client:
            raise ValueError("OpenAI client not configured")
            
        try:
            api_params = {
                "model": settings.openai_model,
                "messages": [
                    {
                        "role": "system",
                        "content": "あなたは会議の議事録作成の専門家です。与えられたトランスクリプトから、指定されたフォーマットに従って詳細な議事録を作成してください。"
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "temperature": settings.openai_temperature
            }
            
            if settings.openai_max_tokens is not None:
                api_params["max_tokens"] = settings.openai_max_tokens
                
            response = self.client.chat.completions.create(**api_params)
            
            logger.info("OpenAI API call successful")
            return response.choices[0].message.content
            
        except openai.AuthenticationError as e:
            logger.error(f"OpenAI API authentication failed: {str(e)}")
            raise ValueError("OpenAI API key is invalid or not configured")
        except openai.RateLimitError as e:
            logger.error(f"OpenAI API rate limit exceeded: {str(e)}")
            raise
        except openai.APITimeoutError as e:
            logger.error(f"OpenAI API timeout after {settings.openai_timeout}s: {str(e)}")
            raise
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI API call: {str(e)}")
            raise
