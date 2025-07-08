# 議事録生成システム

文字起こしテキストから構造化された議事録を自動生成するシステムです。

## 概要

このシステムは、会議の文字起こしテキストを入力として受け取り、AI（OpenAI GPT）を使用して以下の要素を含む構造化された議事録を自動生成します：

- 会議概要
- 参加者リスト
- 主な議題
- 決定事項
- アクションアイテム
- 詳細な文字起こし

## 機能

### 主要機能
- **文字起こし解析**: 話者識別、タイムスタンプ処理、ノイズ除去
- **AI要約**: OpenAI GPTを使用した自動要約と構造化
- **多様な出力形式**: HTML、Markdown、PDF形式での議事録生成
- **Web API**: RESTful APIによるファイルアップロードと処理
- **日本語対応**: 日本語の会議に特化した処理

### 対応形式
- **入力**: テキストファイル (.txt, .md)
- **出力**: HTML、Markdown、PDF

## システム構成

```
src/
├── transcription/          # 文字起こし処理
│   ├── parser.py          # テキスト解析
│   └── preprocessor.py    # 前処理（ノイズ除去等）
├── ai/
│   └── summarizer.py      # AI要約エンジン
├── minutes/
│   ├── generator.py       # 議事録生成
│   └── formatter.py       # 出力フォーマット
└── api/
    └── main.py           # FastAPI Webサービス
```

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env.example`をコピーして`.env`ファイルを作成し、OpenAI APIキーを設定してください：

```bash
cp .env.example .env
```

`.env`ファイルを編集：
```
OPENAI_API_KEY=your_openai_api_key_here
AI_MODEL=gpt-4
MAX_TOKENS=2000
TEMPERATURE=0.3
```

### 3. サーバーの起動

```bash
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## 使用方法

### Web API経由

#### 1. ファイルアップロード
```bash
curl -X POST "http://localhost:8000/upload-transcription/" \
  -F "file=@sample_data/sample_transcription.txt" \
  -F "meeting_title=プロジェクト進捗会議" \
  -F "meeting_date=2024年1月15日" \
  -F "output_format=html"
```

#### 2. テキスト直接入力
```bash
curl -X POST "http://localhost:8000/generate-minutes/" \
  -F "transcription_text=司会：本日はありがとうございます..." \
  -F "meeting_title=定例会議" \
  -F "output_format=markdown"
```

### APIエンドポイント

- `GET /`: システム情報
- `POST /upload-transcription/`: ファイルアップロードによる議事録生成
- `POST /generate-minutes/`: テキスト直接入力による議事録生成
- `GET /health`: ヘルスチェック

### パラメータ

- `meeting_title`: 会議タイトル（デフォルト: "会議"）
- `meeting_date`: 会議日付（デフォルト: 現在日付）
- `output_format`: 出力形式（html, markdown, pdf）

## サンプルデータ

`sample_data/sample_transcription.txt`にサンプルの文字起こしデータが含まれています。

## 文字起こし形式

システムは以下の形式の文字起こしに対応しています：

```
司会：本日はお忙しい中、お集まりいただきありがとうございます。
田中：よろしくお願いします。
[10:30:15] 佐藤：資料の件ですが、来週までに準備いたします。
```

- 話者名は「名前：」の形式
- タイムスタンプは「[HH:MM:SS]」の形式（オプション）
- 自動的にノイズ除去と正規化が行われます

## 技術スタック

- **Python 3.8+**
- **FastAPI**: Web APIフレームワーク
- **OpenAI GPT**: AI要約エンジン
- **Jinja2**: テンプレートエンジン
- **WeasyPrint**: PDF生成
- **spaCy**: 自然言語処理（予定）

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
