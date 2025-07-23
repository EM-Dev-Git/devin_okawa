from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    openai_api_key: str
    microsoft_client_id: str
    microsoft_client_secret: str
    microsoft_tenant_id: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///./meeting_minutes.db"
    log_level: str = "INFO"
    log_file_path: str = "./logs/app.log"
    log_max_size: int = 10485760
    log_backup_count: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
