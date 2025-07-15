from openai import AzureOpenAI
import logging
from typing import Optional
import json

logger = logging.getLogger(__name__)

class AzureOpenAIClient:
    def __init__(self, 
                 azure_openai_api_key: str,
                 azure_openai_endpoint: str, 
                 azure_openai_model: str,
                 azure_openai_version: str):
        self.azure_openai_api_key = azure_openai_api_key
        self.azure_openai_endpoint = azure_openai_endpoint
        self.azure_openai_model = azure_openai_model
        self.azure_openai_version = azure_openai_version
        
        if not all([self.azure_openai_api_key, self.azure_openai_endpoint, self.azure_openai_model, self.azure_openai_version]):
            raise ValueError("Missing required Azure OpenAI configuration parameters")
        
        try:
            self.client = AzureOpenAI(
                api_key=self.azure_openai_api_key,
                api_version=self.azure_openai_version,
                azure_endpoint=self.azure_openai_endpoint
            )
            logger.info("Azure OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
            raise
        
    def generate_minutes(self, prompt: str) -> str:
        try:
            logger.info("Starting Azure OpenAI API call for minutes generation")
            
            response = self.client.chat.completions.create(
                model=self.azure_openai_model,
                messages=[
                    {"role": "system", "content": "You are an expert meeting minutes generator. Generate structured meeting minutes in JSON format based on the provided transcript."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            logger.info("Azure OpenAI API call completed successfully")
            return content
            
        except Exception as e:
            logger.error(f"Azure OpenAI API call failed: {str(e)}")
            raise
