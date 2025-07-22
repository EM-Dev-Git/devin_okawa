import pytest
from src.modules.user_store import UserStore
from datetime import datetime

class TestUserStore:
    
    def test_create_user_success(self):
        store = UserStore()
        user = store.create_user("testuser", "test@example.com", "hashed_password")
        
        assert user["username"] == "testuser"
        assert user["email"] == "test@example.com"
        assert user["hashed_password"] == "hashed_password"
        assert user["is_active"] is True
        assert isinstance(user["id"], str)
        assert isinstance(user["created_at"], datetime)
        assert isinstance(user["updated_at"], datetime)
    
    def test_create_user_duplicate_username(self):
        store = UserStore()
        store.create_user("testuser", "test1@example.com", "password1")
        
        with pytest.raises(ValueError, match="Username already exists"):
            store.create_user("testuser", "test2@example.com", "password2")
    
    def test_create_user_duplicate_email(self):
        store = UserStore()
        store.create_user("user1", "test@example.com", "password1")
        
        with pytest.raises(ValueError, match="Email already exists"):
            store.create_user("user2", "test@example.com", "password2")
    
    def test_get_user_by_username(self):
        store = UserStore()
        created_user = store.create_user("testuser", "test@example.com", "password")
        
        retrieved_user = store.get_user_by_username("testuser")
        assert retrieved_user == created_user
        
        assert store.get_user_by_username("nonexistent") is None
    
    def test_get_user_by_email(self):
        store = UserStore()
        created_user = store.create_user("testuser", "test@example.com", "password")
        
        retrieved_user = store.get_user_by_email("test@example.com")
        assert retrieved_user == created_user
        
        assert store.get_user_by_email("nonexistent@example.com") is None
    
    def test_update_user(self):
        store = UserStore()
        user = store.create_user("testuser", "test@example.com", "password")
        original_updated_at = user["updated_at"]
        
        updated_user = store.update_user("testuser", email="newemail@example.com")
        
        assert updated_user["email"] == "newemail@example.com"
        assert updated_user["updated_at"] > original_updated_at
        assert store.get_user_by_email("newemail@example.com") == updated_user
        assert store.get_user_by_email("test@example.com") is None
    
    def test_update_user_email_conflict(self):
        store = UserStore()
        store.create_user("user1", "email1@example.com", "password1")
        store.create_user("user2", "email2@example.com", "password2")
        
        with pytest.raises(ValueError, match="Email already exists"):
            store.update_user("user1", email="email2@example.com")
    
    def test_delete_user(self):
        store = UserStore()
        store.create_user("testuser", "test@example.com", "password")
        
        result = store.delete_user("testuser")
        assert result is True
        assert store.get_user_by_username("testuser") is None
        assert store.get_user_by_email("test@example.com") is None
        
        result = store.delete_user("nonexistent")
        assert result is False
    
    def test_clear_all_users(self):
        store = UserStore()
        store.create_user("user1", "email1@example.com", "password1")
        store.create_user("user2", "email2@example.com", "password2")
        
        store.clear_all_users()
        
        assert store.get_user_by_username("user1") is None
        assert store.get_user_by_username("user2") is None
        assert store.get_user_by_email("email1@example.com") is None
        assert store.get_user_by_email("email2@example.com") is None
