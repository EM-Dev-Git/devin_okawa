# TranscriptProcessor クラス作業計画書

## 概要
朝の進捗報告会のトランスクリプトをAIを使用して構造化された議事録に変換するサービスクラス

## 責任範囲
- OpenAI APIを使用したトランスクリプト処理
- AIプロンプトの作成と管理
- AI応答の解析と構造化データへの変換
- エラーハンドリング

## 主要メソッド

### `__init__(self)`
- OpenAIクライアントの初期化
- 環境変数からAPIキーを取得
- APIキーが設定されていない場合はValueErrorを発生

### `process_transcript(self, request: TranscriptRequest) -> MeetingMinutes`
- メインの処理メソッド
- トランスクリプトを受け取り、構造化された議事録を返す
- AIプロンプト作成、API呼び出し、レスポンス解析を統合
- ヘッダー情報と抽出されたデータを組み合わせてMeetingMinutesオブジェクトを作成

### `_get_system_prompt(self) -> str`
- AI処理用のシステムプロンプトを返す
- 日本語での指示を含む
- JSON形式での回答を要求
- 朝の進捗報告会の文脈を明確に指定

### `_create_processing_prompt(self, transcript: str) -> str`
- トランスクリプトを含む具体的なプロンプトを作成
- 期待するJSON形式を明示
- 3つのセクション（目標、進捗・問題、解決策）の抽出を指示

### `_parse_ai_response(self, ai_content: str) -> dict`
- AI応答からJSONを抽出
- JSONの開始と終了位置を特定
- Pydanticモデルに変換
- エラーハンドリング（JSON解析エラー、不正な形式）

## 依存関係
- OpenAI Python SDK
- Pydantic models (PersonGoal, PersonProgress, PersonSolution)
- 環境変数 (OPENAI_API_KEY)
- JSON標準ライブラリ

## エラーハンドリング
- OpenAI API呼び出し失敗
- JSON解析エラー
- 不正なレスポンス形式
- APIキー未設定エラー

## 設定要件
- OPENAI_API_KEY環境変数の設定
- GPT-4モデルへのアクセス権限

## テスト要件
- 正常なトランスクリプト処理
- 不正なトランスクリプト処理
- API呼び出し失敗時の処理
- JSON解析エラー時の処理
- APIキー未設定時の処理
