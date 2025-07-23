import openai
from typing import Dict, Any
from ..config import settings
from .logger import get_logger

logger = get_logger(__name__)

openai.api_key = settings.openai_api_key


class TranscriptProcessor:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        logger.info("TranscriptProcessor初期化完了")

    async def analyze_transcript(self, transcript: str, header: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("トランスクリプト解析開始")
            
            prompt = f"""
以下の会議トランスクリプトを分析し、構造化された議事録を生成してください。

会議情報:
- タイトル: {header.get('title', '未設定')}
- 日時: {header.get('date', '未設定')}
- 場所: {header.get('location', '未設定')}
- 参加者: {', '.join(header.get('participants', []))}
- 司会者: {header.get('facilitator', '未設定')}

トランスクリプト:
{transcript}

以下の形式でJSONレスポンスを生成してください:
{{
    "summary": "会議の要約",
    "agenda_items": [
        {{
            "title": "議題タイトル",
            "discussion": "議論内容の要約",
            "decisions": ["決定事項1", "決定事項2"],
            "action_items": [
                {{
                    "task": "タスク内容",
                    "assignee": "担当者",
                    "deadline": "期限"
                }}
            ]
        }}
    ],
    "next_meeting": "次回会議の予定",
    "notes": "その他の注意事項"
}}
"""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは会議の議事録作成の専門家です。日本語で正確で構造化された議事録を作成してください。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )

            result = response.choices[0].message.content
            logger.info("トランスクリプト解析完了")
            
            return {
                "analysis": result,
                "token_usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }

        except Exception as e:
            logger.error(f"トランスクリプト解析エラー: {str(e)}")
            raise Exception(f"OpenAI API エラー: {str(e)}")
