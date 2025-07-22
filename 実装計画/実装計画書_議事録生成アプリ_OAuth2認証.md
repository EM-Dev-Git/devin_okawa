# FastAPI 議事録生成アプリ OAuth2認証 実装計画書

## 1. プロジェクト概要

### 1.1 目的
FastAPIを使用して議事録生成アプリケーションを作成し、OAuth2を使った認証機能を実装する。
Azure OpenAIを活用した議事録生成機能と、JWTベースの認証システムを統合した最小構成のWebアプリケーションを構築する。

### 1.2 主要機能
- **議事録生成機能**: Azure OpenAI APIを使用した会議トランスクリプトから議事録への自動変換
- **OAuth2認証機能**: JWTトークンベースのユーザー認証システム
- **ユーザー管理**: メモリ内辞書を使用した軽量なユーザー管理
- **API保護**: 認証が必要なエンドポイントの保護
- **ログ機能**: 包括的なログ記録とエラーハンドリング

### 1.3 技術スタック
- **フレームワーク**: FastAPI 0.104+
- **認証**: OAuth2 with Password (and hashing), Bearer with JWT tokens
- **AI処理**: Azure OpenAI API
- **パスワードハッシュ**: bcrypt
- **JWT処理**: PyJWT
- **データ管理**: メモリ内Python辞書（最小構成）
- **バリデーション**: Pydantic
- **設定管理**: pydantic-settings
- **テスト**: pytest + TestClient

## 2. システム構成

### 2.1 ディレクトリ構造
```
/
├── src/
│   ├── __init__.py
│   ├── main.py                    # FastAPIアプリケーションエントリーポイント
│   ├── config.py                  # 設定管理
│   ├── schemas/                   # Pydanticデータモデル
│   │   ├── __init__.py
│   │   ├── auth.py               # 認証関連スキーマ
│   │   ├── transcript.py         # トランスクリプトスキーマ
│   │   └── minutes.py            # 議事録スキーマ
│   ├── modules/                   # ビジネスロジック
│   │   ├── __init__.py
│   │   ├── auth.py               # 認証ユーティリティ
│   │   ├── user_store.py         # メモリ内ユーザー管理
│   │   ├── azure_openai_client.py # Azure OpenAIクライアント
│   │   ├── minutes_generator.py   # 議事録生成ロジック
│   │   └── logger_config.py       # ログ設定
│   ├── routers/                   # FastAPIルーター
│   │   ├── __init__.py
│   │   ├── auth.py               # 認証エンドポイント
│   │   └── minutes.py            # 議事録生成エンドポイント
│   └── dependencies/             # FastAPI依存関係
│       ├── __init__.py
│       └── auth.py               # 認証依存関係
├── env/                          # 環境設定
│   ├── .env                      # 環境変数（機密情報）
│   └── .env.example              # 環境変数テンプレート
├── requirements.txt              # Python依存関係
└── README.md                     # プロジェクト説明
```

### 2.2 アーキテクチャ図
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Azure OpenAI  │
│   (Client)      │◄──►│   Backend       │◄──►│   API           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   In-Memory     │
                       │   User Store    │
                       └─────────────────┘
```

## 3. 環境設定

### 3.1 依存関係 (requirements.txt)
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
PyJWT==2.8.0
bcrypt==4.1.2
openai==1.3.0
python-dotenv==1.0.0
pytest==7.4.3
httpx==0.25.2
```

### 3.2 環境変数設定

#### env/.env
```env
# Azure OpenAI設定
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_MODEL=gpt-4
AZURE_OPENAI_VERSION=2024-02-15-preview
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# JWT認証設定
JWT_SECRET_KEY=your_super_secret_jwt_key_here_change_in_production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# アプリケーション設定
APP_NAME=Meeting Minutes Generator
APP_VERSION=1.0.0
DEBUG=False
```

