import pytest
import tempfile
import os
from src.modules.user_store import UserStore
from src.schemas.auth import UserCreate

@pytest.fixture
def temp_user_store():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        storage_file = tmp.name
    
    store = UserStore(storage_file)
    yield store
    
    if os.path.exists(storage_file):
        os.unlink(storage_file)

def test_create_and_get_user(temp_user_store):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass"
    )
    
    created_user = temp_user_store.create_user(user_data, "hashed_password")
    retrieved_user = temp_user_store.get_user("testuser")
    
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "test@example.com"
    assert retrieved_user.hashed_password == "hashed_password"

def test_refresh_token_storage(temp_user_store):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass"
    )
    
    temp_user_store.create_user(user_data, "hashed_password")
    
    refresh_token = "test_refresh_token"
    temp_user_store.store_refresh_token("testuser", refresh_token)
    
    retrieved_username = temp_user_store.get_user_by_refresh_token(refresh_token)
    assert retrieved_username == "testuser"

def test_revoke_refresh_token(temp_user_store):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass"
    )
    
    temp_user_store.create_user(user_data, "hashed_password")
    
    refresh_token = "test_refresh_token"
    temp_user_store.store_refresh_token("testuser", refresh_token)
    temp_user_store.revoke_refresh_token(refresh_token)
    
    retrieved_username = temp_user_store.get_user_by_refresh_token(refresh_token)
    assert retrieved_username is None

def test_persistence_across_instances():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        storage_file = tmp.name
    
    try:
        store1 = UserStore(storage_file)
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="testpass"
        )
        store1.create_user(user_data, "hashed_password")
        
        store2 = UserStore(storage_file)
        retrieved_user = store2.get_user("testuser")
        
        assert retrieved_user is not None
        assert retrieved_user.username == "testuser"
        
    finally:
        if os.path.exists(storage_file):
            os.unlink(storage_file)
