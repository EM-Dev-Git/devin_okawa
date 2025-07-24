import pytest
from datetime import datetime
from src.schemas.transcript import TranscriptRequest
from src.schemas.minutes import MinutesResponse

def test_transcript_request_creation():
    """TranscriptRequest スキーマのテスト"""
    request = TranscriptRequest(
        content="テストトランスクリプト",
        meeting_title="テスト会議",
        participants=["田中", "佐藤"]
    )
    assert request.content == "テストトランスクリプト"
    assert request.meeting_title == "テスト会議"
    assert request.participants == ["田中", "佐藤"]

def test_transcript_request_minimal():
    """TranscriptRequest 最小構成のテスト"""
    request = TranscriptRequest(content="テストトランスクリプト")
    assert request.content == "テストトランスクリプト"
    assert request.meeting_title is None
    assert request.participants is None

def test_minutes_response_creation():
    """MinutesResponse スキーマのテスト"""
    now = datetime.utcnow()
    response = MinutesResponse(
        id="test_001",
        title="テスト議事録",
        content="## 議事録内容",
        created_at=now,
        participants=["田中", "佐藤"]
    )
    assert response.id == "test_001"
    assert response.title == "テスト議事録"
    assert response.content == "## 議事録内容"
    assert response.created_at == now
    assert response.participants == ["田中", "佐藤"]

def test_transcript_request_validation():
    """TranscriptRequest バリデーションテスト"""
    with pytest.raises(ValueError):
        TranscriptRequest()  # content が必須
