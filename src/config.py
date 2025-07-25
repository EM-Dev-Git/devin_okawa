from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_model: str
    azure_openai_version: str
    azure_openai_endpoint: str
    
    jwt_secret_key: str = "test_secret_key_for_development_only_change_in_production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    jwt_refresh_expire_days: int = 7
    jwt_remember_me_expire_days: int = 30
    
    class Config:
        env_file = "env/.env"

settings = Settings()
