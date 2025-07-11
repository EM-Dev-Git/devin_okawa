"""
Meeting minutes prompt templates and formatting logic
Contains the Japanese meeting minutes format templates for OpenAI
"""

from schemas.llm import MeetingMinutesInput
from typing import List


class MeetingMinutesPrompt:
    """Class containing meeting minutes formatting templates and logic for OpenAI"""
    
    @staticmethod
    def call_system_minutes() -> str:
        """
        Generate the system prompt for OpenAI meeting minutes generation
        
        Returns:
            str: System prompt with rules and role definition
        """
        data = (
            f'# あなたの役割\n'
            f'あなたはユーザーから投げられた会話の文字起こしをもとに議事録を作成するスペシャリストです。\n'
            f'また、あなたはフォーマットを忠実に再現します。\n'
            f'作成にあたって以下のルールを設けます。\n'
            f'# ルール\n'
            f'名前の表記は苗字のみ。\n'
            f'各項目の記入順序は参加者の順序と一致させる。\n'
            f'「*」「#」「-」は使用不可です。\n'
            f'議事録本文の項目と名前の先頭に「・」を必ず記入してください。\n'
            f'フォーマット内容は項目を含めて必ず全て表示してください。\n'
            f'議事録以外の内容は記載しないでください。\n'
            f'アジェンダの転換では改行を行ってください。\n'
            f'インデントも忠実に再現してください。\n'
            f'textの中身を議事録としてフォーマットに当てはめて行ってください。\n'
            f'これからタイトル、日時、場所、参加者、欠席者、ファシリティ、文字起こしを入力するのでフォーマットに従って議事録を作成してください。\n'
        )
        return data

    @staticmethod
    def call_user_minutes(title: str, date: str, meeting_room: str, attendees: str, absentees: str, facility: str, text: str) -> str:
        """
        Generate the user prompt for OpenAI meeting minutes generation
        
        Args:
            title: Meeting title
            date: Meeting date
            meeting_room: Meeting room/location
            attendees: Meeting attendees
            absentees: Absent members
            facility: Meeting facilitator
            text: Meeting transcript text
            
        Returns:
            str: User prompt with meeting data and format template
        """
        data = (
            f'# 文字起こし内容\n'
            f'{text}\n'

            f'# フォーマット\n'
            f'{title}\n'
            f'日時：{date}\n'
            f'場所：{meeting_room}\n'
            f'参加者：{attendees}\n'
            f'欠席者：{absentees}\n'
            f'ファシリティ：{facility}\n'

            f'アジェンダ\n'
            f'本日の業務目標\n'
            f'現在の進捗と問題点\n'
            f'問題解決方法\n'
            f'次回進捗報告内容\n'

            f'・本日の業務目標\n'
            f'　名前1\n'
            f'　目標内容\n'
            f'　名前2\n'
            f'　目標内容\n'

            f'・現在の進捗と問題点\n'
            f'　・名前1\n'
            f'　　　前日の達成度：%\n'
            f'　　　進捗状況：\n'
            f'　　　問題点：\n'
            f'　・名前2\n'
            f'　　　前日の達成度：%\n'
            f'　　　進捗状況：\n'
            f'　　　問題点：\n'

            f'・問題解決方法\n'
            f'　・名前1\n'
            f'　　内容\n'
            f'　・名前2\n'
            f'　　内容\n'

            f'次回進捗報告内容\n'
            f'　①先日業務目標について\n'
            f'　②進捗、課題報告\n'
            f'　③課題に対する解決策\n'
        )
        return data
    
    @staticmethod
    def format_meeting_minutes_text(data: MeetingMinutesInput) -> str:
        """
        Format the meeting minutes using OpenAI prompts (for testing without OpenAI)
        
        Args:
            data: Meeting minutes input data
            
        Returns:
            str: Formatted meeting minutes text using the prompt template
        """
        system_prompt = MeetingMinutesPrompt.call_system_minutes()
        user_prompt = MeetingMinutesPrompt.call_user_minutes(
            data.title, data.date, data.meeting_room, 
            data.attendees, data.absentees, data.facility, data.text
        )
        
        lines = []
        lines.append(f"{data.title}")
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
