
import openai
from config import settings
from utils.logger import get_logger
from schemas.llm import MeetingMinutesInput, MeetingMinutesOutput
from modules.prompt import MeetingMinutesPrompt
from typing import List

logger = get_logger("fastapi_app.modules.meeting_minutes")  # 議事録モジュール用ロガー


class MeetingMinutesService:
    
    def generate_meeting_minutes(self, input_data: MeetingMinutesInput) -> MeetingMinutesOutput:
        # input_data: 議事録入力データ
        logger.info(f"Generating meeting minutes for: {input_data.title}")
        
        try:
            if settings.openai_api_key and settings.openai_api_key != "your-openai-api-key-here":
                try:
                    meeting_text = self._generate_with_openai(input_data)
                    logger.info("Meeting minutes generated successfully using OpenAI API")
                    return MeetingMinutesOutput(meeting_minutes_text=meeting_text)
                except Exception as api_error:
                    logger.warning(f"OpenAI API call failed, falling back to template: {str(api_error)}")
            
            meeting_text = MeetingMinutesPrompt.format_meeting_minutes_text(input_data)
            logger.info("Meeting minutes generated successfully using template fallback")
            return MeetingMinutesOutput(meeting_minutes_text=meeting_text)
            
        except Exception as e:
            logger.error(f"Error generating meeting minutes: {str(e)}")
            raise Exception(f"Failed to generate meeting minutes: {str(e)}")
    
    def _generate_with_openai(self, input_data: MeetingMinutesInput) -> str:
        client = openai.OpenAI(api_key=settings.openai_api_key)
        
        system_prompt = MeetingMinutesPrompt.call_system_minutes()
        user_prompt = MeetingMinutesPrompt.call_user_minutes(
            input_data.title, input_data.date, input_data.meeting_room,
            input_data.attendees, input_data.absentees, input_data.facility, input_data.text
        )
        
        response = client.chat.completions.create(
            model=input_data.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=input_data.max_tokens,
            temperature=input_data.temperature,
            top_p=input_data.top_p
        )
        
        return response.choices[0].message.content
