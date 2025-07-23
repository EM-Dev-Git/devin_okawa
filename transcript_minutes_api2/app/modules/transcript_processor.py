import openai
from typing import Dict, Any
from ..config import settings
from ..modules.logger import get_logger

logger = get_logger(__name__)

openai.api_key = settings.openai_api_key


class TranscriptProcessor:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
    
    async def process_transcript(self, transcript: str, title: str = "会議") -> Dict[str, Any]:
        try:
            logger.info(f"トランスクリプト処理開始: {title}")
            
            prompt = f"""
あなたは会議の議事録作成の専門家です。
以下のトランスクリプトから、構造化された議事録を作成してください。

【出力形式】
1. 会議概要
2. 参加者
3. 議題と討議内容
4. 決定事項
5. アクションアイテム
6. 次回予定

【トランスクリプト】
{transcript}

日本語で回答してください。
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは会議の議事録作成の専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            generated_minutes = response.choices[0].message.content
            
            logger.info(f"トランスクリプト処理完了: {title}")
            
            return {
                "title": title,
                "transcript": transcript,
                "generated_minutes": generated_minutes,
                "processing_status": "success"
            }
            
        except Exception as e:
            logger.error(f"トランスクリプト処理エラー: {str(e)}")
            return {
                "title": title,
                "transcript": transcript,
                "generated_minutes": f"議事録生成中にエラーが発生しました: {str(e)}",
                "processing_status": "error"
            }


transcript_processor = TranscriptProcessor()
