import bcrypt
from typing import Optional, Dict, Any
from src.modules.user_store import user_store
import logging

logger = logging.getLogger(__name__)

def get_password_hash(password: str) -> str:
    if not password:
        raise ValueError("Password cannot be empty")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    user = user_store.get_user_by_username(username)
    if not user:
        return None
    
    if not verify_password(password, user['hashed_password']):
        return None
    
    return user

def register_user(username: str, email: str, password: str) -> Dict[str, Any]:
    if user_store.get_user_by_username(username):
        raise ValueError("Username already exists")
    
    if user_store.get_user_by_email(email):
        raise ValueError("Email already exists")
    
    hashed_password = get_password_hash(password)
    return user_store.create_user(username, email, hashed_password)
