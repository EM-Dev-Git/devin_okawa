import openai
import logging
from src.config import settings
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        placeholder_keys = [
            "your_azure_openai_api_key_here",
            "your_openai_api_key_here", 
            "your_actual_openai_api_key_here"
        ]
        placeholder_endpoints = [
            "https://your-resource.openai.azure.com/",
            "your-resource.openai.azure.com"
        ]
        
        if not settings.openai_api_key or settings.openai_api_key in placeholder_keys:
            self.client = None
            logger.warning("Azure OpenAI API key not configured or using placeholder - fallback mode will be used")
        elif not settings.azure_openai_endpoint or settings.azure_openai_endpoint in placeholder_endpoints:
            self.client = None
            logger.warning("Azure OpenAI endpoint not configured or using placeholder - fallback mode will be used")
        else:
            try:
                self.client = openai.AzureOpenAI(
                    api_key=settings.openai_api_key,
                    azure_endpoint=settings.azure_openai_endpoint,
                    api_version=settings.azure_openai_api_version,
                    timeout=settings.openai_timeout
                )
                logger.info("Azure OpenAI client initialized successfully")
            except Exception as e:
                self.client = None
                logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
        
    def generate_minutes(self, prompt: str) -> str:
        if not self.client:
            raise ValueError("Azure OpenAI client not configured")
            
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
            
            logger.info("Azure OpenAI API call successful")
            return response.choices[0].message.content
            
        except openai.AuthenticationError as e:
            logger.error(f"Azure OpenAI API authentication failed: {str(e)}")
            raise ValueError("Azure OpenAI API key is invalid or not configured")
        except openai.RateLimitError as e:
            logger.error(f"Azure OpenAI API rate limit exceeded: {str(e)}")
            raise
        except openai.APITimeoutError as e:
            logger.error(f"Azure OpenAI API timeout after {settings.openai_timeout}s: {str(e)}")
            raise
        except openai.APIError as e:
            logger.error(f"Azure OpenAI API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in Azure OpenAI API call: {str(e)}")
            raise
