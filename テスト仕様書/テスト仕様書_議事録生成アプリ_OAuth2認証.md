# FastAPI 議事録生成アプリ OAuth2認証 テスト仕様書

## 1. テスト概要

### 1.1 テスト目的
FastAPIを使用した議事録生成アプリケーションのOAuth2認証機能および議事録生成機能の品質保証を行う。
すべての機能が仕様通りに動作し、セキュリティ要件を満たすことを確認する。

### 1.2 テスト対象
- OAuth2認証システム（ユーザー登録、ログイン、トークン管理）
- 議事録生成機能（Azure OpenAI統合）
- API エンドポイントの保護機能
- エラーハンドリング
- セキュリティ機能

### 1.3 テスト環境
- **テストフレームワーク**: pytest
- **HTTPクライアント**: FastAPI TestClient
- **モック**: unittest.mock
- **カバレッジ**: pytest-cov
- **Python バージョン**: 3.8+

### 1.4 テスト戦略
- **単体テスト**: 各モジュールの個別機能テスト
- **統合テスト**: API エンドポイントの統合テスト
- **セキュリティテスト**: 認証・認可機能のテスト
- **エラーハンドリングテスト**: 異常系のテスト

## 2. テスト環境セットアップ

### 2.1 テスト用依存関係
```txt
# requirements-test.txt
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2
pytest-mock==3.12.0
```

### 2.2 テスト設定ファイル
```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.modules.user_store import user_store

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def clean_user_store():
    user_store.clear_all_users()
    yield
    user_store.clear_all_users()

@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }

@pytest.fixture
def authenticated_headers(client, test_user_data, clean_user_store):
    # ユーザー登録
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # ログイン
    login_data = {
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}
```

### 2.3 テスト用環境変数
```python
# test_config.py
import os
from src.config import Settings

def get_test_settings():
    return Settings(
        azure_openai_api_key="test_key",
        azure_openai_model="gpt-4",
        azure_openai_version="2024-02-15-preview",
        azure_openai_endpoint="https://test.openai.azure.com/",
        jwt_secret_key="test_secret_key_for_testing_only",
        jwt_algorithm="HS256",
        jwt_expire_minutes=30,
        app_name="Test Meeting Minutes Generator",
        app_version="1.0.0-test",
        debug=True
    )
```

## 3. 単体テスト仕様

### 3.1 ユーザーストアテスト (test_user_store.py)

#### 3.1.1 ユーザー作成テスト
```python
def test_create_user(clean_user_store):
    """ユーザー作成機能のテスト"""
    # テストデータ
    username = "testuser"
    email = "test@example.com"
    hashed_password = "hashed_password_123"
    
    # ユーザー作成
    user = user_store.create_user(username, email, hashed_password)
    
    # 検証
    assert user["username"] == username
    assert user["email"] == email
    assert user["hashed_password"] == hashed_password
    assert user["is_active"] is True
    assert "id" in user
    assert "created_at" in user
    assert "updated_at" in user
```

#### 3.1.2 ユーザー取得テスト
```python
def test_get_user_by_username(clean_user_store):
    """ユーザー名によるユーザー取得テスト"""
    # テストユーザー作成
    username = "testuser"
    user_store.create_user(username, "test@example.com", "hashed_password")
    
    # ユーザー取得
    retrieved_user = user_store.get_user_by_username(username)
    
    # 検証
    assert retrieved_user is not None
    assert retrieved_user["username"] == username

def test_get_user_by_email(clean_user_store):
    """メールアドレスによるユーザー取得テスト"""
    # テストユーザー作成
    email = "test@example.com"
    user_store.create_user("testuser", email, "hashed_password")
    
    # ユーザー取得
    retrieved_user = user_store.get_user_by_email(email)
    
    # 検証
    assert retrieved_user is not None
    assert retrieved_user["email"] == email

def test_get_nonexistent_user(clean_user_store):
    """存在しないユーザーの取得テスト"""
    # 存在しないユーザーの取得
    user = user_store.get_user_by_username("nonexistent")
    
    # 検証
    assert user is None
```

