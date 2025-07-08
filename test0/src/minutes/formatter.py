from typing import Dict
from jinja2 import Template
import weasyprint
import os

class MinutesFormatter:
    def __init__(self):
        self.html_template = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ meeting_title }} - 議事録</title>
    <style>
        body {
            font-family: 'Hiragino Sans', 'Yu Gothic', 'Meiryo', sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
        }
        .header {
            border-bottom: 2px solid #007acc;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .meeting-title {
            font-size: 24px;
            font-weight: bold;
            color: #007acc;
            margin-bottom: 10px;
        }
        .meeting-info {
            font-size: 14px;
            color: #666;
        }
        .section {
            margin-bottom: 30px;
        }
        .section-title {
            font-size: 18px;
            font-weight: bold;
            color: #007acc;
            border-left: 4px solid #007acc;
            padding-left: 10px;
            margin-bottom: 15px;
        }
        .participants {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .participant {
            background-color: #f0f8ff;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 14px;
        }
        .action-item {
            background-color: #fff8dc;
            border-left: 4px solid #ffa500;
            padding: 10px;
            margin-bottom: 10px;
        }
        .transcription {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            font-size: 14px;
            white-space: pre-wrap;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
            text-align: right;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="meeting-title">{{ meeting_title }}</div>
        <div class="meeting-info">
            開催日: {{ meeting_date }}<br>
            参加者: {{ participants|length }}名
        </div>
    </div>

    <div class="section">
        <div class="section-title">参加者</div>
        <div class="participants">
            {% for participant in participants %}
            <span class="participant">{{ participant }}</span>
            {% endfor %}
        </div>
    </div>

    <div class="section">
        <div class="section-title">会議内容</div>
        <div>{{ summary|safe }}</div>
    </div>

    {% if action_items %}
    <div class="section">
        <div class="section-title">アクションアイテム</div>
        {% for item in action_items %}
        <div class="action-item">
            <strong>{{ item.action }}</strong><br>
            {% if item.assignee %}担当者: {{ item.assignee }}<br>{% endif %}
            {% if item.deadline %}期限: {{ item.deadline }}{% endif %}
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <div class="section">
        <div class="section-title">詳細な文字起こし</div>
        <div class="transcription">{{ full_transcription }}</div>
    </div>

    <div class="footer">
        生成日時: {{ generated_at }}
    </div>
</body>
</html>
        """
        
        self.markdown_template = """

**開催日:** {{ meeting_date }}  
**参加者:** {{ participants|join(', ') }}


{{ summary }}

{% if action_items %}

{% for item in action_items %}
- **{{ item.action }}**
  {% if item.assignee %}- 担当者: {{ item.assignee }}{% endif %}
  {% if item.deadline %}- 期限: {{ item.deadline }}{% endif %}

{% endfor %}
{% endif %}


```
{{ full_transcription }}
```

---
*生成日時: {{ generated_at }}*
        """
    
    def format_to_html(self, minutes_data: Dict) -> str:
        """
        議事録をHTML形式でフォーマット
        """
        template = Template(self.html_template)
        return template.render(**minutes_data)
    
    def format_to_markdown(self, minutes_data: Dict) -> str:
        """
        議事録をMarkdown形式でフォーマット
        """
        template = Template(self.markdown_template)
        return template.render(**minutes_data)
    
    def format_to_pdf(self, minutes_data: Dict, output_path: str) -> str:
        """
        議事録をPDF形式でフォーマット
        """
        html_content = self.format_to_html(minutes_data)
        
        try:
            weasyprint.HTML(string=html_content).write_pdf(output_path)
            return f"PDFファイルが生成されました: {output_path}"
        except Exception as e:
            return f"PDF生成中にエラーが発生しました: {str(e)}"
    
    def save_minutes(self, minutes_data: Dict, output_format: str = "html", 
                    output_dir: str = "output") -> str:
        """
        議事録を指定された形式で保存
        """
        os.makedirs(output_dir, exist_ok=True)
        
        meeting_title = minutes_data.get("meeting_title", "会議")
        meeting_date = minutes_data.get("meeting_date", "").replace("/", "-")
        
        if output_format.lower() == "html":
            filename = f"{meeting_title}_{meeting_date}.html"
            filepath = os.path.join(output_dir, filename)
            content = self.format_to_html(minutes_data)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"HTMLファイルが保存されました: {filepath}"
        
        elif output_format.lower() == "markdown":
            filename = f"{meeting_title}_{meeting_date}.md"
            filepath = os.path.join(output_dir, filename)
            content = self.format_to_markdown(minutes_data)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Markdownファイルが保存されました: {filepath}"
        
        elif output_format.lower() == "pdf":
            filename = f"{meeting_title}_{meeting_date}.pdf"
            filepath = os.path.join(output_dir, filename)
            result = self.format_to_pdf(minutes_data, filepath)
            
            return result
        
        else:
            return f"サポートされていない出力形式です: {output_format}"
