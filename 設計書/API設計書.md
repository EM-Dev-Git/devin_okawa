# API設計書 - トランスクリプト議事録生成システム

## 1. 文書情報

| 項目 | 内容 |
|------|------|
| 文書名 | API設計書 |
| バージョン | 1.0 |
| 作成日 | 2025年7月24日 |
| 作成者 | AI Assistant |
| 基準文書 | 実装計画書01.md, システム設計書.md |

## 2. API概要

### 2.1 API基本情報

| 項目 | 内容 |
|------|------|
| API名 | 議事録生成API |
| ベースURL | `https://api.example.com` |
| プロトコル | HTTPS |
| データ形式 | JSON |
| 文字エンコーディング | UTF-8 |
| APIバージョン | v1.0 |

### 2.2 認証方式
- **認証タイプ**: Bearer Token (将来実装予定)
- **トークン形式**: JWT (JSON Web Token)
- **有効期限**: 24時間
- **リフレッシュ**: 自動リフレッシュ対応

### 2.3 レート制限
- **制限**: 100 requests/minute/IP
- **ヘッダー**: `X-RateLimit-*` ヘッダーで制限情報提供
- **超過時**: HTTP 429 Too Many Requests

## 3. エンドポイント一覧

### 3.1 エンドポイント概要

| メソッド | パス | 説明 | 認証 | 実装状況 |
|---------|------|------|------|----------|
| GET | `/` | ルートエンドポイント | 不要 | ✅ 実装済み |
| POST | `/minutes/generate` | 議事録生成 | 不要 | ✅ 実装済み |
| GET | `/minutes/health` | ヘルスチェック | 不要 | ✅ 実装済み |
| GET | `/docs` | API ドキュメント | 不要 | ✅ 自動生成 |
| GET | `/redoc` | ReDoc ドキュメント | 不要 | ✅ 自動生成 |

### 3.2 将来実装予定エンドポイント

| メソッド | パス | 説明 | 認証 | 実装予定 |
|---------|------|------|------|----------|
| POST | `/auth/login` | ユーザーログイン | 不要 | Phase 2 |
| POST | `/auth/register` | ユーザー登録 | 不要 | Phase 2 |
| GET | `/minutes/` | 議事録一覧取得 | 必要 | Phase 2 |
| GET | `/minutes/{id}` | 議事録詳細取得 | 必要 | Phase 2 |
| PUT | `/minutes/{id}` | 議事録更新 | 必要 | Phase 2 |
| DELETE | `/minutes/{id}` | 議事録削除 | 必要 | Phase 2 |

## 4. エンドポイント詳細仕様

### 4.1 ルートエンドポイント

#### 4.1.1 基本情報
- **メソッド**: `GET`
- **パス**: `/`
- **説明**: APIの基本情報を返却
- **認証**: 不要

#### 4.1.2 リクエスト
```http
GET / HTTP/1.1
Host: api.example.com
Accept: application/json
```

#### 4.1.3 レスポンス
**成功時 (200 OK)**
```json
{
  "message": "議事録生成API",
  "version": "1.0.0"
}
```

#### 4.1.4 レスポンススキーマ
```python
class RootResponse(BaseModel):
    message: str = Field(..., description="APIメッセージ")
    version: str = Field(..., description="APIバージョン")
```

### 4.2 議事録生成エンドポイント

#### 4.2.1 基本情報
- **メソッド**: `POST`
- **パス**: `/minutes/generate`
- **説明**: トランスクリプトから議事録を生成
- **認証**: 不要（将来的に必要）

#### 4.2.2 リクエスト
```http
POST /minutes/generate HTTP/1.1
Host: api.example.com
Content-Type: application/json
Accept: application/json

{
  "content": "会議のトランスクリプト内容...",
  "meeting_title": "週次定例会議",
  "participants": ["田中", "佐藤", "鈴木"]
}
```

#### 4.2.3 リクエストスキーマ
```python
class TranscriptRequest(BaseModel):
    content: str = Field(
        ..., 
        description="トランスクリプト内容",
        min_length=10,
        max_length=100000,
        example="今日の会議では、新しいプロジェクトについて話し合いました。"
    )
    meeting_title: Optional[str] = Field(
        None, 
        description="会議タイトル",
        max_length=200,
        example="週次定例会議"
    )
    participants: Optional[List[str]] = Field(
        None, 
        description="参加者リスト",
        max_items=50,
        example=["田中", "佐藤", "鈴木"]
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "content": "会議のトランスクリプト内容...",
                "meeting_title": "週次定例会議",
                "participants": ["田中", "佐藤", "鈴木"]
            }
        }
    )
```

