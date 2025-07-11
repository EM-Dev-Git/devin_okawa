"""
Configuration settings for FastAPI application
Loads environment variables from .env file
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    app_name: str = "FastAPI Basic Application"
    app_version: str = "1.0.0"
    app_description: str = "A basic FastAPI application with modular structure"
    debug: bool = True
    environment: str = "development"
    
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True
    
    secret_key: str = "dev-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    database_url: str = "sqlite:///./app.db"
    
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    cors_origins: str = "http://localhost:3000,http://localhost:8080,http://127.0.0.1:3000,http://127.0.0.1:8080"
    cors_allow_credentials: bool = True
    cors_allow_methods: str = "GET,POST,PUT,DELETE,OPTIONS"
    cors_allow_headers: str = "*"
    
    max_file_size: int = 10485760  # 10MB
    upload_dir: str = "./uploads"
    
    openai_api_key: str = "your-openai-api-key-here"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS origins string to list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = "env/.env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
