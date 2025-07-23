# Meeting Minutes API

トランスクリプトから議事録を自動生成するFastAPI アプリケーション

## 機能

- **JWT認証**: セキュアなユーザー認証システム
- **ユーザー管理**: ユーザー登録・ログイン・プロフィール管理
- **議事録生成**: OpenAI GPT-4を使用したトランスクリプト解析・議事録生成
- **データベース管理**: SQLiteを使用したデータ永続化
- **ログ機能**: 包括的なログ記録とローテーション
- **環境変数管理**: セキュアな設定管理

## 技術スタック

- **FastAPI**: 高性能なWebフレームワーク
- **SQLAlchemy**: ORM
- **OpenAI API**: GPT-4による自然言語処理
- **JWT**: セキュアな認証
- **SQLite**: データベース（開発環境）

## セットアップ

### 1. 依存関係のインストール

```bash
cd transcript_minutes_api
poetry install
```

### 2. 環境変数の設定

`.env` ファイルを編集して必要な設定を行ってください：

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# JWT Configuration
SECRET_KEY=your_super_secret_jwt_key_here_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=sqlite:///./meeting_minutes.db

# Logging Configuration
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

## API エンドポイント

### 認証

- `POST /auth/register` - ユーザー登録
- `POST /auth/login` - ログイン

### ユーザー管理

- `GET /users/me` - 現在のユーザー情報取得
- `PUT /users/me` - ユーザー情報更新
- `DELETE /users/me` - ユーザー削除

### 議事録

- `POST /minutes/generate` - トランスクリプトから議事録生成
- `GET /minutes/` - ユーザーの議事録一覧
- `GET /minutes/{id}` - 特定の議事録取得
- `DELETE /minutes/{id}` - 議事録削除

### その他

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
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
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

## ディレクトリ構成

```
transcript_minutes_api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPIアプリケーション
│   ├── config.py              # 設定管理
│   ├── database.py            # データベース接続
│   ├── models.py              # SQLAlchemyモデル
│   ├── dependencies.py        # 依存性注入
│   ├── routers/               # APIルーター
│   │   ├── __init__.py
│   │   ├── auth.py           # 認証エンドポイント
│   │   ├── users.py          # ユーザー管理
│   │   └── minutes.py        # 議事録生成
│   ├── schemas/               # Pydanticスキーマ
│   │   ├── __init__.py
│   │   ├── auth.py           # 認証スキーマ
│   │   ├── users.py          # ユーザースキーマ
│   │   └── minutes.py        # 議事録スキーマ
│   └── modules/               # ビジネスロジック
│       ├── __init__.py
│       ├── auth.py           # 認証処理
│       ├── transcript_processor.py  # トランスクリプト処理
│       ├── minutes_formatter.py     # 議事録フォーマット
│       └── logger.py         # ログ設定
├── logs/                      # ログファイル
├── .env                       # 環境変数
├── pyproject.toml            # Poetry設定
└── README.md                 # このファイル
```

## 開発

### API ドキュメント

サーバー起動後、以下のURLでAPI ドキュメントを確認できます：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### ログ

アプリケーションのログは以下に出力されます：

- コンソール出力
- ファイル出力: `logs/app.log`

### セキュリティ

- パスワードはbcryptでハッシュ化
- JWT トークンによる認証
- CORS設定済み

## ライセンス

MIT License
