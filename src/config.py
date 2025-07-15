from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_model: str
    azure_openai_version: str
    azure_openai_endpoint: str
    
    class Config:
        env_file = "env/.env"

settings = Settings()
