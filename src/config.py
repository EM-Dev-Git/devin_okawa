from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_model: str
    azure_openai_version: str
    azure_openai_endpoint: str
    
    oauth2_secret_key: str = "your-secret-key-here-change-in-production"
    oauth2_algorithm: str = "HS256"
    oauth2_access_token_expire_minutes: int = 30
    
    class Config:
        env_file = "env/.env"

settings = Settings()
