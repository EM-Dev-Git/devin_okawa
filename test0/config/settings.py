import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    AI_MODEL = os.getenv("AI_MODEL", "gpt-4")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
    
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_EXTENSIONS = ["txt", "md"]
    
    OUTPUT_FORMATS = ["html", "markdown", "pdf"]
    DEFAULT_OUTPUT_FORMAT = "html"

settings = Settings()
