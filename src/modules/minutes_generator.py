from .azure_openai_client import AzureOpenAIClient
from src.config import settings
from src.schemas.transcript import TranscriptInput
from src.schemas.minutes import MinutesOutput
import logging
import json
import time

logger = logging.getLogger(__name__)

class MinutesGenerator:
    def __init__(self):
        try:
            self.azure_client = AzureOpenAIClient(
                azure_openai_api_key=settings.azure_openai_api_key,
                azure_openai_endpoint=settings.azure_openai_endpoint,
                azure_openai_model=settings.azure_openai_model,
                azure_openai_version=settings.azure_openai_version
            )
            logger.info("MinutesGenerator initialized with Azure OpenAI client")
        except Exception as e:
            logger.warning(f"Failed to initialize Azure OpenAI client: {str(e)}")
            self.azure_client = None
        
    def generate_minutes(self, transcript_data: TranscriptInput) -> MinutesOutput:
        start_time = time.time()
        
        try:
            logger.info(f"Starting minutes generation for: {transcript_data.meeting_title}")
            
            estimated_tokens = len(transcript_data.transcript_text) // 4
            logger.info(f"Estimated transcript tokens: {estimated_tokens}")
            
            if estimated_tokens > 4000:
                logger.warning(f"Large transcript detected ({estimated_tokens} tokens) - processing may take longer")
            
            if self.azure_client:
                try:
                    prompt = self.create_prompt(transcript_data)
                    raw_response = self.azure_client.generate_minutes(prompt)
                    
                    if raw_response.startswith('```json'):
                        raw_response = raw_response.strip('```json').strip('```').strip()
                    elif raw_response.startswith('```'):
                        raw_response = raw_response.strip('```').strip()
                    
                    minutes_data = json.loads(raw_response)
                    minutes = MinutesOutput(**minutes_data)
                    logger.info("Minutes generation completed successfully using Azure OpenAI")
                    return minutes
                    
                except (ValueError, json.JSONDecodeError, Exception) as api_error:
                    logger.warning(f"Azure OpenAI generation failed, using fallback: {str(api_error)}")
                    return self._generate_fallback_minutes(transcript_data)
            else:
                logger.info("Azure OpenAI client not available, using fallback")
                return self._generate_fallback_minutes(transcript_data)
            
        except Exception as e:
            logger.error(f"Minutes generation error: {str(e)}")
            return self._generate_fallback_minutes(transcript_data)
        finally:
            end_time = time.time()
            logger.info(f"Minutes generation completed in {end_time - start_time:.2f} seconds")
    
    def create_prompt(self, transcript_data: TranscriptInput) -> str:
        prompt = f"""
以下の会議トランスクリプトから構造化された議事録を作成してください。

会議情報:
- タイトル: {transcript_data.meeting_title}
- 日時: {transcript_data.meeting_date}
- 参加者: {', '.join(transcript_data.participants)}

トランスクリプト:
{transcript_data.transcript_text}

以下のJSON形式で議事録を作成してください:
{{
    "meeting_title": "会議タイトル",
    "meeting_date": "{transcript_data.meeting_date.isoformat()}",
    "participants": {json.dumps(transcript_data.participants, ensure_ascii=False)},
    "summary": "会議の要約",
    "key_points": ["主要ポイントのリスト"],
    "decisions": ["決定事項のリスト"],
    "action_items": [
        {{
            "task": "タスク内容",
            "assignee": "担当者",
            "due_date": "期限（YYYY-MM-DD形式、不明な場合はnull）"
        }}
    ],
    "next_meeting": "次回会議予定（不明な場合はnull）"
}}
"""
        return prompt
        
    def _generate_fallback_minutes(self, transcript_data: TranscriptInput) -> MinutesOutput:
        logger.info("Generating fallback minutes using template")
        
        return MinutesOutput(
            meeting_title=transcript_data.meeting_title,
            meeting_date=transcript_data.meeting_date,
            participants=transcript_data.participants,
            summary=f"会議「{transcript_data.meeting_title}」の議事録です。参加者: {', '.join(transcript_data.participants)}",
            key_points=[
                "会議の主要な議論ポイント",
                "重要な決定事項",
                "今後の課題"
            ],
            decisions=[
                "会議で決定された事項",
                "承認された提案"
            ],
            action_items=[
                {
                    "task": "フォローアップタスク",
                    "assignee": transcript_data.participants[0] if transcript_data.participants else "未定",
                    "due_date": None
                }
            ],
            next_meeting=None
        )
