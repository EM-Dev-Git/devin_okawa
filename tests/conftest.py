import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.modules.user_store import user_store
from src.modules.auth import create_access_token
from datetime import timedelta

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def clean_user_store():
    user_store.clear_all_users()
    yield user_store
    user_store.clear_all_users()

@pytest.fixture
def test_user(clean_user_store):
    from src.modules.auth import create_user
    user = create_user("testuser", "test@example.com", "testpassword123")
    return user

@pytest.fixture
def auth_headers(test_user):
    access_token = create_access_token(
        data={"sub": test_user["username"]},
        expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def sample_transcript():
    from datetime import datetime
    return {
        "meeting_title": "Weekly Team Meeting",
        "meeting_date": "2024-01-15T10:00:00",
        "participants": ["Alice", "Bob", "Charlie"],
        "transcript_text": "Alice: Let's start the meeting. Bob: I have an update on the project. Charlie: The deadline is next week.",
        "additional_notes": "Important decisions were made"
    }
