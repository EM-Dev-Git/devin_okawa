import pytest
from datetime import datetime, timedelta
from src.modules.auth import (
    verify_password, get_password_hash, authenticate_user,
    create_access_token, verify_token, create_user
)
from src.schemas.auth import TokenData
from fastapi import HTTPException

class TestAuth:
    
    def test_password_hashing(self):
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False
    
    def test_create_user(self, clean_user_store):
        user = create_user("testuser", "test@example.com", "password123")
        
        assert user["username"] == "testuser"
        assert user["email"] == "test@example.com"
        assert verify_password("password123", user["hashed_password"])
        assert user["is_active"] is True
    
    def test_authenticate_user_success(self, test_user):
        result = authenticate_user("testuser", "testpassword123")
        assert result == test_user
    
    def test_authenticate_user_wrong_password(self, test_user):
        result = authenticate_user("testuser", "wrongpassword")
        assert result is False
    
    def test_authenticate_user_nonexistent(self, clean_user_store):
        result = authenticate_user("nonexistent", "password")
        assert result is False
    
    def test_create_access_token(self):
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_with_expiry(self):
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=15)
        token = create_access_token(data, expires_delta)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_token_success(self, test_user):
        token = create_access_token({"sub": test_user["username"]})
        credentials_exception = HTTPException(status_code=401, detail="Invalid")
        
        token_data = verify_token(token, credentials_exception)
        
        assert isinstance(token_data, TokenData)
        assert token_data.username == test_user["username"]
    
    def test_verify_token_invalid(self):
        invalid_token = "invalid.token.here"
        credentials_exception = HTTPException(status_code=401, detail="Invalid")
        
        with pytest.raises(HTTPException):
            verify_token(invalid_token, credentials_exception)
    
    def test_verify_token_expired(self, test_user):
        expired_token = create_access_token(
            {"sub": test_user["username"]},
            expires_delta=timedelta(seconds=-1)
        )
        credentials_exception = HTTPException(status_code=401, detail="Invalid")
        
        with pytest.raises(HTTPException):
            verify_token(expired_token, credentials_exception)