#### env/.env.example
```env
# Azure OpenAI設定
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_MODEL=gpt-4
AZURE_OPENAI_VERSION=2024-02-15-preview
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# JWT認証設定
JWT_SECRET_KEY=your_super_secret_jwt_key_here_change_in_production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# アプリケーション設定
APP_NAME=Meeting Minutes Generator
APP_VERSION=1.0.0
DEBUG=False
```

## 4. 実装詳細

### 4.1 設定管理 (src/config.py)
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Azure OpenAI設定
    azure_openai_api_key: str
    azure_openai_model: str = "gpt-4"
    azure_openai_version: str = "2024-02-15-preview"
    azure_openai_endpoint: str
    
    # JWT認証設定
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # アプリケーション設定
    app_name: str = "Meeting Minutes Generator"
    app_version: str = "1.0.0"
    debug: bool = False
    
    class Config:
        env_file = "env/.env"

settings = Settings()
```

### 4.2 認証スキーマ (src/schemas/auth.py)
```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
```

### 4.3 議事録スキーマ (src/schemas/transcript.py, src/schemas/minutes.py)
```python
# src/schemas/transcript.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TranscriptInput(BaseModel):
    meeting_title: str
    meeting_date: datetime
    participants: List[str]
    transcript_text: str
    additional_notes: Optional[str] = None

# src/schemas/minutes.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MinutesOutput(BaseModel):
    meeting_title: str
    meeting_date: datetime
    participants: List[str]
    summary: str
    key_points: List[str]
    action_items: List[str]
    next_meeting: Optional[str] = None
    generated_at: datetime
```

### 4.4 ユーザー管理 (src/modules/user_store.py)
```python
import uuid
from datetime import datetime
from typing import Dict, Optional, List