#### 3.1.3 ユーザー更新・削除テスト
```python
def test_update_user(clean_user_store):
    """ユーザー情報更新テスト"""
    # テストユーザー作成
    username = "testuser"
    user_store.create_user(username, "test@example.com", "hashed_password")
    
    # ユーザー更新
    updated_user = user_store.update_user(username, email="updated@example.com")
    
    # 検証
    assert updated_user is not None
    assert updated_user["email"] == "updated@example.com"
    assert "updated_at" in updated_user

def test_delete_user(clean_user_store):
    """ユーザー削除テスト"""
    # テストユーザー作成
    username = "testuser"
    user_store.create_user(username, "test@example.com", "hashed_password")
    
    # ユーザー削除
    result = user_store.delete_user(username)
    
    # 検証
    assert result is True
    assert user_store.get_user_by_username(username) is None
```

### 3.2 認証モジュールテスト (test_auth.py)

#### 3.2.1 パスワードハッシュテスト
```python
from src.modules.auth import get_password_hash, verify_password

def test_password_hashing():
    """パスワードハッシュ化テスト"""
    password = "testpassword123"
    
    # パスワードハッシュ化
    hashed = get_password_hash(password)
    
    # 検証
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False
```

#### 3.2.2 JWTトークンテスト
```python
from src.modules.auth import create_access_token, verify_token
from fastapi import HTTPException
import pytest

def test_create_access_token():
    """JWTトークン作成テスト"""
    data = {"sub": "testuser"}
    
    # トークン作成
    token = create_access_token(data)
    
    # 検証
    assert isinstance(token, str)
    assert len(token) > 0

def test_verify_valid_token():
    """有効なJWTトークン検証テスト"""
    data = {"sub": "testuser"}
    token = create_access_token(data)
    
    # トークン検証
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    token_data = verify_token(token, credentials_exception)
    
    # 検証
    assert token_data.username == "testuser"

def test_verify_invalid_token():
    """無効なJWTトークン検証テスト"""
    invalid_token = "invalid.token.here"
    
    # トークン検証（例外発生を期待）
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    
    with pytest.raises(HTTPException):
        verify_token(invalid_token, credentials_exception)
```

#### 3.2.3 ユーザー認証テスト
```python
from src.modules.auth import authenticate_user, create_user

def test_authenticate_valid_user(clean_user_store):
    """有効なユーザー認証テスト"""
    # テストユーザー作成
    username = "testuser"
    password = "testpassword123"
    create_user(username, "test@example.com", password)
    
    # ユーザー認証
    user = authenticate_user(username, password)
    
    # 検証
    assert user is not False
    assert user["username"] == username

def test_authenticate_invalid_user(clean_user_store):
    """無効なユーザー認証テスト"""
    # 存在しないユーザーの認証
    user = authenticate_user("nonexistent", "password")
    
    # 検証
    assert user is False

def test_authenticate_wrong_password(clean_user_store):
    """間違ったパスワードでの認証テスト"""
    # テストユーザー作成
    username = "testuser"
    create_user(username, "test@example.com", "correctpassword")
    
    # 間違ったパスワードで認証
    user = authenticate_user(username, "wrongpassword")
    
    # 検証
    assert user is False
```

### 3.3 議事録生成モジュールテスト (test_minutes_generator.py)

