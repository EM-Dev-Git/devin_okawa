import pytest
from config import settings, Settings

def test_settings_import():
    """設定ファイルのインポートテスト"""
    assert settings is not None
    assert isinstance(settings, Settings)

def test_required_fields():
    """必須フィールドの存在確認"""
    try:
        assert hasattr(settings, 'azure_openai_api_key')
        assert hasattr(settings, 'azure_openai_model')
        assert hasattr(settings, 'azure_openai_version')
        assert hasattr(settings, 'azure_openai_endpoint')
    except Exception as e:
        assert "azure_openai_api_key" in str(e) or "field required" in str(e)

def test_config_class():
    """Config クラスの設定確認"""
    assert Settings.Config.env_file == "env/.env"
