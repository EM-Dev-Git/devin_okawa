


from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    
    app_name: str = "FastAPI Basic Application"  # アプリケーション名
    app_version: str = "1.0.0"  # バージョン番号
    app_description: str = "A basic FastAPI application with modular structure"  # アプリケーション説明
    debug: bool = True  # デバッグモードフラグ
    environment: str = "development"  # 実行環境（development/production）
    
    host: str = "127.0.0.1"  # サーバーホストアドレス
    port: int = 8000  # サーバーポート番号
    reload: bool = True  # ホットリロード有効フラグ
    
    secret_key: str = "dev-secret-key-change-in-production"  # JWT署名用秘密鍵
    access_token_expire_minutes: int = 30  # アクセストークン有効期限（分）
    
    database_url: str = "sqlite:///./app.db"  # データベース接続URL
    
    log_level: str = "INFO"  # ログレベル
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # ログフォーマット
    
    cors_origins: str = "http://localhost:3000,http://localhost:8080,http://127.0.0.1:3000,http://127.0.0.1:8080"  # 許可オリジン
    cors_allow_credentials: bool = True  # 認証情報送信許可フラグ
    cors_allow_methods: str = "GET,POST,PUT,DELETE,OPTIONS"  # 許可HTTPメソッド
    cors_allow_headers: str = "*"  # 許可HTTPヘッダー
    
    max_file_size: int = 10485760  # 最大ファイルサイズ（10MB）
    upload_dir: str = "./uploads"  # アップロードディレクトリ
    
    openai_api_key: str = "your-openai-api-key-here"  # OpenAI APIキー
    openai_model: str = "gpt-4"  # OpenAI使用モデル
    openai_max_tokens: int = 2000  # OpenAI最大トークン数
    openai_temperature: float = 0.7  # OpenAI生成温度（0.0-2.0）
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = "env/.env"  # 環境変数ファイルパス
        env_file_encoding = "utf-8"  # ファイルエンコーディング
        case_sensitive = False  # 環境変数名の大文字小文字区別なし


settings = Settings()
