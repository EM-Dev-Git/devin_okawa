from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    openai_api_key: Optional[str] = None
    openai_model: str
    openai_max_tokens: Optional[int] = None
    openai_temperature: float
    openai_timeout: int = 60
    
    azure_openai_endpoint: str
    azure_openai_api_version: str
    
    app_name: str
    app_version: str
    debug: bool
    log_level: str
    
    host: str
    port: int
    
    def is_azure_openai_configured(self) -> bool:
        """Check if Azure OpenAI is properly configured with real values"""
        placeholder_keys = [
            "your_azure_openai_api_key_here",
            "your_openai_api_key_here", 
            "your_actual_openai_api_key_here"
        ]
        placeholder_endpoints = [
            "https://your-resource.openai.azure.com/",
            "your-resource.openai.azure.com"
        ]
        
        return (
            self.openai_api_key and 
            self.openai_api_key not in placeholder_keys and
            self.azure_openai_endpoint and 
            self.azure_openai_endpoint not in placeholder_endpoints
        )
    
    class Config:
        env_file = "env/.env"

settings = Settings()
