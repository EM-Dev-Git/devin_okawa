import pytest
import logging
from src.modules.logger import setup_logger

def test_setup_logger():
    """ログ設定のテスト"""
    logger = setup_logger()
    assert logger is not None
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.INFO

def test_logger_handlers():
    """ログハンドラーの確認"""
    logger = setup_logger()
    assert len(logger.handlers) > 0
    
    console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
    assert len(console_handlers) > 0

def test_logger_format():
    """ログフォーマットの確認"""
    logger = setup_logger()
    handler = logger.handlers[0]
    formatter = handler.formatter
    assert formatter is not None
    assert '%(asctime)s' in formatter._fmt
    assert '%(name)s' in formatter._fmt
    assert '%(levelname)s' in formatter._fmt
    assert '%(message)s' in formatter._fmt
