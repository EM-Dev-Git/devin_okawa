import pytest
from src.transcription.parser import TranscriptionParser, TranscriptionSegment
from src.transcription.preprocessor import TranscriptionPreprocessor

class TestTranscriptionParser:
    def setup_method(self):
        self.parser = TranscriptionParser()
    
    def test_parse_basic_transcription(self):
        text = """司会：本日はありがとうございます。
田中：よろしくお願いします。
佐藤：こちらこそ、よろしくお願いします。"""
        
        segments = self.parser.parse_transcription(text)
        
        assert len(segments) == 3
        assert segments[0].speaker == "司会"
        assert segments[0].content == "本日はありがとうございます。"
        assert segments[1].speaker == "田中"
        assert segments[1].content == "よろしくお願いします。"
    
    def test_parse_with_timestamp(self):
        text = "[10:30:15] 司会：会議を開始します。"
        
        segments = self.parser.parse_transcription(text)
        
        assert len(segments) == 1
        assert segments[0].speaker == "司会"
        assert segments[0].timestamp == "10:30:15"
        assert segments[0].content == "会議を開始します。"
    
    def test_group_by_speaker(self):
        segments = [
            TranscriptionSegment("田中", None, "最初の発言"),
            TranscriptionSegment("佐藤", None, "佐藤の発言"),
            TranscriptionSegment("田中", None, "田中の二回目の発言")
        ]
        
        grouped = self.parser.group_by_speaker(segments)
        
        assert "田中" in grouped
        assert "佐藤" in grouped
        assert len(grouped["田中"]) == 2
        assert len(grouped["佐藤"]) == 1

class TestTranscriptionPreprocessor:
    def setup_method(self):
        self.preprocessor = TranscriptionPreprocessor()
    
    def test_clean_text(self):
        text = "えー、そのー、今日は（笑）よろしくお願いします。"
        cleaned = self.preprocessor.clean_text(text)
        
        assert "えー" not in cleaned
        assert "そのー" not in cleaned
        assert "（笑）" not in cleaned
        assert "よろしくお願いします" in cleaned
    
    def test_normalize_speakers(self):
        text = "司会者：本日はありがとうございます。"
        normalized = self.preprocessor.normalize_speakers(text)
        
        assert "司会：" in normalized
