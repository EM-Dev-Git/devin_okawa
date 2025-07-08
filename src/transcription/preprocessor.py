import re
from typing import List

class TranscriptionPreprocessor:
    def __init__(self):
        self.noise_patterns = [
            r'\(笑\)',
            r'\(咳\)',
            r'\(雑音\)',
            r'\(不明瞭\)',
            r'えー+',
            r'あー+',
            r'うー+',
            r'そのー+',
        ]
    
    def clean_text(self, text: str) -> str:
        """
        文字起こしテキストのノイズを除去
        """
        cleaned = text
        
        for pattern in self.noise_patterns:
            cleaned = re.sub(pattern, '', cleaned)
        
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        cleaned = cleaned.strip()
        
        return cleaned
    
    def normalize_speakers(self, text: str) -> str:
        """
        話者名の表記を正規化
        """
        speaker_mappings = {
            r'司会者?[:：]': '司会：',
            r'議長[:：]': '司会：',
            r'参加者[A-Z][:：]': lambda m: f'参加者{m.group(0)[-2]}：',
        }
        
        normalized = text
        for pattern, replacement in speaker_mappings.items():
            if callable(replacement):
                normalized = re.sub(pattern, replacement, normalized)
            else:
                normalized = re.sub(pattern, replacement, normalized)
        
        return normalized
    
    def split_long_sentences(self, text: str, max_length: int = 200) -> str:
        """
        長すぎる文を適切な位置で分割
        """
        sentences = text.split('。')
        result = []
        
        for sentence in sentences:
            if len(sentence) > max_length:
                parts = sentence.split('、')
                current_part = ""
                
                for part in parts:
                    if len(current_part + part) > max_length and current_part:
                        result.append(current_part.strip() + '。')
                        current_part = part
                    else:
                        current_part += part + '、'
                
                if current_part:
                    result.append(current_part.rstrip('、') + '。')
            else:
                result.append(sentence + '。')
        
        return ''.join(result)
