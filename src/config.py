from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import field_validator

class Settings(BaseSettings):
    openai_api_key: Optional[str] = None
    openai_model: str
    openai_max_tokens: Optional[int] = None
    openai_temperature: float
    openai_timeout: int = 60
    
    app_name: str
    app_version: str
    debug: bool
    log_level: str
    
    host: str
    port: int
    
    @field_validator('openai_max_tokens', mode='before')
    @classmethod
    def validate_max_tokens(cls, v):
        if v == '' or v is None:
            return None
        return int(v)
    
    class Config:
        env_file = "env/.env"

settings = Settings()
