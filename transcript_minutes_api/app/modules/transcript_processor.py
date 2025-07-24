import openai
from typing import Dict, Any
from ..config import settings
from .logger import get_logger

logger = get_logger(__name__)

openai.api_key = settings.openai_api_key


class TranscriptProcessor:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
    
    async def process_transcript(self, transcript: str, title: str = "") -> str:
        try:
            logger.info(f"Processing transcript for: {title}")
            
            prompt = self._create_prompt(transcript, title)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは議事録作成の専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            generated_minutes = response.choices[0].message.content
            logger.info("Transcript processing completed successfully")
            
            return generated_minutes
            
        except Exception as e:
            logger.error(f"Error processing transcript: {str(e)}")
            raise Exception(f"トランスクリプト処理中にエラーが発生しました: {str(e)}")
    
    def _create_prompt(self, transcript: str, title: str) -> str:
        return f"""
以下のトランスクリプトから、構造化された議事録を作成してください。

- 会議名: {title if title else "未設定"}
- 参加者: 
- 議題: 

1. 
2. 
3. 

- 
- 

- [ ] 担当者: 期限: 内容
- [ ] 担当者: 期限: 内容

- 
- 

{transcript}
"""


transcript_processor = TranscriptProcessor()