#### 4.2.4 レスポンス
**成功時 (200 OK)**
```json
{
  "id": "minutes_a1b2c3d4",
  "title": "週次定例会議",
  "content": "## 議事録\n\n### 議題1: 新プロジェクトについて\n- 田中さんより新プロジェクトの概要説明\n- 予算: 500万円\n- 期間: 6ヶ月\n\n### 決定事項\n1. プロジェクト承認\n2. 来週までに詳細計画作成\n\n### アクションアイテム\n- [ ] 田中: 詳細計画書作成 (期限: 2025/07/31)\n- [ ] 佐藤: 予算申請 (期限: 2025/07/28)",
  "created_at": "2025-07-24T10:00:00Z",
  "participants": ["田中", "佐藤", "鈴木"]
}
```

#### 4.2.5 レスポンススキーマ
```python
class MinutesResponse(BaseModel):
    id: str = Field(..., description="議事録ID", example="minutes_a1b2c3d4")
    title: str = Field(..., description="会議タイトル", example="週次定例会議")
    content: str = Field(..., description="議事録内容（Markdown形式）")
    created_at: datetime = Field(..., description="作成日時")
    participants: Optional[List[str]] = Field(None, description="参加者リスト")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "minutes_a1b2c3d4",
                "title": "週次定例会議",
                "content": "## 議事録\n\n### 議題1\n...",
                "created_at": "2025-07-24T10:00:00Z",
                "participants": ["田中", "佐藤", "鈴木"]
            }
        }
    )
```

#### 4.2.6 エラーレスポンス
**バリデーションエラー (422 Unprocessable Entity)**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "content"],
      "msg": "String should have at least 10 characters",
      "input": "短い",
      "ctx": {"min_length": 10}
    }
  ]
}
```

**サーバーエラー (500 Internal Server Error)**
```json
{
  "detail": "議事録生成に失敗しました"
}
```

### 4.3 ヘルスチェックエンドポイント

#### 4.3.1 基本情報
- **メソッド**: `GET`
- **パス**: `/minutes/health`
- **説明**: サービスの稼働状況確認
- **認証**: 不要

#### 4.3.2 リクエスト
```http
GET /minutes/health HTTP/1.1
Host: api.example.com
Accept: application/json
```

#### 4.3.3 レスポンス
**成功時 (200 OK)**
```json
{
  "status": "healthy",
  "service": "minutes-api"
}
```

#### 4.3.4 レスポンススキーマ
```python
class HealthResponse(BaseModel):
    status: str = Field(..., description="サービス状態", example="healthy")
    service: str = Field(..., description="サービス名", example="minutes-api")
```

## 5. データモデル詳細

### 5.1 共通データ型

#### 5.1.1 基本型
```python
# 文字列型（日本語対応）
str_jp = Annotated[str, Field(regex=r'^[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF\w\s\-_.!?()（）「」、。]*$')]

# 日時型（ISO 8601形式）
datetime_iso = Annotated[datetime, Field(example="2025-07-24T10:00:00Z")]

# ID型（英数字8文字）
id_type = Annotated[str, Field(regex=r'^[a-zA-Z0-9]{8}$', example="a1b2c3d4")]
```

#### 5.1.2 制約定義
```python
# 文字列長制約
CONTENT_MIN_LENGTH = 10
CONTENT_MAX_LENGTH = 100000
TITLE_MAX_LENGTH = 200
PARTICIPANT_MAX_COUNT = 50
PARTICIPANT_NAME_MAX_LENGTH = 50

# その他制約
MAX_REQUEST_SIZE = 10 * 1024 * 1024  # 10MB
TIMEOUT_SECONDS = 30
```

### 5.2 バリデーションルール

#### 5.2.1 トランスクリプト内容
```python
@field_validator('content')
@classmethod
def validate_content(cls, v: str) -> str:
    # 空白文字のみの場合はエラー
    if not v.strip():
        raise ValueError('Content cannot be empty or whitespace only')
    
    # 制御文字の除去
    v = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', v)
    
    # 連続する空白の正規化
    v = re.sub(r'\s+', ' ', v)
    
    return v.strip()
```

#### 5.2.2 参加者リスト
```python
@field_validator('participants')
@classmethod
def validate_participants(cls, v: Optional[List[str]]) -> Optional[List[str]]:
    if v is None:
        return v
    
    # 重複除去
    unique_participants = list(dict.fromkeys(v))
    
    # 空文字列の除去
    filtered_participants = [p.strip() for p in unique_participants if p.strip()]
    
    return filtered_participants if filtered_participants else None