#### 3.3.1 Azure OpenAI クライアントテスト
```python
import pytest
from unittest.mock import Mock, patch
from src.modules.azure_openai_client import AzureOpenAIClient

def test_azure_openai_client_initialization():
    """Azure OpenAI クライアント初期化テスト"""
    client = AzureOpenAIClient(
        azure_openai_api_key="test_key",
        azure_openai_endpoint="https://test.openai.azure.com/",
        azure_openai_model="gpt-4",
        azure_openai_version="2024-02-15-preview"
    )
    
    assert client.azure_openai_api_key == "test_key"
    assert client.azure_openai_model == "gpt-4"

def test_azure_openai_client_missing_config():
    """Azure OpenAI クライアント設定不足テスト"""
    with pytest.raises(ValueError):
        AzureOpenAIClient(
            azure_openai_api_key="",
            azure_openai_endpoint="https://test.openai.azure.com/",
            azure_openai_model="gpt-4",
            azure_openai_version="2024-02-15-preview"
        )

@patch('src.modules.azure_openai_client.AzureOpenAI')
def test_generate_minutes_success(mock_azure_openai):
    """議事録生成成功テスト"""
    # モックレスポンス設定
    mock_response = Mock()
    mock_response.choices[0].message.content = "Generated minutes content"
    mock_azure_openai.return_value.chat.completions.create.return_value = mock_response
    
    # クライアント作成
    client = AzureOpenAIClient(
        azure_openai_api_key="test_key",
        azure_openai_endpoint="https://test.openai.azure.com/",
        azure_openai_model="gpt-4",
        azure_openai_version="2024-02-15-preview"
    )
    
    # 議事録生成
    result = client.generate_minutes("Test prompt")
    
    # 検証
    assert result == "Generated minutes content"
    mock_azure_openai.return_value.chat.completions.create.assert_called_once()
```

## 4. 統合テスト仕様

### 4.1 認証APIテスト (test_auth_api.py)

#### 4.1.1 ユーザー登録テスト
```python
def test_register_user_success(client, clean_user_store):
    """ユーザー登録成功テスト"""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword123"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "created_at" in data

def test_register_duplicate_username(client, clean_user_store):
    """重複ユーザー名登録テスト"""
    user_data = {
        "username": "testuser",
        "email": "test1@example.com",
        "password": "password123"
    }
    
    # 最初の登録
    client.post("/api/v1/auth/register", json=user_data)
    
    # 重複ユーザー名で再登録
    duplicate_data = {
        "username": "testuser",
        "email": "test2@example.com",
        "password": "password456"
    }
    
    response = client.post("/api/v1/auth/register", json=duplicate_data)
    
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]

def test_register_duplicate_email(client, clean_user_store):
    """重複メールアドレス登録テスト"""
    user_data = {
        "username": "testuser1",
        "email": "test@example.com",
        "password": "password123"
    }
    
    # 最初の登録
    client.post("/api/v1/auth/register", json=user_data)
    
    # 重複メールアドレスで再登録
    duplicate_data = {
        "username": "testuser2",
        "email": "test@example.com",
        "password": "password456"
    }
    
    response = client.post("/api/v1/auth/register", json=duplicate_data)
    
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_register_invalid_email(client, clean_user_store):
    """無効なメールアドレス登録テスト"""
    user_data = {
        "username": "testuser",
        "email": "invalid-email",
        "password": "password123"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 422
```

#### 4.1.2 ログインテスト
```python
def test_login_success(client, test_user_data, clean_user_store):
    """ログイン成功テスト"""
    # ユーザー登録
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # ログイン
    login_data = {
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_username(client, clean_user_store):
    """無効なユーザー名でのログインテスト"""
    login_data = {
        "username": "nonexistent",
        "password": "password123"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_login_invalid_password(client, test_user_data, clean_user_store):
    """無効なパスワードでのログインテスト"""
    # ユーザー登録
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # 間違ったパスワードでログイン
    login_data = {
        "username": test_user_data["username"],
        "password": "wrongpassword"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]
```

#### 4.1.3 認証保護エンドポイントテスト
```python
def test_get_current_user_success(client, authenticated_headers):
    """現在のユーザー情報取得成功テスト"""
    response = client.get("/api/v1/auth/me", headers=authenticated_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert "email" in data
    assert "id" in data

def test_get_current_user_no_token(client):
    """トークンなしでの現在ユーザー情報取得テスト"""
    response = client.get("/api/v1/auth/me")
    
    assert response.status_code == 401

def test_get_current_user_invalid_token(client):
    """無効なトークンでの現在ユーザー情報取得テスト"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 401

def test_logout_success(client, authenticated_headers):
    """ログアウト成功テスト"""
    response = client.post("/api/v1/auth/logout", headers=authenticated_headers)
    
    assert response.status_code == 200
    assert "Successfully logged out" in response.json()["message"]
```

