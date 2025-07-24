from typing import Dict, Any
from .logger import get_logger

logger = get_logger(__name__)


class MinutesFormatter:
    def format_minutes(self, raw_minutes: str, metadata: Dict[str, Any] = None) -> str:
        try:
            logger.info("Formatting meeting minutes")
            
            if metadata is None:
                metadata = {}
            
            formatted_minutes = self._apply_formatting(raw_minutes, metadata)
            
            logger.info("Minutes formatting completed")
            return formatted_minutes
            
        except Exception as e:
            logger.error(f"Error formatting minutes: {str(e)}")
            return raw_minutes
    
    def _apply_formatting(self, minutes: str, metadata: Dict[str, Any]) -> str:
        formatted = minutes
        
        if not formatted.startswith("# "):
            title = metadata.get("title", "会議議事録")
            formatted = f"# {title}\n\n{formatted}"
        
        if "作成日時:" not in formatted:
            from datetime import datetime
            created_at = datetime.now().strftime("%Y年%m月%d日 %H:%M")
            formatted += f"\n\n---\n**作成日時:** {created_at}"
        
        return formatted


minutes_formatter = MinutesFormatter()
