import openai
from typing import Dict, Any
from ..config import settings
from .logger import get_logger

logger = get_logger(__name__)

openai.api_key = settings.openai_api_key


class TranscriptProcessor:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
    
    def process_transcript(self, transcript: str, meeting_info: Dict[str, Any] = None) -> str:
        logger.info("トランスクリプト処理開始")
        
        prompt = self._create_prompt(transcript, meeting_info)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは会議の議事録作成の専門家です。与えられたトランスクリプトから、構造化された日本語の議事録を作成してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            generated_minutes = response.choices[0].message.content
            logger.info("議事録生成完了")
            return generated_minutes
            
        except Exception as e:
            logger.error(f"OpenAI API エラー: {str(e)}")
            raise Exception(f"議事録生成中にエラーが発生しました: {str(e)}")
    
    def _create_prompt(self, transcript: str, meeting_info: Dict[str, Any] = None) -> str:
        base_prompt = """
以下のトランスクリプトから、構造化された議事録を作成してください。

【出力形式】

- 会議名: 
- 日時: 
- 場所: 
- 参加者: 

- 討議内容: 
- 主な意見: 

- 

| 項目 | 担当者 | 期限 |
|------|--------|------|
|      |        |      |

- 

【トランスクリプト】
"""
        
        if meeting_info:
            base_prompt += f"\n【会議情報】\n"
            for key, value in meeting_info.items():
                base_prompt += f"- {key}: {value}\n"
        
        base_prompt += f"\n{transcript}"
        
        return base_prompt
