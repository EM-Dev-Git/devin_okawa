from typing import Dict, Any
from datetime import date
from ..schemas.minutes import MeetingHeader
from .logger import get_logger

logger = get_logger(__name__)

class MeetingMinutesFormatter:
    def format_minutes(self, processed_data: Dict[str, Any], header: MeetingHeader) -> str:
        try:
            logger.info("議事録フォーマット開始")
            
            formatted_minutes = self._create_formatted_minutes(processed_data, header)
            
            logger.info("議事録フォーマット完了")
            return formatted_minutes
            
        except Exception as e:
            logger.error(f"議事録フォーマットエラー: {str(e)}")
            raise Exception(f"議事録フォーマットに失敗しました: {str(e)}")

    def _create_formatted_minutes(self, data: Dict[str, Any], header: MeetingHeader) -> str:
        participants_str = "、".join(header.participants) if header.participants else "記載なし"
        
        minutes = f"""

- **日時**: {header.date}
- **場所**: {header.location}
- **参加者**: {participants_str}
- **司会**: {header.facilitator}

{data.get('summary', '概要なし')}

"""
        
        agenda_items = data.get('agenda_items', [])
        if not agenda_items:
            minutes += "\n議題なし\n"
        else:
            for i, item in enumerate(agenda_items, 1):
                minutes += f"\n### {i}. {item.get('title', f'議題{i}')}\n"
                minutes += f"\n**議論内容**\n{item.get('discussion', '記載なし')}\n"
                
                decisions = item.get('decisions', [])
                if decisions:
                    minutes += "\n**決定事項**\n"
                    for decision in decisions:
                        minutes += f"- {decision}\n"
                
                action_items = item.get('action_items', [])
                if action_items:
                    minutes += "\n**アクションアイテム**\n"
                    for action in action_items:
                        task = action.get('task', '未定義')
                        assignee = action.get('assignee', '未定義')
                        deadline = action.get('deadline', '未定義')
                        minutes += f"- {task} (担当: {assignee}, 期限: {deadline})\n"
        
        next_meeting = data.get('next_meeting', '')
        if next_meeting:
            minutes += f"\n## 次回会議\n{next_meeting}\n"
        
        minutes += f"\n---\n*議事録作成日時: {date.today()}*\n"
        
        return minutes

minutes_formatter = MeetingMinutesFormatter()
