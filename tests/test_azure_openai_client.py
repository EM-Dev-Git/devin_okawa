import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.modules.azure_openai_client import AzureOpenAIClient

@pytest.fixture
def mock_settings():
    """モック設定"""
    with patch('src.modules.azure_openai_client.settings') as mock:
        mock.azure_openai_api_key = "test_key"
        mock.azure_openai_model = "gpt-4"
        mock.azure_openai_version = "2023-12-01-preview"
        mock.azure_openai_endpoint = "https://test.openai.azure.com/"
        yield mock

@pytest.fixture
def client(mock_settings):
    """テスト用クライアント"""
    with patch('src.modules.azure_openai_client.AzureOpenAI'):
        return AzureOpenAIClient()

def test_client_initialization(mock_settings):
    """クライアント初期化のテスト"""
    with patch('src.modules.azure_openai_client.AzureOpenAI') as mock_azure:
        client = AzureOpenAIClient()
        assert client.model == "gpt-4"
        assert client.logger is not None
        mock_azure.assert_called_once()

@pytest.mark.asyncio
async def test_generate_minutes_success(client):
    """議事録生成成功のテスト"""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "生成された議事録"
    
    client.client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    result = await client.generate_minutes("テストトランスクリプト")
    assert result == "生成された議事録"

@pytest.mark.asyncio
async def test_generate_minutes_error(client):
    """議事録生成エラーのテスト"""
    client.client.chat.completions.create = AsyncMock(side_effect=Exception("API エラー"))
    
    with pytest.raises(Exception) as exc_info:
        await client.generate_minutes("テストトランスクリプト")
    
    assert "API エラー" in str(exc_info.value)
