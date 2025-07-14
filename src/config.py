from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    openai_api_key: Optional[str] = None
    openai_model: str
    openai_max_tokens: int
    openai_temperature: float
    
    app_name: str
    app_version: str
    debug: bool
    log_level: str
    
    host: str
    port: int
    
    class Config:
        env_file = "env/.env"

settings = Settings()
