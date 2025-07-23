import logging
import logging.handlers
import os
from ..config import settings


def setup_logger():
    os.makedirs(os.path.dirname(settings.log_file_path), exist_ok=True)
    
    logger = logging.getLogger("transcript_minutes_api2")
    logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    file_handler = logging.handlers.RotatingFileHandler(
        settings.log_file_path,
        maxBytes=settings.log_max_size,
        backupCount=settings.log_backup_count
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str):
    setup_logger()
    return logging.getLogger(f"transcript_minutes_api2.{name}")
