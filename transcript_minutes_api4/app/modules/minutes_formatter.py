import json
from typing import Dict, Any, List
from datetime import datetime
from .logger import get_logger

logger = get_logger(__name__)


class MeetingMinutesFormatter:
    def __init__(self):
        logger.info("MeetingMinutesFormatter初期化完了")

    def format_minutes(self, analysis_result: str, header: Dict[str, Any]) -> str:
        try:
            logger.info("議事録フォーマット開始")
            
            try:
                analysis_data = json.loads(analysis_result)
            except json.JSONDecodeError:
                analysis_data = {"summary": analysis_result}

            formatted_minutes = self._generate_formatted_minutes(analysis_data, header)
            
            logger.info("議事録フォーマット完了")
            return formatted_minutes

        except Exception as e:
            logger.error(f"議事録フォーマットエラー: {str(e)}")
            raise Exception(f"フォーマットエラー: {str(e)}")

    def _generate_formatted_minutes(self, analysis_data: Dict[str, Any], header: Dict[str, Any]) -> str:
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M")
        
        minutes = f"""

- **日時**: {header.get('date', '未設定')}
- **場所**: {header.get('location', '未設定')}
- **司会者**: {header.get('facilitator', '未設定')}
- **参加者**: {', '.join(header.get('participants', []))}
- **作成日時**: {current_time}

{analysis_data.get('summary', '要約なし')}

"""

        if 'agenda_items' in analysis_data and analysis_data['agenda_items']:
            minutes += "## 議題・討議内容\n\n"
            for i, item in enumerate(analysis_data['agenda_items'], 1):
                minutes += f"### {i}. {item.get('title', f'議題{i}')}\n\n"
                minutes += f"**討議内容**: {item.get('discussion', '記録なし')}\n\n"
                
                if item.get('decisions'):
                    minutes += "**決定事項**:\n"
                    for decision in item['decisions']:
                        minutes += f"- {decision}\n"
                    minutes += "\n"
                
                if item.get('action_items'):
                    minutes += "**アクションアイテム**:\n"
                    for action in item['action_items']:
                        minutes += f"- {action.get('task', 'タスク未設定')} "
                        minutes += f"(担当: {action.get('assignee', '未設定')}, "
                        minutes += f"期限: {action.get('deadline', '未設定')})\n"
                    minutes += "\n"

        if analysis_data.get('next_meeting'):
            minutes += f"## 次回会議\n{analysis_data['next_meeting']}\n\n"

        if analysis_data.get('notes'):
            minutes += f"## その他・注意事項\n{analysis_data['notes']}\n\n"

        minutes += "---\n*この議事録はAIによって自動生成されました*"

        return minutes
