from pydantic_settings import BaseSettings
from typing import Optional
import os
import sys

def validate_required_env_vars():
    """必須環境変数の存在確認とエラーハンドリング"""
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT", 
        "JWT_SECRET_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing required environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file with the required variables.")
        print("You can copy .env.example to .env and modify the values:")
        print("  cp .env.example .env")
        print("\nUsing development defaults for missing variables...")
        return False
    
    return True

class Settings(BaseSettings):
    azure_openai_api_key: str = "test_key_for_development"
    azure_openai_endpoint: str = "https://test.openai.azure.com/"
    jwt_secret_key: str = "test_secret_key_for_development_only_change_in_production"
    
    azure_openai_model: str = "gpt-4"
    azure_openai_version: str = "2024-02-15-preview"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    app_name: str = "Meeting Minutes Generator"
    app_version: str = "1.0.0"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = ""
        case_sensitive = False
        extra = "ignore"

env_vars_ok = validate_required_env_vars()

settings = Settings()

if __name__ != "__main__":  # モジュールとしてインポートされた場合のみ
    import logging
    logger = logging.getLogger(__name__)
    
    if env_vars_ok:
        logger.info("All required environment variables loaded successfully")
    else:
        logger.warning("Some environment variables missing, using development defaults")