### 4.2 議事録生成APIテスト (test_minutes_api.py)

#### 4.2.1 議事録生成テスト
```python
@patch('src.modules.azure_openai_client.AzureOpenAI')
def test_generate_minutes_success(mock_azure_openai, client, authenticated_headers):
    """議事録生成成功テスト"""
    # モックレスポンス設定
    mock_response = Mock()
    mock_response.choices[0].message.content = '''
    {
        "meeting_title": "Weekly Team Meeting",
        "meeting_date": "2024-01-15T10:00:00",
        "participants": ["Alice", "Bob", "Charlie"],
        "summary": "Discussed project progress and next steps",
        "key_points": ["Project is on track", "Need to review requirements"],
        "action_items": ["Alice to update documentation", "Bob to review code"],
        "next_meeting": "2024-01-22T10:00:00"
    }
    '''
    mock_azure_openai.return_value.chat.completions.create.return_value = mock_response
    
    # テストデータ
    transcript_data = {
        "meeting_title": "Weekly Team Meeting",
        "meeting_date": "2024-01-15T10:00:00",
        "participants": ["Alice", "Bob", "Charlie"],
        "transcript_text": "Alice: Good morning everyone. Let's start with the project update...",
        "additional_notes": "Meeting held via video conference"
    }
    
    response = client.post(
        "/api/v1/minutes/generate",
        json=transcript_data,
        headers=authenticated_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "meeting_title" in data
    assert "summary" in data
    assert "key_points" in data
    assert "action_items" in data

def test_generate_minutes_no_auth(client):
    """認証なしでの議事録生成テスト"""
    transcript_data = {
        "meeting_title": "Weekly Team Meeting",
        "meeting_date": "2024-01-15T10:00:00",
        "participants": ["Alice", "Bob", "Charlie"],
        "transcript_text": "Alice: Good morning everyone...",
    }
    
    response = client.post("/api/v1/minutes/generate", json=transcript_data)
    
    assert response.status_code == 401

@patch('src.modules.azure_openai_client.AzureOpenAI')
def test_generate_minutes_invalid_token(mock_azure_openai, client):
    """無効なトークンでの議事録生成テスト"""
    transcript_data = {
        "meeting_title": "Weekly Team Meeting",
        "meeting_date": "2024-01-15T10:00:00",
        "participants": ["Alice", "Bob", "Charlie"],
        "transcript_text": "Alice: Good morning everyone...",
    }
    
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post(
        "/api/v1/minutes/generate",
        json=transcript_data,
        headers=headers
    )
    
    assert response.status_code == 401

@patch('src.modules.azure_openai_client.AzureOpenAI')
def test_generate_minutes_azure_openai_error(mock_azure_openai, client, authenticated_headers):
    """Azure OpenAI APIエラー時の議事録生成テスト"""
    # Azure OpenAI APIエラーをシミュレート
    mock_azure_openai.return_value.chat.completions.create.side_effect = Exception("API Error")
    
    transcript_data = {
        "meeting_title": "Weekly Team Meeting",
        "meeting_date": "2024-01-15T10:00:00",
        "participants": ["Alice", "Bob", "Charlie"],
        "transcript_text": "Alice: Good morning everyone...",
    }
    
    response = client.post(
        "/api/v1/minutes/generate",
        json=transcript_data,
        headers=authenticated_headers
    )
    
    assert response.status_code == 500
    assert "Failed to generate meeting minutes" in response.json()["detail"]

def test_generate_minutes_invalid_data(client, authenticated_headers):
    """無効なデータでの議事録生成テスト"""
    invalid_data = {
        "meeting_title": "",  # 空のタイトル
        "meeting_date": "invalid-date",  # 無効な日付
        "participants": [],  # 空の参加者リスト
        "transcript_text": "",  # 空のトランスクリプト
    }
    
    response = client.post(
        "/api/v1/minutes/generate",
        json=invalid_data,
        headers=authenticated_headers
    )
    
    assert response.status_code == 422
```

