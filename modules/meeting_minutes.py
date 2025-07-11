"""
Meeting minutes business logic module
Converts JSON input to formatted text meeting minutes
"""

from utils.logger import get_logger
from schemas.meeting_minutes import MeetingMinutesInput, MeetingMinutesOutput
from typing import List

logger = get_logger("fastapi_app.modules.meeting_minutes")


class MeetingMinutesService:
    """Service class for meeting minutes generation operations"""
    
    def generate_meeting_minutes(self, input_data: MeetingMinutesInput) -> MeetingMinutesOutput:
        """
        Generate formatted text meeting minutes from JSON input
        
        Args:
            input_data: Meeting minutes input data
            
        Returns:
            MeetingMinutesOutput: Generated meeting minutes in text format
        """
        logger.info(f"Generating meeting minutes for: {input_data.title}")
        
        try:
            meeting_text = self._format_meeting_minutes(input_data)
            
            logger.info("Meeting minutes generated successfully")
            return MeetingMinutesOutput(
                meeting_minutes_text=meeting_text
            )
            
        except Exception as e:
            logger.error(f"Error generating meeting minutes: {str(e)}")
            return MeetingMinutesOutput(
                success=False,
                message=f"Failed to generate meeting minutes: {str(e)}",
                meeting_minutes_text=""
            )
    
    def _format_meeting_minutes(self, data: MeetingMinutesInput) -> str:
        """
        Format the meeting minutes according to the specified Japanese format
        
        Args:
            data: Meeting minutes input data
            
        Returns:
            str: Formatted meeting minutes text
        """
        lines = []
        
        lines.append(f"タイトル：{data.title}")
        lines.append(f"日時：{data.date}")
        lines.append(f"場所：{data.location}")
        lines.append(f"参加者：{', '.join(data.participants)}")
        
        if data.absent_members:
            lines.append(f"欠席者：{', '.join(data.absent_members)}")
        else:
            lines.append("欠席者：なし")
            
        lines.append(f"ファシリティ：{data.facilitator}")
        lines.append("")
        
        lines.append("アジェンダ")
        lines.append("本日の業務目標")
        lines.append("現在の進捗と問題点")
        lines.append("問題解決方法")
        lines.append("次回進捗報告内容")
        lines.append("")
        
        lines.append("・本日の業務目標")
        for goal in data.participant_goals:
            lines.append(f"　{goal.name}")
            lines.append(f"　{goal.goal_content}")
        lines.append("")
        
        lines.append("・現在の進捗と問題点")
        for progress in data.participant_progress:
            lines.append(f"　・{progress.name}")
            lines.append(f"　　　前日の達成度：{progress.previous_achievement_rate}%")
            lines.append(f"　　　進捗状況：{progress.progress_status}")
            lines.append(f"　　　問題点：{progress.issues}")
        lines.append("")
        
        lines.append("・問題解決方法")
        for solution in data.participant_solutions:
            lines.append(f"　・{solution.name}")
            lines.append(f"　　{solution.solution_content}")
        lines.append("")
        
        lines.append("次回進捗報告内容")
        lines.append("　①先日業務目標について")
        lines.append("　②進捗、課題報告")
        lines.append("　③課題に対する解決策")
        
        return "\n".join(lines)
