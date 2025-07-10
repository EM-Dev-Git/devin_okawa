# API Endpoints 作業計画書

## 概要
FastAPI議事録生成システムのAPIエンドポイント設計と実装

## エンドポイント仕様

### 1. GET /healthz
**目的**: APIの健全性チェック
**レスポンス**: `{"status": "ok"}`
**エラーハンドリング**: なし（常に200を返す）

### 2. POST /process-transcript
**目的**: トランスクリプトを処理して構造化された議事録データを生成
**入力**: TranscriptRequest (header + transcript)
**出力**: MeetingMinutes
**処理フロー**:
1. TranscriptProcessorインスタンス取得
2. AI処理実行
3. 構造化データ返却
**エラーハンドリング**:
- OpenAI API呼び出し失敗 → 500エラー
- JSON解析エラー → 500エラー
- APIキー未設定 → 500エラー

### 3. POST /format-minutes
**目的**: 構造化された議事録データをテキスト形式に変換
**入力**: MeetingMinutes
**出力**: `{"formatted_minutes": "テキスト形式の議事録"}`
**処理フロー**:
1. MeetingMinutesFormatterでテキスト変換
2. フォーマット済みテキスト返却
**エラーハンドリング**:
- フォーマットエラー → 500エラー

### 4. POST /generate-minutes
**目的**: トランスクリプト処理とフォーマットを一括実行
**入力**: TranscriptRequest
**出力**: `{"formatted_minutes": "テキスト", "structured_data": MeetingMinutes}`
**処理フロー**:
1. process-transcriptと同様の処理
2. format-minutesと同様の処理
3. 両方の結果を返却
**エラーハンドリング**: 上記2つのエンドポイントのエラーを統合

## データモデル

### TranscriptRequest
- header: MeetingHeader
- transcript: str

### MeetingHeader
- title: str
- date: str
- location: str
- participants: List[str]
- absent_members: List[str] (デフォルト: [])
- facilitator: str

### MeetingMinutes
- ヘッダー情報 + 構造化データ
- daily_goals: List[PersonGoal]
- progress_and_issues: List[PersonProgress]
- problem_solutions: List[PersonSolution]
- next_meeting_content: List[str] (固定値)

## セキュリティ考慮事項
- OpenAI APIキーの環境変数管理
- CORS設定（開発用に全許可）
- 入力データの検証（Pydanticによる自動検証）

## パフォーマンス考慮事項
- TranscriptProcessorのシングルトンパターン
- OpenAIクライアントの再利用
- エラー時の適切なHTTPステータスコード

## テスト要件
- 各エンドポイントの正常系テスト
- エラーハンドリングのテスト
- データ検証のテスト
- OpenAI API統合テスト（モック使用）