class UserStore:
    def __init__(self):
        self.users: Dict[str, Dict] = {}
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        return self.users.get(username)
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        for user_data in self.users.values():
            if user_data.get('email') == email:
                return user_data
        return None
    
    def create_user(self, username: str, email: str, hashed_password: str) -> Dict:
        user_id = str(uuid.uuid4())
        user_data = {
            'id': user_id,
            'username': username,
            'email': email,
            'hashed_password': hashed_password,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        self.users[username] = user_data
        return user_data
    
    def update_user(self, username: str, **kwargs) -> Optional[Dict]:
        if username not in self.users:
            return None
        
        self.users[username].update(kwargs)
        self.users[username]['updated_at'] = datetime.utcnow()
        return self.users[username]
    
    def delete_user(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            return True
        return False
    
    def list_users(self) -> List[Dict]:
        return list(self.users.values())
    
    def clear_all_users(self):
        self.users.clear()

user_store = UserStore()
```

### 4.5 認証ユーティリティ (src/modules/auth.py)
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.modules.config import settings
from src.modules.user_store import user_store
from src.schemas.auth import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    user = user_store.get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user['hashed_password']):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data

def get_user_by_username(username: str):
    return user_store.get_user_by_username(username)

def get_user_by_email(email: str):
    return user_store.get_user_by_email(email)

def create_user(username: str, email: str, password: str):
    hashed_password = get_password_hash(password)
    return user_store.create_user(username, email, hashed_password)
```

### 4.6 認証依存関係 (src/dependencies/auth.py)
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.modules.auth import verify_token, get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token, credentials_exception)
    user = get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if not current_user.get('is_active'):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

### 4.7 認証ルーター (src/routers/auth.py)
```python
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.auth import UserCreate, UserResponse, Token
from src.modules.auth import (
    authenticate_user, 
    create_access_token, 
    get_user_by_username, 
    get_user_by_email, 
    create_user
)
from src.dependencies.auth import get_current_active_user
import logging

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    try:
        if get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        if get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        user = create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        
        logger.info(f"User registration successful: {user_data.username}")
        return UserResponse(**user)
        
    except Exception as e:
        logger.error(f"User registration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            logger.warning(f"Failed login attempt: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": user['username']})
        logger.info(f"User login successful: {form_data.username}")
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    return UserResponse(**current_user)

@router.post("/logout")
async def logout_user(current_user: dict = Depends(get_current_active_user)):
    logger.info(f"User logout: {current_user['username']}")
    return {"message": "Successfully logged out"}
```

### 4.8 議事録生成ルーター (src/routers/minutes.py)
```python
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.transcript import TranscriptInput
from src.schemas.minutes import MinutesOutput
from src.modules.minutes_generator import MinutesGenerator
from src.dependencies.auth import get_current_active_user
import logging

router = APIRouter(prefix="/api/v1/minutes", tags=["minutes"])
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=MinutesOutput)
async def generate_meeting_minutes(
    transcript_data: TranscriptInput,
    current_user: dict = Depends(get_current_active_user)
):
    try:
        logger.info(f"User {current_user['username']} requested minutes generation for: {transcript_data.meeting_title}")
        
        generator = MinutesGenerator()
        minutes = generator.generate_minutes(transcript_data)
        
        logger.info("Minutes generation request completed successfully")
        return minutes
        
    except Exception as e:
        logger.error(f"Error generating meeting minutes: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate meeting minutes: {str(e)}"
        )
```

### 4.9 メインアプリケーション (src/main.py)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.auth import router as auth_router
from src.routers.minutes import router as minutes_router
from src.modules.logger_config import setup_logger
from src.config import settings
import logging

setup_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="Azure OpenAI powered meeting minutes generation system with OAuth2 authentication",
    version=settings.app_version
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(minutes_router)

@app.get("/")
async def root():
    return {
        "message": f"{settings.app_name} API", 
        "status": "running",
        "version": settings.app_version
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "meeting-minutes-generator"}

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {settings.app_name} API server")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.debug)
```

## 5. 実装手順

### 5.1 環境セットアップ
1. 仮想環境の作成と有効化
2. 依存関係のインストール: `pip install -r requirements.txt`
3. 環境変数ファイルの設定: `cp env/.env.example env/.env`
4. Azure OpenAI APIキーの設定

### 5.2 コア機能実装順序
1. **設定管理**: `src/config.py`
2. **スキーマ定義**: `src/schemas/`
3. **ユーザー管理**: `src/modules/user_store.py`
4. **認証機能**: `src/modules/auth.py`
5. **依存関係**: `src/dependencies/auth.py`
6. **認証ルーター**: `src/routers/auth.py`
7. **議事録ルーター**: `src/routers/minutes.py`（認証保護追加）
8. **メインアプリケーション**: `src/main.py`

### 5.3 テスト実装
1. 単体テスト: 各モジュールの個別テスト
2. 統合テスト: API エンドポイントのテスト
3. 認証フローテスト: ログイン・認証・保護されたエンドポイントアクセス

### 5.4 起動・動作確認
```bash
# 開発サーバー起動
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# API ドキュメント確認
# http://localhost:8000/docs
```

## 6. セキュリティ考慮事項

### 6.1 認証セキュリティ
- パスワードのbcryptハッシュ化
- JWTトークンの適切な有効期限設定
- HTTPS通信の推奨（本番環境）
- 環境変数での機密情報管理

### 6.2 API セキュリティ
- CORS設定の適切な制限（本番環境）
- レート制限の実装（本番環境推奨）
- 入力値検証とサニタイゼーション
- エラーメッセージでの情報漏洩防止

## 7. 運用・保守

### 7.1 ログ管理
- 構造化ログの実装
- 認証イベントの記録
- エラー追跡とモニタリング

### 7.2 パフォーマンス
- Azure OpenAI APIレスポンス時間の監視
- メモリ使用量の監視（ユーザー数増加時）
- 非同期処理の活用

### 7.3 スケーラビリティ
- メモリ内ユーザーストアからデータベースへの移行計画
- 水平スケーリング対応
- キャッシュ戦略の検討

## 8. 参考資料

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [FastAPI Security Tutorial](https://fastapi.tiangolo.com/tutorial/security/)
- [OAuth2 with Password (and hashing), Bearer with JWT tokens](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [Azure OpenAI Service Documentation](https://docs.microsoft.com/azure/cognitive-services/openai/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
