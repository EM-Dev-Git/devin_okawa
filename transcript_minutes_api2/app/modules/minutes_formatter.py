from typing import Dict, Any
from datetime import datetime
from ..modules.logger import get_logger

logger = get_logger(__name__)


class MinutesFormatter:
    def __init__(self):
        pass
    
    def format_minutes(self, minutes_data: Dict[str, Any]) -> str:
        try:
            logger.info("議事録フォーマット処理開始")
            
            formatted_minutes = f"""

**作成日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}


{minutes_data.get('generated_minutes', '議事録が生成されませんでした。')}

---

**処理ステータス**: {minutes_data.get('processing_status', 'unknown')}
**元トランスクリプト文字数**: {len(minutes_data.get('transcript', ''))}文字
"""
            
            logger.info("議事録フォーマット処理完了")
            return formatted_minutes.strip()
            
        except Exception as e:
            logger.error(f"議事録フォーマットエラー: {str(e)}")
            return f"議事録のフォーマット中にエラーが発生しました: {str(e)}"
    
    def extract_summary(self, minutes: str) -> str:
        try:
            lines = minutes.split('\n')
            summary_lines = []
            
            for line in lines:
                if line.strip() and not line.startswith('#') and not line.startswith('**'):
                    summary_lines.append(line.strip())
                    if len(summary_lines) >= 3:
                        break
            
            return ' '.join(summary_lines)[:200] + "..." if len(' '.join(summary_lines)) > 200 else ' '.join(summary_lines)
            
        except Exception as e:
            logger.error(f"サマリー抽出エラー: {str(e)}")
            return "サマリーの抽出に失敗しました。"


minutes_formatter = MinutesFormatter()
