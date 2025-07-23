# Transcript Minutes API

トランスクリプトから議事録を自動生成するFastAPI アプリケーション

## 機能

- **JWT認証**: セキュアなユーザー認証システム
- **OpenAI統合**: GPT-4を使用したトランスクリプト解析と議事録生成
- **データベース管理**: SQLiteを使用したユーザーと議事録データの管理
- **ログ機能**: 包括的なログ記録とファイルローテーション
- **環境変数管理**: セキュアな設定管理

## セットアップ

### 1. 依存関係のインストール

```bash
poetry install
```

### 2. 環境変数の設定

`.env` ファイルを編集して、必要なAPIキーと設定を追加してください：

```bash
# OpenAI設定
OPENAI_API_KEY=your_openai_api_key_here

# JWT設定
SECRET_KEY=your_super_secret_jwt_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# データベース設定
DATABASE_URL=sqlite:///./meeting_minutes.db

# ログ設定
LOG_LEVEL=INFO
LOG_FILE_PATH=./logs/app.log
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5
```

### 3. サーバーの起動

```bash
poetry run uvicorn app.main:app --reload
```

サーバーは `http://localhost:8000` で起動します。

## API ドキュメント

サーバー起動後、以下のURLでAPI ドキュメントを確認できます：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API エンドポイント

### 認証
- `POST /auth/register` - ユーザー登録
- `POST /auth/login` - ログイン（JWTトークン発行）

### ユーザー管理
- `GET /users/me` - 現在のユーザー情報取得
- `PUT /users/me` - ユーザー情報更新
- `DELETE /users/me` - ユーザー削除

### 議事録生成
- `POST /minutes/generate` - トランスクリプトから議事録生成
- `GET /minutes/` - ユーザーの議事録一覧取得
- `GET /minutes/{id}` - 特定の議事録取得
- `DELETE /minutes/{id}` - 議事録削除

### ヘルスチェック
- `GET /` - ルートエンドポイント
- `GET /health` - ヘルスチェック

## 使用例

### 1. ユーザー登録

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

### 2. ログイン

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword123"
  }'
```

### 3. 議事録生成

```bash
curl -X POST "http://localhost:8000/minutes/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "transcript": "会議のトランスクリプトテキスト...",
    "header": {
      "title": "週次進捗会議",
      "date": "2025-07-23",
      "location": "会議室A",
      "participants": ["田中", "佐藤", "鈴木"],
      "facilitator": "田中"
    }
  }'
```

## 技術スタック

- **FastAPI**: Webフレームワーク
- **SQLAlchemy**: ORM
- **Pydantic**: データバリデーション
- **python-jose**: JWT認証
- **passlib**: パスワードハッシュ化
- **OpenAI**: GPT-4 API
- **SQLite**: データベース（開発環境）

## ログ

アプリケーションログは以下の場所に保存されます：
- コンソール出力（開発時）
- ファイル出力: `./logs/app.log`
- ローテーション: 10MB、5ファイル保持

## セキュリティ

- bcryptによるパスワードハッシュ化
- JWT トークンベース認証
- CORS設定
- 環境変数による機密情報管理

## 開発

### テスト実行

```bash
poetry run pytest
```

### コード品質チェック

```bash
poetry run black .
poetry run isort .
poetry run flake8 .
```

## ライセンス

MIT License
