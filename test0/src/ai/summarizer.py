import openai
from typing import List, Dict
from config.settings import settings
from src.transcription.parser import TranscriptionSegment

class AISummarizer:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.AI_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
    
    def summarize_meeting(self, segments: List[TranscriptionSegment]) -> Dict[str, str]:
        """
        会議全体の要約を生成
        """
        full_text = self._segments_to_text(segments)
        
        prompt = f"""
以下の会議の文字起こしから、構造化された議事録を作成してください。

文字起こし:
{full_text}

以下の形式で出力してください：

[会議の目的と概要を簡潔に]

[議論された主要な議題をリスト形式で]

[会議で決定された事項をリスト形式で]

[今後のアクション項目と担当者をリスト形式で]

[その他の重要な情報]
"""
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "あなたは会議の議事録作成の専門家です。文字起こしから重要な情報を抽出し、構造化された議事録を作成してください。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return {
                "summary": response.choices[0].message.content,
                "status": "success"
            }
        
        except Exception as e:
            return {
                "summary": f"要約生成中にエラーが発生しました: {str(e)}",
                "status": "error"
            }
    
    def extract_action_items(self, segments: List[TranscriptionSegment]) -> List[Dict[str, str]]:
        """
        アクションアイテムを抽出
        """
        full_text = self._segments_to_text(segments)
        
        prompt = f"""
以下の会議の文字起こしから、アクションアイテム（今後の行動項目）を抽出してください。

文字起こし:
{full_text}

各アクションアイテムについて、以下の情報を抽出してください：
- アクション内容
- 担当者（明記されている場合）
- 期限（明記されている場合）

JSON形式で出力してください：
[
  {{
    "action": "アクション内容",
    "assignee": "担当者",
    "deadline": "期限"
  }}
]
"""
        
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "あなたは会議のアクションアイテム抽出の専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            import json
            action_items = json.loads(response.choices[0].message.content)
            return action_items
        
        except Exception as e:
            return [{"action": f"アクションアイテム抽出中にエラーが発生しました: {str(e)}", "assignee": "", "deadline": ""}]
    
    def _segments_to_text(self, segments: List[TranscriptionSegment]) -> str:
        """
        セグメントリストをテキストに変換
        """
        text_parts = []
        for segment in segments:
            speaker_part = f"{segment.speaker}：" if segment.speaker else ""
            timestamp_part = f"[{segment.timestamp}] " if segment.timestamp else ""
            text_parts.append(f"{timestamp_part}{speaker_part}{segment.content}")
        
        return "\n".join(text_parts)
