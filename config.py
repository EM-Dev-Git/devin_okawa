from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_model: str
    azure_openai_version: str
    azure_openai_endpoint: str
    
    class Config:
        env_file = "transcript-minutes-api-001/env/.env"

settings = Settings()
