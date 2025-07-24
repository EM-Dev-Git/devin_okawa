import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)

def test_root_endpoint():
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "議事録生成API"
    assert data["version"] == "1.0.0"

def test_health_check():
    """ヘルスチェックエンドポイントのテスト"""
    response = client.get("/minutes/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "minutes-api"

@patch('src.modules.transcript_processor.TranscriptProcessor.process_transcript')
def test_generate_minutes_endpoint(mock_process):
    """議事録生成エンドポイントのテスト"""
    from src.schemas.minutes import MinutesResponse
    from datetime import datetime
    
    mock_response = MinutesResponse(
        id="test_001",
        title="テスト会議",
        content="生成された議事録",
        created_at=datetime.utcnow(),
        participants=["田中", "佐藤"]
    )
    mock_process.return_value = mock_response
    
    request_data = {
        "content": "テストトランスクリプト",
        "meeting_title": "テスト会議",
        "participants": ["田中", "佐藤"]
    }
    
    response = client.post("/minutes/generate", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == "test_001"
    assert data["title"] == "テスト会議"
    assert data["content"] == "生成された議事録"

def test_generate_minutes_invalid_request():
    """無効なリクエストのテスト"""
    response = client.post("/minutes/generate", json={})
    assert response.status_code == 422  # Validation error

@patch('src.modules.transcript_processor.TranscriptProcessor.process_transcript')
def test_generate_minutes_server_error(mock_process):
    """サーバーエラーのテスト"""
    mock_process.side_effect = Exception("処理エラー")
    
    request_data = {
        "content": "テストトランスクリプト"
    }
    
    response = client.post("/minutes/generate", json=request_data)
    assert response.status_code == 500
    
    data = response.json()
    assert "議事録生成に失敗しました" in data["detail"]
