from modules.config import settings
print('Configuration test:')
print(f'API Key: {settings.azure_openai_api_key[:10]}...')
print(f'Model: {settings.azure_openai_model}')
print(f'Version: {settings.azure_openai_version}')
print(f'Endpoint: {settings.azure_openai_endpoint}')

sample_transcript = {
    "meeting_title": "朝の進捗報告会",
    "meeting_date": "2025-07-14T09:00:00",
    "participants": ["田中", "佐藤", "鈴木"],
    "transcript_text": "田中: おはようございます。今日の進捗報告を始めます。佐藤さんから報告をお願いします。佐藤: 昨日はAPIの実装を進めました。80%完了しています。問題点として、認証部分でエラーが発生しています。鈴木: 私はフロントエンドの作業を行いました。デザインは完了し、現在コンポーネントの実装中です。田中: ありがとうございます。佐藤さんの認証エラーについて、明日までに解決策を検討しましょう。次回は明後日の同時刻に行います。"
}

print('\nSample transcript data for testing:')
import json
print(json.dumps(sample_transcript, ensure_ascii=False, indent=2))
