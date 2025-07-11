"""
Meeting minutes prompt templates and formatting logic
Contains the Japanese meeting minutes format templates
"""

from schemas.llm import MeetingMinutesInput
from typing import List


class MeetingMinutesPrompt:
    """Class containing meeting minutes formatting templates and logic"""
    
    @staticmethod
    def format_meeting_minutes_text(data: MeetingMinutesInput) -> str:
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
        lines.append(f"場所：{data.meeting_room}")
        lines.append(f"参加者：{data.attendees}")
        lines.append(f"欠席者：{data.absentees}")
        lines.append(f"ファシリティ：{data.facility}")
        lines.append("")
        
        lines.append("アジェンダ")
        lines.append("本日の業務目標")
        lines.append("現在の進捗と問題点")
        lines.append("問題解決方法")
        lines.append("次回進捗報告内容")
        lines.append("")
        
        lines.append("・本日の業務目標")
        lines.append("　（会議内容から抽出）")
        lines.append("")
        
        lines.append("・現在の進捗と問題点")
        lines.append("　（会議内容から抽出）")
        lines.append("")
        
        lines.append("・問題解決方法")
        lines.append("　（会議内容から抽出）")
        lines.append("")
        
        lines.append("次回進捗報告内容")
        lines.append("　①先日業務目標について")
        lines.append("　②進捗、課題報告")
        lines.append("　③課題に対する解決策")
        lines.append("")
        
        lines.append("会議内容：")
        lines.append(data.text)
        
        return "\n".join(lines)
    
    @staticmethod
    def get_agenda_template() -> List[str]:
        """
        Get the standard agenda template items
        
        Returns:
            List[str]: Standard agenda items
        """
        return [
            "本日の業務目標",
            "現在の進捗と問題点", 
            "問題解決方法",
            "次回進捗報告内容"
        ]
    
    @staticmethod
    def get_next_meeting_template() -> List[str]:
        """
        Get the standard next meeting agenda template
        
        Returns:
            List[str]: Next meeting agenda items
        """
        return [
            "①先日業務目標について",
            "②進捗、課題報告", 
            "③課題に対する解決策"
        ]
