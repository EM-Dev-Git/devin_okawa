# 議事録作成API

トランスクリプトから議事録を自動生成するFastAPIアプリケーション

## 機能

- JWT認証によるユーザー管理
- OpenAI APIを使用した議事録自動生成
- SQLiteデータベースでのデータ永続化
- 構造化されたログ出力
- RESTful API設計

## セットアップ

### 1. 依存関係のインストール

```bash
cd transcript_minutes_api
poetry install
```

### 2. 環境変数の設定

`.env`ファイルを編集して、OpenAI APIキーを設定してください：

```env
OPENAI_API_KEY=your-actual-openai-api-key
```

### 3. データベースの初期化

```bash
poetry run python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### 4. アプリケーションの起動

```bash
poetry run uvicorn app.main:app --reload
```

アプリケーションは `http://localhost:8000` で起動します。

## API ドキュメント

起動後、以下のURLでAPI ドキュメントを確認できます：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API エンドポイント

### 認証関連

- `POST /auth/login` - ログイン
- `POST /auth/refresh` - トークンリフレッシュ
- `POST /auth/logout` - ログアウト

### ユーザー管理

- `POST /users/register` - ユーザー登録
- `GET /users/me` - 現在のユーザー情報取得
- `PUT /users/me` - ユーザー情報更新

### 議事録

- `POST /minutes/generate` - 議事録生成
- `GET /minutes/` - 議事録一覧取得
- `GET /minutes/{id}` - 特定の議事録取得
- `DELETE /minutes/{id}` - 議事録削除

## 使用例

### 1. ユーザー登録

```bash
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "password": "password123",
    "email": "test@example.com"
  }'
```

### 2. ログイン

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "password": "password123"
  }'
```

### 3. 議事録生成

```bash
curl -X POST "http://localhost:8000/minutes/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "transcript": "会議のトランスクリプト内容...",
    "header": {
      "title": "週次進捗会議",
      "date": "2025-07-23",
      "location": "会議室A",
      "participants": ["田中", "佐藤", "鈴木"],
      "facilitator": "田中"
    }
  }'
```

## ディレクトリ構造

```
transcript_minutes_api/
├── app/
│   ├── main.py                 # FastAPIアプリケーション
│   ├── config.py               # 設定管理
│   ├── database.py             # データベース接続
│   ├── models.py               # SQLAlchemyモデル
│   ├── dependencies.py         # 依存関係
│   ├── routers/               # APIルーター
│   │   ├── auth.py            # 認証関連エンドポイント
│   │   ├── minutes.py         # 議事録生成エンドポイント
│   │   └── users.py           # ユーザー管理エンドポイント
│   ├── modules/               # ビジネスロジック
│   │   ├── auth.py            # 認証ロジック
│   │   ├── transcript_processor.py  # トランスクリプト処理
│   │   ├── minutes_formatter.py     # 議事録フォーマット
│   │   └── logger.py          # ログ管理
│   └── schemas/               # Pydanticスキーマ
│       ├── auth.py            # 認証関連スキーマ
│       ├── minutes.py         # 議事録関連スキーマ
│       └── users.py           # ユーザー関連スキーマ
├── logs/                      # ログファイル
├── .env                       # 環境変数
├── pyproject.toml            # 依存関係
└── README.md                 # このファイル
```

## 技術スタック

- **FastAPI**: Webフレームワーク
- **SQLAlchemy**: ORM
- **SQLite**: データベース（開発用）
- **python-jose**: JWT処理
- **passlib**: パスワードハッシュ化
- **OpenAI**: 議事録生成AI
- **Pydantic**: データ検証

## ログ

アプリケーションのログは `logs/app.log` に出力されます。ログレベルは環境変数 `LOG_LEVEL` で設定できます。

## セキュリティ

- パスワードはbcryptでハッシュ化
- JWT トークンによる認証
- 環境変数による機密情報の管理
- CORS設定による適切なアクセス制御
