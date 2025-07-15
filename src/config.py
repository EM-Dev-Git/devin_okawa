from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_model: str
    azure_openai_version: str
    azure_openai_endpoint: str
    
    session_secret_key: str
    session_expire_hours: int = 24
    
    auth_excluded_paths: str = "/api/v1/auth/login,/api/v1/auth/register,/api/v1/auth/logout,/login,/health"
    
    @property
    def excluded_paths_list(self) -> List[str]:
        return [path.strip() for path in self.auth_excluded_paths.split(",")]
    
    class Config:
        env_file = "env/.env"

settings = Settings()
