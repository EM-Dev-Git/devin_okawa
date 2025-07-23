from typing import Dict, Any
from ..schemas.minutes import MeetingHeader

class MeetingMinutesFormatter:
    def format_minutes(self, raw_minutes: str, header: MeetingHeader) -> str:
        formatted_minutes = raw_minutes
        
        if not formatted_minutes.startswith("## 会議概要"):
            participants_str = "、".join(header.participants)
            absent_str = "、".join(header.absent_members) if header.absent_members else "なし"
            
            header_section = f"""## 会議概要
- 会議名: {header.title}
- 日時: {header.date}
- 場所: {header.location or "記載なし"}
- 参加者: {participants_str}
- 欠席者: {absent_str}
- 司会者: {header.facilitator or "記載なし"}

"""
            formatted_minutes = header_section + formatted_minutes
        
        return formatted_minutes

    def extract_action_items(self, formatted_minutes: str) -> list:
        action_items = []
        lines = formatted_minutes.split('\n')
        in_action_section = False
        
        for line in lines:
            if "## アクションアイテム" in line:
                in_action_section = True
                continue
            elif line.startswith("## ") and in_action_section:
                break
            elif in_action_section and line.strip().startswith("-"):
                action_items.append(line.strip()[1:].strip())
        
        return action_items

minutes_formatter = MeetingMinutesFormatter()
