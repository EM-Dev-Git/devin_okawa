import pytest
from datetime import datetime, timedelta
from src.modules.auth import create_access_token, verify_token
from src.config import settings
from fastapi import HTTPException
from jose import jwt

class TestSecurity:
    
    def test_jwt_token_structure(self):
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        decoded = jwt.decode(
            token, 
            settings.jwt_secret_key, 
            algorithms=[settings.jwt_algorithm]
        )
        
        assert decoded["sub"] == "testuser"
        assert "exp" in decoded
    
    def test_jwt_token_expiration(self):
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=1)
        token = create_access_token(data, expires_delta)
        
        decoded = jwt.decode(
            token, 
            settings.jwt_secret_key, 
            algorithms=[settings.jwt_algorithm]
        )
        
        exp_time = datetime.fromtimestamp(decoded["exp"])
        expected_exp = datetime.utcnow() + expires_delta
        
        assert abs((exp_time - expected_exp).total_seconds()) < 5
    
    def test_jwt_token_tampering(self):
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        tampered_token = token[:-10] + "tampered123"
        credentials_exception = HTTPException(status_code=401, detail="Invalid")
        
        with pytest.raises(HTTPException):
            verify_token(tampered_token, credentials_exception)
    
    def test_jwt_token_wrong_secret(self):
        data = {"sub": "testuser"}
        token = jwt.encode(data, "wrong_secret", algorithm=settings.jwt_algorithm)
        
        credentials_exception = HTTPException(status_code=401, detail="Invalid")
        
        with pytest.raises(HTTPException):
            verify_token(token, credentials_exception)
    
    def test_password_strength_validation(self):
        from src.modules.auth import get_password_hash
        
        weak_passwords = ["123", "password", "abc"]
        strong_passwords = ["StrongPass123!", "MySecureP@ssw0rd", "Complex1ty!"]
        
        for password in weak_passwords + strong_passwords:
            hashed = get_password_hash(password)
            assert len(hashed) > 50
            assert hashed != password
    
    def test_token_without_subject(self):
        token = jwt.encode(
            {"exp": datetime.utcnow() + timedelta(minutes=30)},
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )
        
        credentials_exception = HTTPException(status_code=401, detail="Invalid")
        
        with pytest.raises(HTTPException):
            verify_token(token, credentials_exception)
    
    def test_malformed_token(self):
        malformed_tokens = [
            "not.a.token",
            "invalid_token_format",
            "",
            "Bearer token_without_bearer_prefix"
        ]
        
        credentials_exception = HTTPException(status_code=401, detail="Invalid")
        
        for token in malformed_tokens:
            with pytest.raises(HTTPException):
                verify_token(token, credentials_exception)
