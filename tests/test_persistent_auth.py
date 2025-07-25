import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.modules.user_store import user_store
import os
import tempfile

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_user_store():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        test_storage_file = tmp.name
    
    original_storage_file = user_store.storage_file
    user_store.storage_file = test_storage_file
    user_store.users = {}
    user_store.refresh_tokens = {}
    
    yield
    
    user_store.storage_file = original_storage_file
    if os.path.exists(test_storage_file):
        os.unlink(test_storage_file)

def test_user_registration():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["is_active"] == True

def test_user_login_with_remember_me():
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    })
    
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword123",
        "remember_me": True
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_refresh_token():
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    })
    
    login_response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword123",
        "remember_me": False
    })
    refresh_token = login_response.json()["refresh_token"]
    
    response = client.post("/auth/refresh", json={
        "refresh_token": refresh_token
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_protected_endpoint_with_auth():
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    })
    
    login_response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword123"
    })
    access_token = login_response.json()["access_token"]
    
    response = client.post(
        "/api/generate-minutes",
        json={
            "content": "Test meeting transcript",
            "meeting_title": "Test Meeting",
            "participants": ["User1", "User2"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

def test_logout():
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    })
    
    login_response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword123"
    })
    tokens = login_response.json()
    
    response = client.post(
        "/auth/logout",
        json={"refresh_token": tokens["refresh_token"]},
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    assert response.status_code == 200
    
    refresh_response = client.post("/auth/refresh", json={
        "refresh_token": tokens["refresh_token"]
    })
    assert refresh_response.status_code == 401
