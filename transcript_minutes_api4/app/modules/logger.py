import logging
import logging.handlers
import os
from pathlib import Path
from ..config import settings


class LoggerConfig:
    @staticmethod
    def setup_logging():
        log_dir = Path(settings.log_file_path).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, settings.log_level.upper()),
            format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.StreamHandler(),
                logging.handlers.RotatingFileHandler(
                    settings.log_file_path,
                    maxBytes=settings.log_max_size,
                    backupCount=settings.log_backup_count,
                    encoding='utf-8'
                )
            ]
        )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
