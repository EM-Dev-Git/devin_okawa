# Meeting Minutes API v4

トランスクリプトから議事録を自動生成するFastAPI（Microsoft Graph SDK統合版）

## 機能

- **JWT認証**: ユーザー登録・ログイン機能
- **議事録生成**: OpenAI GPT-4を使用したトランスクリプト解析
- **Microsoft Graph統合**: Teams会議のトランスクリプト取得
- **データベース**: SQLiteによるユーザー・議事録管理
- **ログ機能**: ファイルローテーション付きログ
- **環境変数**: 設定の外部化

## セットアップ

### 1. 依存関係のインストール

```bash
cd transcript_minutes_api4
poetry install
```

### 2. 環境変数の設定

`.env`ファイルを編集して以下を設定：

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Microsoft Graph Configuration
MICROSOFT_CLIENT_ID=your_client_id_here
MICROSOFT_CLIENT_SECRET=your_client_secret_here
MICROSOFT_TENANT_ID=your_tenant_id_here

# JWT Configuration
SECRET_KEY=your_super_secret_jwt_key_here_change_this_in_production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=sqlite:///./meeting_minutes.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE_PATH=./logs/app.log
```

### 3. Microsoft Graph API設定

Azure ADでアプリケーションを登録し、以下の権限を設定：

- `OnlineMeetings.Read`
- `CallRecords.Read.All`
- `User.Read`

### 4. サーバー起動

```bash
poetry run uvicorn app.main:app --reload
```

## API エンドポイント

### 認証

- `POST /auth/register` - ユーザー登録
- `POST /auth/login` - ログイン（JWTトークン取得）

### ユーザー管理

- `GET /users/me` - 現在のユーザー情報取得
- `PUT /users/me` - ユーザー情報更新
- `GET /users/` - 全ユーザー一覧

### 議事録生成

- `POST /minutes/generate` - トランスクリプトから議事録生成
- `GET /minutes/` - ユーザーの議事録一覧
- `GET /minutes/{id}` - 特定の議事録取得
- `DELETE /minutes/{id}` - 議事録削除

### Microsoft Graph

- `POST /graph/meetings` - Teams会議一覧取得
- `POST /graph/meeting-transcripts` - 会議のトランスクリプト一覧取得
- `POST /graph/transcript` - 会議トランスクリプト取得
- `POST /graph/call-records` - 通話記録取得
- `POST /graph/transcript-to-minutes` - Graphトランスクリプトから議事録生成

## 使用例

### 1. ユーザー登録

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. ログイン

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

### 3. 議事録生成

```bash
curl -X POST "http://localhost:8000/minutes/generate" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "会議のトランスクリプト内容...",
    "header": {
      "title": "週次進捗会議",
      "date": "2025-01-23",
      "location": "会議室A",
      "participants": ["田中", "佐藤", "鈴木"],
      "facilitator": "田中"
    }
  }'
```

### 4. Teams会議一覧取得

```bash
curl -X POST "http://localhost:8000/graph/meetings" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user@company.com"
  }'
```

### 5. 会議のトランスクリプト一覧取得

```bash
curl -X POST "http://localhost:8000/graph/meeting-transcripts" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "meeting_id": "meeting_id_here"
  }'
```

## 技術スタック

- **FastAPI**: Webフレームワーク
- **SQLAlchemy**: ORM
- **SQLite**: データベース
- **OpenAI**: GPT-4による議事録生成
- **Microsoft Graph SDK**: Teams統合
- **JWT**: 認証
- **Poetry**: 依存関係管理

## ディレクトリ構成

```
transcript_minutes_api4/
├── app/
│   ├── routers/          # APIルーター
│   ├── modules/          # ビジネスロジック
│   ├── schemas/          # Pydanticモデル
│   ├── config.py         # 設定
│   ├── database.py       # データベース設定
│   ├── models.py         # SQLAlchemyモデル
│   ├── dependencies.py   # 依存関係
│   └── main.py          # FastAPIアプリケーション
├── logs/                # ログファイル
├── .env                 # 環境変数
├── pyproject.toml       # Poetry設定
└── README.md           # このファイル
```

## 開発

### テスト実行

```bash
poetry run pytest
```

### コードフォーマット

```bash
poetry run black app/
poetry run isort app/
```

### リント

```bash
poetry run flake8 app/
```

## ライセンス

MIT License
