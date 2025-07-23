import openai
from typing import Dict, Any
from ..config import settings
from .logger import get_logger

logger = get_logger(__name__)

openai.api_key = settings.openai_api_key


class TranscriptProcessor:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
    
    async def analyze_transcript(self, transcript: str, header: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("トランスクリプト解析開始")
            
            prompt = self._create_analysis_prompt(transcript, header)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは会議の議事録作成の専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            analysis_result = response.choices[0].message.content
            
            logger.info("トランスクリプト解析完了")
            
            return {
                "analysis": analysis_result,
                "token_usage": response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            logger.error(f"トランスクリプト解析エラー: {str(e)}")
            raise Exception(f"OpenAI API エラー: {str(e)}")
    
    def _create_analysis_prompt(self, transcript: str, header: Dict[str, Any]) -> str:
        return f"""
以下のトランスクリプトから、構造化された議事録を作成してください。

【会議情報】
- タイトル: {header.get('title', '未設定')}
- 日時: {header.get('date', '未設定')}
- 場所: {header.get('location', '未設定')}
- 参加者: {', '.join(header.get('participants', []))}
- 進行: {header.get('facilitator', '未設定')}

【出力形式】
1. 会議概要
2. 参加者
3. 議題と討議内容
4. 決定事項
5. アクションアイテム（担当者・期限含む）
6. 次回予定

【トランスクリプト】
{transcript}

上記の形式で、簡潔で分かりやすい議事録を作成してください。
"""