```

## 6. エラーハンドリング

### 6.1 HTTPステータスコード

| コード | 説明 | 使用場面 |
|--------|------|----------|
| 200 | OK | 正常処理完了 |
| 400 | Bad Request | 不正なリクエスト |
| 401 | Unauthorized | 認証エラー（将来実装） |
| 403 | Forbidden | 認可エラー（将来実装） |
| 404 | Not Found | リソースが見つからない |
| 422 | Unprocessable Entity | バリデーションエラー |
| 429 | Too Many Requests | レート制限超過 |
| 500 | Internal Server Error | サーバー内部エラー |
| 502 | Bad Gateway | 外部サービスエラー |
| 503 | Service Unavailable | サービス利用不可 |

### 6.2 エラーレスポンス形式

#### 6.2.1 標準エラーレスポンス
```python
class ErrorResponse(BaseModel):
    detail: str = Field(..., description="エラーメッセージ")
    error_code: Optional[str] = Field(None, description="エラーコード")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="エラー発生時刻")
    request_id: Optional[str] = Field(None, description="リクエストID")
```

#### 6.2.2 バリデーションエラーレスポンス
```python
class ValidationError(BaseModel):
    type: str = Field(..., description="エラータイプ")
    loc: List[Union[str, int]] = Field(..., description="エラー箇所")
    msg: str = Field(..., description="エラーメッセージ")
    input: Any = Field(..., description="入力値")
    ctx: Optional[Dict[str, Any]] = Field(None, description="エラーコンテキスト")

class ValidationErrorResponse(BaseModel):
    detail: List[ValidationError] = Field(..., description="バリデーションエラー詳細")
```

### 6.3 エラーコード体系

#### 6.3.1 業務エラーコード
```python
class ErrorCodes:
    # 入力エラー (1000番台)
    INVALID_CONTENT = "E1001"
    CONTENT_TOO_LONG = "E1002"
    INVALID_PARTICIPANTS = "E1003"
    
    # 処理エラー (2000番台)
    AI_SERVICE_ERROR = "E2001"
    PROCESSING_TIMEOUT = "E2002"
    QUOTA_EXCEEDED = "E2003"
    
    # システムエラー (9000番台)
    INTERNAL_ERROR = "E9001"
    SERVICE_UNAVAILABLE = "E9002"
    CONFIGURATION_ERROR = "E9003"
```

#### 6.3.2 エラーメッセージ
```python
ERROR_MESSAGES = {
    "E1001": "トランスクリプト内容が無効です",
    "E1002": "トランスクリプト内容が長すぎます（最大100,000文字）",
    "E1003": "参加者リストの形式が無効です",
    "E2001": "AI サービスでエラーが発生しました",
    "E2002": "処理がタイムアウトしました",
    "E2003": "利用制限に達しました",
    "E9001": "内部エラーが発生しました",
    "E9002": "サービスが利用できません",
    "E9003": "設定エラーが発生しました"
}
```

## 7. セキュリティ仕様

### 7.1 HTTPS通信
- **TLS バージョン**: TLS 1.3 以上
- **証明書**: 有効なSSL証明書必須
- **HSTS**: HTTP Strict Transport Security 有効
- **リダイレクト**: HTTP → HTTPS 自動リダイレクト

### 7.2 CORS設定
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trusted-domain.com"],  # 本番環境では制限
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 7.3 入力検証
- **SQLインジェクション**: Pydantic による型安全な検証
- **XSS**: 入力値のサニタイゼーション
- **CSRF**: CSRF トークンによる保護（将来実装）
- **ファイルアップロード**: ファイル形式・サイズ制限

### 7.4 レート制限
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/minutes/generate")
@limiter.limit("10/minute")
async def generate_minutes(request: Request, data: TranscriptRequest):
    # 処理実装
    pass
```

## 8. パフォーマンス仕様

### 8.1 レスポンス時間目標

| エンドポイント | 目標時間 | 最大時間 |
|---------------|----------|----------|
| `/` | < 100ms | 500ms |
| `/minutes/health` | < 100ms | 500ms |
| `/minutes/generate` | < 5s | 30s |

### 8.2 スループット目標
- **同時接続数**: 1,000 接続
- **リクエスト/秒**: 100 req/sec
- **データ転送量**: 10 MB/sec

### 8.3 キャッシュ戦略
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# Redis キャッシュ設定（将来実装）
FastAPICache.init(RedisBackend(), prefix="minutes-api")

