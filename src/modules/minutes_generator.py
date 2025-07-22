import json
import logging
from datetime import datetime
from src.modules.azure_openai_client import AzureOpenAIClient
from src.schemas.transcript import TranscriptInput
from src.schemas.minutes import MinutesOutput

logger = logging.getLogger(__name__)

class MinutesGenerator:
    def __init__(self):
        self.azure_client = AzureOpenAIClient()
    
    def generate_minutes(self, transcript_data: TranscriptInput) -> MinutesOutput:
        """トランスクリプトデータから議事録を生成"""
        try:
            logger.info(f"Starting minutes generation for: {transcript_data.meeting_title}")
            
            prompt = self._create_prompt(transcript_data)
            
            generated_content = self.azure_client.generate_minutes(prompt)
            
            minutes_data = self._parse_generated_content(generated_content, transcript_data)
            
            logger.info("Minutes generation completed successfully")
            return minutes_data
            
        except Exception as e:
            logger.error(f"Error in minutes generation: {str(e)}")
            raise
    
    def _create_prompt(self, transcript_data: TranscriptInput) -> str:
        """議事録生成用のプロンプトを作成"""
        prompt = f"""
以下の会議トランスクリプトから、構造化された議事録を作成してください。

会議情報:
- タイトル: {transcript_data.meeting_title}
- 日時: {transcript_data.meeting_date.isoformat()}
- 参加者: {', '.join(transcript_data.participants)}

トランスクリプト:
{transcript_data.transcript_text}

追加メモ:
{transcript_data.additional_notes or 'なし'}

以下のJSON形式で議事録を作成してください:
{{
    "summary": "会議の要約",
    "key_points": ["重要なポイント1", "重要なポイント2"],
    "action_items": ["アクションアイテム1", "アクションアイテム2"],
    "next_meeting": "次回会議の日時（ISO形式、未定の場合はnull）"
}}

JSON形式のみで回答してください。
"""
        return prompt
    
    def _parse_generated_content(self, content: str, transcript_data: TranscriptInput) -> MinutesOutput:
        """生成されたコンテンツをパースしてMinutesOutputに変換"""
        try:
            parsed_data = json.loads(content)
            
            next_meeting = None
            if parsed_data.get("next_meeting"):
                try:
                    next_meeting = datetime.fromisoformat(parsed_data["next_meeting"])
                except (ValueError, TypeError):
                    next_meeting = None
            
            minutes = MinutesOutput(
                meeting_title=transcript_data.meeting_title,
                meeting_date=transcript_data.meeting_date,
                participants=transcript_data.participants,
                summary=parsed_data.get("summary", ""),
                key_points=parsed_data.get("key_points", []),
                action_items=parsed_data.get("action_items", []),
                next_meeting=next_meeting,
                generated_at=datetime.utcnow()
            )
            
            return minutes
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            return self._create_fallback_minutes(transcript_data, content)
        except Exception as e:
            logger.error(f"Error parsing generated content: {str(e)}")
            raise
    
    def _create_fallback_minutes(self, transcript_data: TranscriptInput, content: str) -> MinutesOutput:
        """JSONパースに失敗した場合のフォールバック議事録"""
        return MinutesOutput(
            meeting_title=transcript_data.meeting_title,
            meeting_date=transcript_data.meeting_date,
            participants=transcript_data.participants,
            summary=content[:500] + "..." if len(content) > 500 else content,
            key_points=["議事録の自動生成中にエラーが発生しました"],
            action_items=["生成された内容を手動で確認してください"],
            next_meeting=None,
            generated_at=datetime.utcnow()
        )
