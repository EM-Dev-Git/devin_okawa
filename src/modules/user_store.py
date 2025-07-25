import json
import os
from typing import Dict, Optional
from datetime import datetime
from src.schemas.auth import UserInDB, UserCreate
import uuid

class UserStore:
    def __init__(self, storage_file: str = "users.json"):
        self.storage_file = storage_file
        self.refresh_tokens: Dict[str, str] = {}
        self._load_users()
    
    def _load_users(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.users = {k: UserInDB(**v) for k, v in data.get('users', {}).items()}
                    self.refresh_tokens = data.get('refresh_tokens', {})
            except (json.JSONDecodeError, KeyError):
                self.users = {}
                self.refresh_tokens = {}
        else:
            self.users = {}
            self.refresh_tokens = {}
    
    def _save_users(self):
        data = {
            'users': {k: v.dict() for k, v in self.users.items()},
            'refresh_tokens': self.refresh_tokens
        }
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    def get_user(self, username: str) -> Optional[UserInDB]:
        return self.users.get(username)
    
    def create_user(self, user_data: UserCreate, hashed_password: str) -> UserInDB:
        user_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        user = UserInDB(
            id=user_id,
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=True,
            created_at=now,
            updated_at=now
        )
        
        self.users[user_data.username] = user
        self._save_users()
        return user
    
    def store_refresh_token(self, username: str, refresh_token: str):
        self.refresh_tokens[refresh_token] = username
        self._save_users()
    
    def get_user_by_refresh_token(self, refresh_token: str) -> Optional[str]:
        return self.refresh_tokens.get(refresh_token)
    
    def revoke_refresh_token(self, refresh_token: str):
        if refresh_token in self.refresh_tokens:
            del self.refresh_tokens[refresh_token]
            self._save_users()
    
    def revoke_all_user_tokens(self, username: str):
        tokens_to_remove = [token for token, user in self.refresh_tokens.items() if user == username]
        for token in tokens_to_remove:
            del self.refresh_tokens[token]
        self._save_users()

user_store = UserStore()