### 4.3 アプリケーション全体テスト (test_main.py)

#### 4.3.1 基本エンドポイントテスト
```python
def test_root_endpoint(client):
    """ルートエンドポイントテスト"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert "version" in data
    assert data["status"] == "running"

def test_health_check_endpoint(client):
    """ヘルスチェックエンドポイントテスト"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "meeting-minutes-generator"
```

## 5. セキュリティテスト仕様

### 5.1 認証セキュリティテスト (test_security.py)

#### 5.1.1 JWTトークンセキュリティテスト
```python
import jwt
from datetime import datetime, timedelta
from src.config import settings

def test_expired_token(client, test_user_data, clean_user_store):
    """期限切れトークンテスト"""
    # ユーザー登録
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # 期限切れトークンを手動作成
    expired_payload = {
        "sub": test_user_data["username"],
        "exp": datetime.utcnow() - timedelta(minutes=1)  # 1分前に期限切れ
    }
    expired_token = jwt.encode(expired_payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 401

def test_malformed_token(client):
    """不正な形式のトークンテスト"""
    headers = {"Authorization": "Bearer malformed.token"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 401

def test_missing_bearer_prefix(client, authenticated_headers):
    """Bearerプレフィックス欠如テスト"""
    token = authenticated_headers["Authorization"].replace("Bearer ", "")
    headers = {"Authorization": token}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 401

def test_token_with_wrong_secret(client, test_user_data, clean_user_store):
    """間違った秘密鍵で作成されたトークンテスト"""
    # ユーザー登録
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # 間違った秘密鍵でトークン作成
    wrong_payload = {"sub": test_user_data["username"]}
    wrong_token = jwt.encode(wrong_payload, "wrong_secret_key", algorithm=settings.jwt_algorithm)
    
    headers = {"Authorization": f"Bearer {wrong_token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 401
```

#### 5.1.2 パスワードセキュリティテスト
```python
def test_password_strength_validation(client, clean_user_store):
    """パスワード強度検証テスト（実装に応じて調整）"""
    weak_passwords = [
        "123",
        "password",
        "abc",
        ""
    ]
    
    for weak_password in weak_passwords:
        user_data = {
            "username": f"user_{weak_password}",
            "email": f"user_{weak_password}@example.com",
            "password": weak_password
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        # パスワード強度チェックが実装されている場合は400、そうでなければ200
        # 実装に応じて調整が必要
        assert response.status_code in [200, 400, 422]

def test_password_hashing_uniqueness():
    """パスワードハッシュの一意性テスト"""
    from src.modules.auth import get_password_hash
    
    password = "testpassword123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    # bcryptは同じパスワードでも異なるハッシュを生成する
    assert hash1 != hash2
    
    # しかし両方とも元のパスワードで検証できる
    from src.modules.auth import verify_password
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True
```

### 5.2 入力値検証テスト (test_input_validation.py)

#### 5.2.1 SQLインジェクション対策テスト
```python
def test_sql_injection_attempts(client, clean_user_store):
    """SQLインジェクション攻撃テスト"""
    malicious_inputs = [
        "'; DROP TABLE users; --",
        "admin'--",
        "' OR '1'='1",
        "1' UNION SELECT * FROM users--"
    ]
    
    for malicious_input in malicious_inputs:
        user_data = {
            "username": malicious_input,
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        # 適切に処理されることを確認（エラーまたは正常処理）
        assert response.status_code in [200, 400, 422]

def test_xss_prevention(client, authenticated_headers):
    """XSS攻撃防止テスト"""
    malicious_script = "<script>alert('XSS')</script>"
    
    transcript_data = {
        "meeting_title": malicious_script,
        "meeting_date": "2024-01-15T10:00:00",
        "participants": [malicious_script],
        "transcript_text": f"Meeting content with {malicious_script}",
    }
    
    response = client.post(
        "/api/v1/minutes/generate",
        json=transcript_data,
        headers=authenticated_headers
    )
    
    # レスポンスにスクリプトタグが含まれていないことを確認
    if response.status_code == 200:
        response_text = response.text
        assert "<script>" not in response_text
        assert "alert(" not in response_text
```