@cache(expire=3600)  # 1時間キャッシュ
async def get_cached_response():
    pass
```

## 9. 監視・ログ仕様

### 9.1 アクセスログ
```python
import logging
from fastapi import Request

logger = logging.getLogger("access")

async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.client.host} - "
        f'"{request.method} {request.url.path}" '
        f"{response.status_code} "
        f"{process_time:.3f}s"
    )
    return response
```

### 9.2 エラーログ
```python
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Unhandled exception: {exc}",
        extra={
            "request_id": request.headers.get("X-Request-ID"),
            "path": request.url.path,
            "method": request.method,
            "traceback": traceback.format_exc()
        }
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

### 9.3 メトリクス
- **リクエスト数**: エンドポイント別リクエスト数
- **レスポンス時間**: 平均・95パーセンタイル・最大値
- **エラー率**: HTTP ステータスコード別エラー率
- **Azure OpenAI**: API呼び出し回数・レスポンス時間

## 10. API バージョニング

### 10.1 バージョニング戦略
- **URL パス**: `/v1/minutes/generate`
- **ヘッダー**: `Accept: application/vnd.api+json;version=1`
- **後方互換性**: 最低2バージョン維持

### 10.2 変更管理
```python
# バージョン別ルーター
v1_router = APIRouter(prefix="/v1")
v2_router = APIRouter(prefix="/v2")

app.include_router(v1_router)
app.include_router(v2_router)

# デフォルトバージョン（最新）
app.include_router(v2_router, prefix="")
```

## 11. テスト仕様

### 11.1 単体テスト
```python
import pytest
from fastapi.testclient import TestClient

def test_generate_minutes_success():
    response = client.post("/minutes/generate", json={
        "content": "テスト用のトランスクリプト内容",
        "meeting_title": "テスト会議"
    })
    assert response.status_code == 200
    assert "id" in response.json()
    assert "content" in response.json()
```

### 11.2 統合テスト
```python
@pytest.mark.asyncio
async def test_end_to_end_flow():
    # 1. ヘルスチェック
    health_response = await client.get("/minutes/health")
    assert health_response.status_code == 200
    
    # 2. 議事録生成
    minutes_response = await client.post("/minutes/generate", json=test_data)
    assert minutes_response.status_code == 200
```

### 11.3 負荷テスト
```python
import asyncio
import aiohttp

async def load_test():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(100):
            task = session.post("/minutes/generate", json=test_data)
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        success_count = sum(1 for r in responses if r.status == 200)
        assert success_count >= 95  # 95%以上成功
```

## 12. 将来拡張計画

### 12.1 認証・認可機能
```python
# JWT認証エンドポイント
@router.post("/auth/login")
async def login(credentials: UserCredentials):
    # 認証処理
    pass

@router.post("/auth/register")
async def register(user_data: UserRegistration):
    # ユーザー登録処理
    pass
```

### 12.2 議事録管理機能
```python
# 議事録CRUD操作
@router.get("/minutes/")
async def list_minutes(current_user: User = Depends(get_current_user)):
    # 議事録一覧取得
    pass

@router.get("/minutes/{minutes_id}")
async def get_minutes(minutes_id: str, current_user: User = Depends(get_current_user)):
    # 議事録詳細取得
    pass

@router.put("/minutes/{minutes_id}")
async def update_minutes(minutes_id: str, data: MinutesUpdate, current_user: User = Depends(get_current_user)):
    # 議事録更新
    pass

@router.delete("/minutes/{minutes_id}")
async def delete_minutes(minutes_id: str, current_user: User = Depends(get_current_user)):
    # 議事録削除
    pass
```

### 12.3 Microsoft Graph統合
```python
# Teams連携エンドポイント
@router.get("/graph/meetings")
async def get_meetings(current_user: User = Depends(get_current_user)):
    # Teams会議一覧取得
    pass

@router.get("/graph/meetings/{meeting_id}/transcript")
async def get_meeting_transcript(meeting_id: str, current_user: User = Depends(get_current_user)):
    # 会議トランスクリプト取得
    pass

@router.post("/graph/meetings/{meeting_id}/generate-minutes")
async def generate_minutes_from_teams(meeting_id: str, current_user: User = Depends(get_current_user)):
    # Teams会議から議事録生成
    pass
```

---

**文書管理情報**
- **最終更新**: 2025年7月24日
- **レビュー状況**: 初版作成完了
- **承認者**: 未定
- **次回レビュー**: 実装完了後
