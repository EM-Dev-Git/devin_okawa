from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    azure_openai_api_key: str = "test_key_for_development"
    azure_openai_endpoint: str = "https://test.openai.azure.com/"
    azure_openai_model: str = "gpt-4"
    azure_openai_version: str = "2024-02-15-preview"
    
    jwt_secret_key: str = "test_secret_key_for_development_only_change_in_production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    app_name: str = "Meeting Minutes Generator"
    app_version: str = "1.0.0"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
