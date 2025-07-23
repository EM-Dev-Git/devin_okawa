import logging
import logging.handlers
import os
from pathlib import Path
from ..config import settings

class LoggerConfig:
    @staticmethod
    def setup_logging():
        log_dir = Path(settings.log_file_path).parent
        log_dir.mkdir(exist_ok=True)
        
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, settings.log_level.upper()))
        
        if logger.handlers:
            logger.handlers.clear()
        
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler = logging.handlers.RotatingFileHandler(
            settings.log_file_path,
            maxBytes=10*1024*1024,
            backupCount=30
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger

def get_logger(name: str):
    return logging.getLogger(name)
