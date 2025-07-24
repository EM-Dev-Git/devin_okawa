import logging
import logging.handlers
import os
from ..config import settings


def setup_logger():
    log_dir = os.path.dirname(settings.log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.log_level.upper()))

    if logger.handlers:
        logger.handlers.clear()

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


def get_logger(name: str):
    return logging.getLogger(name)
