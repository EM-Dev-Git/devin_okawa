from typing import Dict, Any
from .logger import get_logger

logger = get_logger(__name__)


class MinutesFormatter:
    def __init__(self):
        pass
    
    def format_minutes(self, raw_minutes: str, meeting_header: Dict[str, Any] = None) -> str:
        logger.info("議事録フォーマット処理開始")
        
        try:
            formatted_minutes = self._apply_formatting(raw_minutes, meeting_header)
            logger.info("議事録フォーマット完了")
            return formatted_minutes
            
        except Exception as e:
            logger.error(f"フォーマット処理エラー: {str(e)}")
            raise Exception(f"議事録フォーマット中にエラーが発生しました: {str(e)}")
    
    def _apply_formatting(self, raw_minutes: str, meeting_header: Dict[str, Any] = None) -> str:
        formatted = raw_minutes
        
        if meeting_header:
            header_section = self._create_header_section(meeting_header)
            formatted = header_section + "\n\n" + formatted
        
        formatted = self._ensure_proper_structure(formatted)
        formatted = self._add_footer(formatted)
        
        return formatted
    
    def _create_header_section(self, meeting_header: Dict[str, Any]) -> str:
        header = "# 会議議事録\n\n"
        header += "## 会議情報\n"
        
        if "title" in meeting_header:
            header += f"- **会議名**: {meeting_header['title']}\n"
        if "date" in meeting_header:
            header += f"- **日時**: {meeting_header['date']}\n"
        if "location" in meeting_header:
            header += f"- **場所**: {meeting_header['location']}\n"
        if "facilitator" in meeting_header:
            header += f"- **司会**: {meeting_header['facilitator']}\n"
        if "participants" in meeting_header:
            participants = ", ".join(meeting_header['participants'])
            header += f"- **参加者**: {participants}\n"
        
        return header
    
    def _ensure_proper_structure(self, content: str) -> str:
        if not content.startswith("# "):
            content = "# 会議議事録\n\n" + content
        
        return content
    
    def _add_footer(self, content: str) -> str:
        footer = "\n\n---\n"
        footer += "*この議事録はAIによって自動生成されました。内容に誤りがある場合は修正してください。*"
        
        return content + footer
    
    def extract_action_items(self, minutes: str) -> list:
        logger.info("アクションアイテム抽出開始")
        
        action_items = []
        lines = minutes.split('\n')
        
        in_action_section = False
        for line in lines:
            if "アクションアイテム" in line or "行動項目" in line:
                in_action_section = True
                continue
            
            if in_action_section:
                if line.startswith("#") and "アクション" not in line:
                    break
                
                if "|" in line and "項目" not in line and "---" not in line:
                    parts = [part.strip() for part in line.split("|")]
                    if len(parts) >= 4:
                        action_items.append({
                            "task": parts[1],
                            "assignee": parts[2],
                            "deadline": parts[3]
                        })
        
        logger.info(f"アクションアイテム {len(action_items)} 件抽出完了")
        return action_items
