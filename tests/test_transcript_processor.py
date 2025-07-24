import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
from src.modules.transcript_processor import TranscriptProcessor
from src.schemas.transcript import TranscriptRequest
from src.schemas.minutes import MinutesResponse

@pytest.fixture
def processor():
    """テスト用プロセッサー"""
    with patch('src.modules.transcript_processor.AzureOpenAIClient'):
        return TranscriptProcessor()

@pytest.mark.asyncio
async def test_process_transcript_success(processor):
    """トランスクリプト処理成功のテスト"""
    processor.openai_client.generate_minutes = AsyncMock(return_value="生成された議事録")
    
    request = TranscriptRequest(
        content="テストトランスクリプト",
        meeting_title="テスト会議",
        participants=["田中", "佐藤"]
    )
    
    result = await processor.process_transcript(request)
    
    assert isinstance(result, MinutesResponse)
    assert result.title == "テスト会議"
    assert result.content == "生成された議事録"
    assert result.participants == ["田中", "佐藤"]
    assert result.id.startswith("minutes_")

@pytest.mark.asyncio
async def test_process_transcript_no_title(processor):
    """タイトルなしトランスクリプト処理のテスト"""
    processor.openai_client.generate_minutes = AsyncMock(return_value="生成された議事録")
    
    request = TranscriptRequest(content="テストトランスクリプト")
    
    result = await processor.process_transcript(request)
    
    assert result.title == "議事録"
    assert result.content == "生成された議事録"

@pytest.mark.asyncio
async def test_process_transcript_error(processor):
    """トランスクリプト処理エラーのテスト"""
    processor.openai_client.generate_minutes = AsyncMock(side_effect=Exception("処理エラー"))
    
    request = TranscriptRequest(content="テストトランスクリプト")
    
    with pytest.raises(Exception) as exc_info:
        await processor.process_transcript(request)
    
    assert "処理エラー" in str(exc_info.value)
