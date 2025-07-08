from typing import List, Dict
from datetime import datetime
from src.transcription.parser import TranscriptionSegment
from src.ai.summarizer import AISummarizer

class MinutesGenerator:
    def __init__(self):
        self.ai_summarizer = AISummarizer()
    
    def generate_minutes(self, segments: List[TranscriptionSegment], 
                        meeting_title: str = "会議", 
                        meeting_date: str = None) -> Dict[str, any]:
        """
        議事録を生成
        """
        if meeting_date is None:
            meeting_date = datetime.now().strftime("%Y年%m月%d日")
        
        summary_result = self.ai_summarizer.summarize_meeting(segments)
        action_items = self.ai_summarizer.extract_action_items(segments)
        
        participants = self._extract_participants(segments)
        
        minutes_data = {
            "meeting_title": meeting_title,
            "meeting_date": meeting_date,
            "participants": participants,
            "summary": summary_result.get("summary", ""),
            "action_items": action_items,
            "full_transcription": self._format_transcription(segments),
            "generated_at": datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        }
        
        return minutes_data
    
    def _extract_participants(self, segments: List[TranscriptionSegment]) -> List[str]:
        """
        参加者リストを抽出
        """
        speakers = set()
        for segment in segments:
            if segment.speaker and segment.speaker != "不明":
                speakers.add(segment.speaker)
        
        return sorted(list(speakers))
    
    def _format_transcription(self, segments: List[TranscriptionSegment]) -> str:
        """
        文字起こしを整形
        """
        formatted_lines = []
        current_speaker = None
        
        for segment in segments:
            if segment.speaker and segment.speaker != current_speaker:
                current_speaker = segment.speaker
                formatted_lines.append(f"\n**{current_speaker}**")
            
            timestamp_part = f"[{segment.timestamp}] " if segment.timestamp else ""
            formatted_lines.append(f"{timestamp_part}{segment.content}")
        
        return "\n".join(formatted_lines)
