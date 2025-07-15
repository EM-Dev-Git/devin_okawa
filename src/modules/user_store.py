from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class UserStore:
    def __init__(self):
        self._users: Dict[str, Dict[str, Any]] = {}
        logger.info("UserStore initialized with empty memory dictionary")
    
    def create_user(self, username: str, email: str, hashed_password: str) -> Dict[str, Any]:
        if username in self._users:
            raise ValueError("Username already exists")
        
        user_data = {
            "username": username,
            "email": email,
            "hashed_password": hashed_password,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self._users[username] = user_data
        logger.info(f"User created: {username}")
        return {k: v for k, v in user_data.items() if k != 'hashed_password'}
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        return self._users.get(username)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        for user in self._users.values():
            if user['email'] == email:
                return user
        return None

user_store = UserStore()
