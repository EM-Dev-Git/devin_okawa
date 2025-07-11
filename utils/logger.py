# 共通ログ機能モジュール
# FastAPIアプリケーション全体で使用する統一されたログ設定を提供

import logging
import sys
from typing import Optional
from config import settings


class LoggerConfig:
    
    _configured = False  # ログ設定済みフラグ（重複設定防止用）
    
    @classmethod
    def setup_logging(
        cls,
        level: Optional[int] = None,
        format_string: Optional[str] = None,
        include_timestamp: bool = True
    ) -> None:
        # アプリケーション全体のログ設定を初期化
        # level: ログレベル（デフォルト: 設定ファイルから取得）
        # format_string: カスタムフォーマット文字列
        # include_timestamp: タイムスタンプを含めるかどうか
        if cls._configured:
            return
            
        if level is None:
            level = getattr(logging, settings.log_level.upper(), logging.INFO)
            
        if format_string is None:
            format_string = settings.log_format
        
        logging.basicConfig(
            level=level,
            format=format_string,
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        cls._configured = True


def get_logger(name: str) -> logging.Logger:
    # 指定された名前のロガーインスタンスを取得
    # name: ロガー名（通常は __name__ を使用）
    # 戻り値: 設定済みのロガーインスタンス
    if not LoggerConfig._configured:
        LoggerConfig.setup_logging()
    
    return logging.getLogger(name)


def get_app_logger() -> logging.Logger:
    # アプリケーションメインのロガーを取得
    # 戻り値: アプリケーション用ロガー
    return get_logger("fastapi_app")


def get_router_logger(router_name: str) -> logging.Logger:
    # ルーター用のロガーを取得
    # router_name: ルーター名
    # 戻り値: ルーター用ロガー
    return get_logger(f"fastapi_app.routers.{router_name}")