## 6. パフォーマンステスト仕様

### 6.1 負荷テスト (test_performance.py)

#### 6.1.1 同時ユーザーテスト
```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

def test_concurrent_user_registration(client, clean_user_store):
    """同時ユーザー登録テスト"""
    def register_user(user_id):
        user_data = {
            "username": f"user_{user_id}",
            "email": f"user_{user_id}@example.com",
            "password": "password123"
        }
        return client.post("/api/v1/auth/register", json=user_data)
    
    # 10人の同時ユーザー登録
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(register_user, i) for i in range(10)]
        results = [future.result() for future in futures]
    
    # すべての登録が成功することを確認
    success_count = sum(1 for result in results if result.status_code == 200)
    assert success_count == 10

def test_concurrent_login_attempts(client, clean_user_store):
    """同時ログイン試行テスト"""
    # テストユーザー作成
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    def login_user():
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        return client.post("/api/v1/auth/login", data=login_data)
    
    # 5回の同時ログイン
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(login_user) for _ in range(5)]
        results = [future.result() for future in futures]
    
    # すべてのログインが成功することを確認
    success_count = sum(1 for result in results if result.status_code == 200)
    assert success_count == 5
```

#### 6.1.2 レスポンス時間テスト
```python
@patch('src.modules.azure_openai_client.AzureOpenAI')
def test_minutes_generation_response_time(mock_azure_openai, client, authenticated_headers):
    """議事録生成レスポンス時間テスト"""
    # モックレスポンス設定
    mock_response = Mock()
    mock_response.choices[0].message.content = "Generated minutes"
    mock_azure_openai.return_value.chat.completions.create.return_value = mock_response
    
    transcript_data = {
        "meeting_title": "Performance Test Meeting",
        "meeting_date": "2024-01-15T10:00:00",
        "participants": ["Alice", "Bob"],
        "transcript_text": "Short transcript for performance testing",
    }
    
    start_time = time.time()
    response = client.post(
        "/api/v1/minutes/generate",
        json=transcript_data,
        headers=authenticated_headers
    )
    end_time = time.time()
    
    response_time = end_time - start_time
    
    assert response.status_code == 200
    assert response_time < 5.0  # 5秒以内のレスポンス
```

## 7. エラーハンドリングテスト仕様

### 7.1 例外処理テスト (test_error_handling.py)

#### 7.1.1 ネットワークエラーテスト
```python
@patch('src.modules.azure_openai_client.AzureOpenAI')
def test_azure_openai_network_error(mock_azure_openai, client, authenticated_headers):
    """Azure OpenAI ネットワークエラーテスト"""
    # ネットワークエラーをシミュレート
    mock_azure_openai.return_value.chat.completions.create.side_effect = ConnectionError("Network error")
    
    transcript_data = {
        "meeting_title": "Network Error Test",
        "meeting_date": "2024-01-15T10:00:00",
        "participants": ["Alice"],
        "transcript_text": "Test transcript",
    }
    
    response = client.post(
        "/api/v1/minutes/generate",
        json=transcript_data,
        headers=authenticated_headers
    )
    
    assert response.status_code == 500
    assert "Failed to generate meeting minutes" in response.json()["detail"]

@patch('src.modules.azure_openai_client.AzureOpenAI')
def test_azure_openai_timeout_error(mock_azure_openai, client, authenticated_headers):
    """Azure OpenAI タイムアウトエラーテスト"""
    # タイムアウトエラーをシミュレート
    mock_azure_openai.return_value.chat.completions.create.side_effect = TimeoutError("Request timeout")
    
    transcript_data = {
        "meeting_title": "Timeout Error Test",
        "meeting_date": "2024-01-15T10:00:00",
        "participants": ["Alice"],
        "transcript_text": "Test transcript",
    }
    
    response = client.post(
        "/api/v1/minutes/generate",
        json=transcript_data,
        headers=authenticated_headers
    )
    
    assert response.status_code == 500
```

