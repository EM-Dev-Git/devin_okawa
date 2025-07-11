from schemas.llm import MeetingMinutesInput


class MeetingMinutesPrompt:
    
    @staticmethod
    def call_system_minutes() -> str:
        return """あなたは議事録作成の専門家です。
与えられた会議の文字起こしテキストから、以下のフォーマットに従って議事録を作成してください。

フォーマット：
タイトル：
日時：
場所：
参加者：
欠席者：
ファシリティ：(司会者)

アジェンダ
本日の業務目標
現在の進捗と問題点
問題解決方法
次回進捗報告内容

・本日の業務目標
　名前1
　目標内容
　名前2
　目標内容

・現在の進捗と問題点
　・名前1
　　　前日の達成度：x%
　　　進捗状況：
　　　問題点：
　・名前2
　　　前日の達成度：x%
　　　進捗状況：
　　　問題点：

・問題解決方法
　・名前1
　　内容
　・名前2
　　内容

次回進捗報告内容
　①先日業務目標について
　②進捗、課題報告
　③課題に対する解決策

文字起こしテキストから適切な情報を抽出し、上記フォーマットに従って整理してください。"""

    @staticmethod
    def call_user_minutes(title: str, date: str, meeting_room: str, 
                         attendees: str, absentees: str, facility: str, text: str) -> str:
        return f"""以下の会議情報と文字起こしテキストから議事録を作成してください。

会議情報：
タイトル：{title}
日時：{date}
場所：{meeting_room}
参加者：{attendees}
欠席者：{absentees}
ファシリティ：{facility}

文字起こしテキスト：
{text}

上記の情報を基に、指定されたフォーマットに従って議事録を作成してください。"""

    @staticmethod
    def format_meeting_minutes_text(data: MeetingMinutesInput) -> str:
        return f"""{data.title}
日時：{data.date}
場所：{data.meeting_room}
参加者：{data.attendees}
欠席者：{data.absentees}
ファシリティ：{data.facility}

アジェンダ
本日の業務目標
現在の進捗と問題点
問題解決方法
次回進捗報告内容

・本日の業務目標
　（会議内容から抽出）

・現在の進捗と問題点
　（会議内容から抽出）

・問題解決方法
　（会議内容から抽出）

次回進捗報告内容
　①先日業務目標について
　②進捗、課題報告
　③課題に対する解決策"""
