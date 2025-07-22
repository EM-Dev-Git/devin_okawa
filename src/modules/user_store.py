from typing import Dict, Optional
from datetime import datetime
import uuid

class UserStore:
    def __init__(self):
        self._users: Dict[str, Dict] = {}
        self._users_by_email: Dict[str, str] = {}
    
    def create_user(self, username: str, email: str, hashed_password: str) -> Dict:
        if username in self._users:
            raise ValueError("Username already exists")
        if email in self._users_by_email:
            raise ValueError("Email already exists")
        
        user_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        user = {
            "id": user_id,
            "username": username,
            "email": email,
            "hashed_password": hashed_password,
            "is_active": True,
            "created_at": now,
            "updated_at": now
        }
        
        self._users[username] = user
        self._users_by_email[email] = username
        
        return user
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        return self._users.get(username)
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        username = self._users_by_email.get(email)
        if username:
            return self._users.get(username)
        return None
    
    def update_user(self, username: str, **kwargs) -> Optional[Dict]:
        if username not in self._users:
            return None
        
        user = self._users[username]
        
        if "email" in kwargs and kwargs["email"] != user["email"]:
            if kwargs["email"] in self._users_by_email:
                raise ValueError("Email already exists")
            del self._users_by_email[user["email"]]
            self._users_by_email[kwargs["email"]] = username
        
        for key, value in kwargs.items():
            if key in user:
                user[key] = value
        
        user["updated_at"] = datetime.utcnow()
        return user
    
    def delete_user(self, username: str) -> bool:
        if username not in self._users:
            return False
        
        user = self._users[username]
        del self._users[username]
        del self._users_by_email[user["email"]]
        
        return True
    
    def clear_all_users(self):
        """テスト用: すべてのユーザーを削除"""
        self._users.clear()
        self._users_by_email.clear()

user_store = UserStore()
