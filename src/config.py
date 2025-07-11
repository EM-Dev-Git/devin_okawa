from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    openai_max_tokens: int = 2000
    openai_temperature: float = 0.7
    
    app_name: str = "Meeting Minutes Generator"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = "../env/.env"

settings = Settings()