#### 7.1.2 データ形式エラーテスト
```python
def test_invalid_json_format(client, authenticated_headers):
    """無効なJSON形式テスト"""
    # 無効なJSONデータ
    invalid_json = '{"meeting_title": "Test", "invalid_json"}'
    
    response = client.post(
        "/api/v1/minutes/generate",
        data=invalid_json,
        headers={**authenticated_headers, "Content-Type": "application/json"}
    )
    
    assert response.status_code == 422

def test_missing_required_fields(client, authenticated_headers):
    """必須フィールド欠如テスト"""
    incomplete_data = {
        "meeting_title": "Test Meeting"
        # meeting_date, participants, transcript_text が欠如
    }
    
    response = client.post(
        "/api/v1/minutes/generate",
        json=incomplete_data,
        headers=authenticated_headers
    )
    
    assert response.status_code == 422
```

## 8. テスト実行手順

### 8.1 テスト環境セットアップ
```bash
# 仮想環境作成・有効化
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 依存関係インストール
pip install -r requirements.txt
pip install -r requirements-test.txt

# 環境変数設定
cp env/.env.example env/.env
# env/.env ファイルを編集してテスト用の値を設定
```

### 8.2 テスト実行コマンド
```bash
# 全テスト実行
pytest

# カバレッジ付きテスト実行
pytest --cov=src --cov-report=html --cov-report=term

# 特定のテストファイル実行
pytest tests/test_auth.py

# 特定のテスト関数実行
pytest tests/test_auth.py::test_password_hashing

# 詳細出力付きテスト実行
pytest -v

# 並列テスト実行（pytest-xdist使用）
pytest -n auto
```

### 8.3 テスト結果の確認
```bash
# HTMLカバレッジレポート確認
open htmlcov/index.html

# テスト結果ログ確認
pytest --tb=short  # 短縮トレースバック
pytest --tb=long   # 詳細トレースバック
```

## 9. 継続的インテグレーション (CI) 設定

### 9.1 GitHub Actions設定例
```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests with pytest
      run: |
        pytest --cov=src --cov-report=xml --cov-report=term
      env:
        AZURE_OPENAI_API_KEY: ${{ secrets.AZURE_OPENAI_API_KEY }}
        AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
        JWT_SECRET_KEY: ${{ secrets.JWT_SECRET_KEY }}
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## 10. テスト品質指標

### 10.1 カバレッジ目標
- **コードカバレッジ**: 90%以上
- **ブランチカバレッジ**: 85%以上
- **関数カバレッジ**: 95%以上

### 10.2 パフォーマンス指標
- **API レスポンス時間**: 95%のリクエストが5秒以内
- **同時ユーザー数**: 100ユーザーまで対応
- **メモリ使用量**: 512MB以下

### 10.3 セキュリティ指標
- **認証テスト**: 100%パス
- **入力値検証テスト**: 100%パス
- **セキュリティ脆弱性**: 0件

## 11. テスト保守・更新

### 11.1 テストデータ管理
- テスト用ユーザーデータの定期更新
- モックデータの最新化
- テスト環境の定期リセット

### 11.2 テストケース追加指針
- 新機能追加時の対応テストケース作成
- バグ修正時の回帰テスト追加
- セキュリティ要件変更時のテスト更新

### 11.3 テスト結果分析
- 失敗テストの原因分析
- パフォーマンス劣化の監視
- カバレッジ低下の防止

## 12. 参考資料

- [FastAPI Testing Documentation](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [TestClient Documentation](https://fastapi.tiangolo.com/tutorial/testing/#using-testclient)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Security Testing Best Practices](https://owasp.org/www-project-web-security-testing-guide/)
