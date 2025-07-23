from typing import Dict, Any
from datetime import datetime
from .logger import get_logger

logger = get_logger(__name__)


class MeetingMinutesFormatter:
    def format_minutes(self, analysis_result: str, header: Dict[str, Any]) -> str:
        try:
            logger.info("議事録フォーマット開始")
            
            formatted_minutes = f"""

- **日時**: {header.get('date', '未設定')}
- **場所**: {header.get('location', '未設定')}
- **進行**: {header.get('facilitator', '未設定')}
- **参加者**: {', '.join(header.get('participants', []))}
- **作成日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}

---

{analysis_result}

---

*この議事録は AI により自動生成されました。*
"""
            
            logger.info("議事録フォーマット完了")
            return formatted_minutes.strip()
            
        except Exception as e:
            logger.error(f"議事録フォーマットエラー: {str(e)}")
            raise Exception(f"フォーマットエラー: {str(e)}")
