from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.config import settings
from src.schemas.auth import UserInDB, TokenData
from src.modules.user_store import user_store
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = user_store.get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
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

def create_refresh_token(username: str, remember_me: bool = False) -> str:
    if remember_me:
        expire_days = settings.jwt_remember_me_expire_days
    else:
        expire_days = settings.jwt_refresh_expire_days
    
    expire = datetime.utcnow() + timedelta(days=expire_days)
    refresh_token = str(uuid.uuid4())
    
    user_store.store_refresh_token(username, refresh_token)
    return refresh_token

def verify_token(token: str) -> Optional[TokenData]:
    try:
        if user_store.is_token_blacklisted(token):
            return None
            
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        return None

def refresh_access_token(refresh_token: str) -> Optional[dict]:
    username = user_store.get_user_by_refresh_token(refresh_token)
    if not username:
        return None
    
    user = user_store.get_user(username)
    if not user or not user.is_active:
        return None
    
    access_token_expires = timedelta(minutes=settings.jwt_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    new_refresh_token = create_refresh_token(username)
    user_store.revoke_refresh_token(refresh_token)
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

def revoke_refresh_token(refresh_token: str):
    user_store.revoke_refresh_token(refresh_token)

def revoke_all_user_tokens(username: str):
    user_store.revoke_all_user_tokens(username)
