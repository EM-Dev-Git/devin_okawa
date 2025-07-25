# API使用ガイド

## 概要
このAPIは議事録生成システムで、OAuth2認証を使用してセキュアなアクセスを提供します。

## 基本URL
```
http://localhost:8000
```

## 認証フロー

### 1. ユーザー登録
新しいユーザーアカウントを作成します。

**エンドポイント:** `POST /auth/register`

**リクエスト例:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepassword123"
}
```

**レスポンス例:**
```json
{
  "id": "user_12345",
  "username": "testuser",
  "email": "test@example.com",
  "is_active": true,
  "created_at": "2025-01-25T10:30:00Z",
  "updated_at": "2025-01-25T10:30:00Z"
}
```

### 2. ログイン
ユーザー認証を行い、アクセストークンとリフレッシュトークンを取得します。

**エンドポイント:** `POST /auth/login`

**リクエスト例（通常ログイン）:**
```json
{
  "username": "testuser",
  "password": "securepassword123",
  "remember_me": false
}
```

**リクエスト例（Remember Me有効）:**
```json
{
  "username": "testuser",
  "password": "securepassword123",
  "remember_me": true
}
```

**レスポンス例:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. トークンリフレッシュ
期限切れのアクセストークンを新しいトークンに更新します。

**エンドポイント:** `POST /auth/refresh`

**リクエスト例:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**レスポンス例:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 4. 現在のユーザー情報取得
認証されたユーザーの情報を取得します。

**エンドポイント:** `GET /auth/me`

**ヘッダー:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**レスポンス例:**
```json
{
  "id": "user_12345",
  "username": "testuser",
  "email": "test@example.com",
  "is_active": true,
  "created_at": "2025-01-25T10:30:00Z",
  "updated_at": "2025-01-25T10:30:00Z"
}
```

### 5. ログアウト
現在のリフレッシュトークンを無効化します。

**エンドポイント:** `POST /auth/logout`

**ヘッダー:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**リクエスト例:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**レスポンス例:**
```json
{
  "message": "Successfully logged out"
}
```

### 6. 全デバイスからログアウト
ユーザーの全てのリフレッシュトークンを無効化します。

**エンドポイント:** `POST /auth/logout-all`

**ヘッダー:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**レスポンス例:**
```json
{
  "message": "Successfully logged out from all devices"
}
```

## 議事録生成API

### 議事録生成
トランスクリプトから議事録を生成します（認証が必要）。

**エンドポイント:** `POST /minutes/generate`

**ヘッダー:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**リクエスト例:**
```json
{
  "transcript": "おはようございます。今日の進捗報告を始めます。田中です。昨日はユーザー認証機能の実装を完了しました。今日はテストケースの作成を予定しています。",
  "meeting_title": "朝の進捗報告会",
  "participants": ["田中", "佐藤", "鈴木"],
  "meeting_date": "2025-01-25"
}
```

**レスポンス例:**
```json
{
  "meeting_title": "朝の進捗報告会",
  "meeting_date": "2025-01-25",
  "participants": ["田中", "佐藤", "鈴木"],
  "agenda_items": [
    {
      "title": "進捗報告",
      "content": "田中：ユーザー認証機能の実装完了",
      "action_items": ["テストケースの作成"]
    }
  ],
  "decisions": [],
  "next_actions": [
    {
      "action": "テストケースの作成",
      "assignee": "田中",
      "due_date": "2025-01-26"
    }
  ],
  "generated_at": "2025-01-25T10:30:00Z"
}
```

### ヘルスチェック
APIの稼働状況を確認します（認証不要）。

**エンドポイント:** `GET /minutes/health`

**レスポンス例:**
```json
{
  "status": "healthy",
  "service": "minutes-api"
}
```

## 使用例（curl）

### 1. ユーザー登録
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

### 2. ログイン
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123",
    "remember_me": true
  }'
```

### 3. 議事録生成（トークンを使用）
```bash
curl -X POST "http://localhost:8000/minutes/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -d '{
    "transcript": "会議の内容をここに入力",
    "meeting_title": "定例会議",
    "participants": ["参加者1", "参加者2"]
  }'
```

## エラーレスポンス

### 認証エラー
```json
{
  "detail": "Could not validate credentials"
}
```

### 無効なトークン
```json
{
  "detail": "Invalid token"
}
```

### ユーザー重複エラー
```json
{
  "detail": "Username already registered"
}
```

### 無効なログイン情報
```json
{
  "detail": "Incorrect username or password"
}
```

## Swagger UI
APIの詳細なドキュメントとテスト機能は以下のURLで確認できます：
```
http://localhost:8000/docs
```

## トークンの有効期限

- **アクセストークン**: 30分（デフォルト）
- **リフレッシュトークン**: 7日間（デフォルト）
- **Remember Me有効時**: 30日間

## セキュリティ機能

1. **パスワードハッシュ化**: bcryptを使用
2. **トークンローテーション**: リフレッシュ時に新しいリフレッシュトークンを発行
3. **トークン無効化**: ログアウト時にリフレッシュトークンを無効化
4. **CORS対応**: フロントエンド統合のためのCORS設定
5. **入力検証**: Pydanticによる厳密な入力検証

## 環境設定

サーバー起動前に `env/.env` ファイルで以下の設定を行ってください：

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_MODEL=gpt-4
AZURE_OPENAI_VERSION=2024-02-15-preview
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# JWT Configuration
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
JWT_REFRESH_EXPIRE_DAYS=7
JWT_REMEMBER_ME_EXPIRE_DAYS=30
```
