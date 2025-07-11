import logging
import sys
from typing import Optional
from config import settings


class LoggerConfig:
    
    @staticmethod
    def setup_logging():
        # アプリケーション全体のログ設定を初期化
        logging.basicConfig(
            level=getattr(logging, settings.log_level.upper()),  # ログレベル設定
            format=settings.log_format,  # ログフォーマット設定
            handlers=[
                logging.StreamHandler(sys.stdout)  # 標準出力へのハンドラー
            ]
        )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def get_app_logger() -> logging.Logger:
    return get_logger("fastapi_app")


def get_router_logger(router_name: str) -> logging.Logger:
    return get_logger(f"fastapi_app.routers.{router_name}")


def get_module_logger(module_name: str) -> logging.Logger:
    return get_logger(f"fastapi_app.modules.{module_name}")
