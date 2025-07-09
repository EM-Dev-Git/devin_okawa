# API Endpoints 作業計画書

## 概要
FastAPIを使用した議事録作成APIのエンドポイント設計と実装

## エンドポイント仕様

### GET /healthz
- **目的**: APIの健全性チェック
- **入力**: なし
- **出力**: `{"status": "ok"}`
- **処理**: 基本的なヘルスチェック

### POST /process-transcript
- **目的**: トランスクリプトを処理して構造化された議事録を生成
- **入力**: `TranscriptRequest` (ヘッダー情報 + トランスクリプト)
- **出力**: `MeetingMinutes` (構造化された議事録)
- **処理**: TranscriptProcessorを使用してAI処理
- **エラー**: 500 - AI処理エラー、APIキー未設定

### POST /format-minutes
- **目的**: 構造化された議事録をテキスト形式に変換
- **入力**: `MeetingMinutes`
- **出力**: `{"formatted_minutes": "フォーマット済みテキスト"}`
- **処理**: MeetingMinutesFormatterを使用
- **エラー**: 500 - フォーマット処理エラー

### POST /generate-minutes
- **目的**: トランスクリプト処理とフォーマットを一括実行
- **入力**: `TranscriptRequest`
- **出力**: `{"formatted_minutes": "テキスト", "structured_data": MeetingMinutes}`
- **処理**: TranscriptProcessor + MeetingMinutesFormatter
- **エラー**: 500 - AI処理またはフォーマットエラー

## 実装要件

### データモデル
- `MeetingHeader`: ユーザー入力フィールド
- `TranscriptRequest`: ヘッダー + トランスクリプト
- `MeetingMinutes`: 完全な構造化議事録
- `PersonGoal`, `PersonProgress`, `PersonSolution`: 個人データ

### エラーハンドリング
- 400 Bad Request: 不正な入力データ（Pydanticバリデーション）
- 500 Internal Server Error: AI処理エラー、システムエラー
- HTTPExceptionを使用した適切なエラーレスポンス
- 詳細なエラーメッセージの返却

### バリデーション
- Pydanticモデルによる自動入力検証
- 必須フィールドのチェック
- データ型の検証
- リスト型フィールドの検証

### レスポンス形式
- JSON形式での構造化データ
- プレーンテキスト形式でのフォーマット済み議事録
- エラー時の詳細メッセージ
- 適切なHTTPステータスコード

### 設定管理
- 環境変数からのOpenAI APIキー取得
- グローバルインスタンス管理（processor, formatter）
- 遅延初期化によるエラーハンドリング

## 依存関係
- FastAPI
- Pydantic models
- TranscriptProcessor service
- MeetingMinutesFormatter service
- OpenAI API (環境変数)
- HTTPException

## セキュリティ考慮事項
- APIキーの環境変数管理
- 入力データのサニタイゼーション
- エラーメッセージでの機密情報漏洩防止

## パフォーマンス考慮事項
- グローバルインスタンスによる初期化コスト削減
- AI API呼び出しのタイムアウト設定
- 大きなトランスクリプトの処理制限

## テスト要件
- 正常なリクエスト処理
- 不正なデータでのエラーハンドリング
- AI処理失敗時の処理
- 各エンドポイントの個別テスト
- 統合テスト
- APIキー未設定時のテスト
- 大きなデータでの処理テスト
