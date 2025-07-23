from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    openai_api_key: str
    microsoft_client_id: str
    microsoft_client_secret: str
    microsoft_tenant_id: str
    database_url: str = "sqlite:///./meeting_minutes.db"
    secret_key: str
    access_token_expire_minutes: int = 30
    log_level: str = "INFO"
    log_file_path: str = "./logs/app.log"

    class Config:
        env_file = ".env"


settings = Settings()
