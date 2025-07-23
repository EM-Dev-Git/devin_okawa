from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 30
    openai_api_key: str
    microsoft_client_id: str
    microsoft_client_secret: str
    microsoft_tenant_id: str
    log_level: str = "INFO"
    log_file_path: str = "logs/app.log"
    debug: bool = False
    cors_origins: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
