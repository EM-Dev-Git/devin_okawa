import re
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class TranscriptionSegment:
    speaker: Optional[str]
    timestamp: Optional[str]
    content: str
    
class TranscriptionParser:
    def __init__(self):
        self.speaker_pattern = r'^([A-Za-z\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]+)[:：]\s*'
        self.timestamp_pattern = r'\[(\d{2}:\d{2}:\d{2})\]'
    
    def parse_transcription(self, text: str) -> List[TranscriptionSegment]:
        """
        文字起こしテキストを解析してセグメントに分割
        """
        segments = []
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            timestamp_match = re.search(self.timestamp_pattern, line)
            timestamp = timestamp_match.group(1) if timestamp_match else None
            
            content = re.sub(self.timestamp_pattern, '', line).strip()
            
            speaker_match = re.match(self.speaker_pattern, content)
            speaker = speaker_match.group(1) if speaker_match else None
            
            if speaker:
                content = re.sub(self.speaker_pattern, '', content).strip()
            
            if content:
                segments.append(TranscriptionSegment(
                    speaker=speaker,
                    timestamp=timestamp,
                    content=content
                ))
        
        return segments
    
    def group_by_speaker(self, segments: List[TranscriptionSegment]) -> Dict[str, List[str]]:
        """
        話者別に発言をグループ化
        """
        grouped = {}
        for segment in segments:
            speaker = segment.speaker or "不明"
            if speaker not in grouped:
                grouped[speaker] = []
            grouped[speaker].append(segment.content)
        return grouped
    
    def extract_topics(self, segments: List[TranscriptionSegment]) -> List[str]:
        """
        議題や重要なトピックを抽出
        """
        topics = []
        topic_keywords = ['議題', 'アジェンダ', '案件', '項目', '話題', '検討事項']
        
        for segment in segments:
            content = segment.content
            for keyword in topic_keywords:
                if keyword in content:
                    topics.append(content)
                    break
        
        return topics
