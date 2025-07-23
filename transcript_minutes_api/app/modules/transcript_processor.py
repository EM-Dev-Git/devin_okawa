import openai
from typing import Dict, Any
from ..config import settings
from ..schemas.minutes import MeetingHeader

class TranscriptProcessor:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)

    async def process_transcript(self, transcript: str, header: MeetingHeader) -> str:
        prompt = self._create_prompt(transcript, header)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは議事録作成の専門家です。与えられたトランスクリプトから構造化された議事録を作成してください。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API呼び出しエラー: {str(e)}")

    def _create_prompt(self, transcript: str, header: MeetingHeader) -> str:
        participants_str = "、".join(header.participants)
        absent_str = "、".join(header.absent_members) if header.absent_members else "なし"
        
        prompt = f"""
以下の会議情報とトランスクリプトから、構造化された議事録を作成してください。

【会議情報】
- 会議名: {header.title}
- 日時: {header.date}
- 場所: {header.location or "記載なし"}
- 参加者: {participants_str}
- 欠席者: {absent_str}
- 司会者: {header.facilitator or "記載なし"}

【トランスクリプト】
{transcript}

【出力形式】
以下の形式で議事録を作成してください：

- 会議名: 
- 日時: 
- 場所: 
- 参加者: 
- 欠席者: 
- 司会者: 

（主要な議題と討議内容を整理）

（会議で決定された事項）

（今後のアクション項目と担当者）

（次回会議の予定があれば記載）

（その他の重要な情報）
"""
        return prompt

transcript_processor = TranscriptProcessor()
