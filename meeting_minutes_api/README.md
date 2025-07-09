# Meeting Minutes API

朝の進捗報告会のトランスクリプトから議事録を自動生成するFastAPI アプリケーション

## 概要

このAPIは、朝の進捗報告会の会話内容のトランスクリプトを受け取り、AIを使用して構造化された議事録を生成します。

## 機能

- **トランスクリプト処理**: OpenAI GPT-4を使用してトランスクリプトから構造化データを抽出
- **議事録フォーマット**: 指定された形式での議事録テキスト生成
- **ユーザー入力**: 会議のメタデータ（タイトル、日時、参加者など）をユーザーが入力可能
- **REST API**: FastAPIによる標準的なREST APIエンドポイント

## API エンドポイント

### GET /healthz
APIの健全性チェック

### POST /process-transcript
トランスクリプトを処理して構造化された議事録データを生成

**入力例:**
```json
{
  "header": {
    "title": "朝の進捗報告会",
    "date": "2025年7月9日",
    "location": "会議室A",
    "participants": ["田中", "佐藤", "鈴木"],
    "absent_members": ["山田"],
    "facilitator": "田中"
  },
  "transcript": "会議のトランスクリプト内容..."
}
```

### POST /format-minutes
構造化された議事録データをテキスト形式に変換

### POST /generate-minutes
トランスクリプト処理とフォーマットを一括実行

## セットアップ

1. 依存関係のインストール:
```bash
poetry install
```

2. 環境変数の設定:
```bash
cp .env.example .env
# .envファイルでOPENAI_API_KEYを設定
```

3. 開発サーバーの起動:
```bash
poetry run fastapi dev app/main.py
```

4. API ドキュメントへのアクセス:
http://localhost:8000/docs

## 出力フォーマット

生成される議事録は以下の形式に従います:

```
タイトル：朝の進捗報告会
日時：2025年7月9日
場所：会議室A
参加者：田中, 佐藤, 鈴木
欠席者：山田
ファシリティ：田中

アジェンダ
本日の業務目標
現在の進捗と問題点
問題解決方法
次回進捗報告内容

・本日の業務目標
　田中
　新機能の設計完了
　佐藤
　テストケース作成

・現在の進捗と問題点
　・田中
　　　前日の達成度：80%
　　　進捗状況：設計書の8割完成
　　　問題点：要件の一部が不明確
　・佐藤
　　　前日の達成度：90%
　　　進捗状況：テストケース作成中
　　　問題点：テスト環境の準備が遅れている

・問題解決方法
　・田中
　　要件について関係者と明日打ち合わせ予定
　・佐藤
　　テスト環境の準備を優先して進める

次回進捗報告内容
　①先日業務目標について
　②進捗、課題報告
　③課題に対する解決策
```

## 技術仕様

- **フレームワーク**: FastAPI
- **AI処理**: OpenAI GPT-4
- **データ検証**: Pydantic
- **言語**: Python 3.12+

## 環境変数

- `OPENAI_API_KEY`: OpenAI APIキー（必須）

## 開発

### 作業計画書

各コンポーネントの詳細な作業計画書は以下にあります:

- [TranscriptProcessor クラス](work_plans/transcript_processor_plan.md)
- [MeetingMinutesFormatter クラス](work_plans/meeting_minutes_formatter_plan.md)
- [API Endpoints](work_plans/api_endpoints_plan.md)

### テスト

```bash
# 開発サーバー起動
poetry run fastapi dev app/main.py

# API ドキュメントでテスト
# http://localhost:8000/docs にアクセス
```
