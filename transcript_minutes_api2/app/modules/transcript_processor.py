from openai import AsyncOpenAI
from typing import Dict, Any
from ..config import settings
from .logger import get_logger

logger = get_logger(__name__)

class TranscriptProcessor:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def process_transcript(self, transcript: str) -> Dict[str, Any]:
        try:
            logger.info("トランスクリプト処理開始")
            
            prompt = self._create_prompt(transcript)
            
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは議事録作成の専門家です。与えられたトランスクリプトから構造化された議事録を作成してください。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            processed_data = self._parse_response(content)
            
            logger.info("トランスクリプト処理完了")
            return processed_data
            
        except Exception as e:
            logger.error(f"トランスクリプト処理エラー: {str(e)}")
            raise Exception(f"トランスクリプト処理に失敗しました: {str(e)}")

    def _create_prompt(self, transcript: str) -> str:
        return f"""
以下のトランスクリプトから議事録を作成してください。

【トランスクリプト】
{transcript}

【出力形式】
以下のJSON形式で出力してください：
{{
    "summary": "会議の概要",
    "agenda_items": [
        {{
            "title": "議題タイトル",
            "discussion": "議論内容",
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
    "next_meeting": "次回会議の予定"
}}
"""

    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            import json
            
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            parsed = json.loads(response)
            logger.info("OpenAI応答解析成功")
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析エラー: {str(e)}")
            return {
                "summary": "解析エラーが発生しました",
                "agenda_items": [],
                "next_meeting": ""
            }
        except Exception as e:
            logger.error(f"応答解析エラー: {str(e)}")
            return {
                "summary": "処理エラーが発生しました",
                "agenda_items": [],
                "next_meeting": ""
            }

transcript_processor = TranscriptProcessor()
