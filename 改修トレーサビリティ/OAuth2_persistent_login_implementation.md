# OAuth2 永続ログイン機能実装 - 改修トレーサビリティ

## 概要
main_okawa_20250722ブランチのOAuth2認証機能をmain_okawa_20250724ブランチに移植し、永続ログイン機能を追加する。

## 改修前後比較

### main_okawa_20250722 (改修前 - 参照実装)
```
src/
├── routers/
│   └── auth.py          # OAuth2認証エンドポイント
├── modules/
│   ├── auth.py          # JWT認証ロジック
│   └── user_store.py    # インメモリユーザーストア
├── dependencies/
│   └── auth.py          # 認証依存関係
├── schemas/
│   └── auth.py          # 認証スキーマ
└── config.py            # JWT設定含む
```

**機能:**
- ユーザー登録/ログイン
- JWT トークン認証 (30分有効期限)
- パスワードハッシュ化 (bcrypt)
- インメモリユーザーストレージ
- 包括的テストスイート

### main_okawa_20250724 (改修前 - 現在の状態)
```
src/
├── routers/
│   └── minutes.py       # 議事録API のみ
├── modules/
│   ├── azure_openai_client.py
│   ├── transcript_processor.py
│   └── logger.py
├── schemas/
│   ├── transcript.py
│   └── minutes.py
└── config.py            # Azure OpenAI設定のみ
```

**機能:**
- 議事録生成API
- Azure OpenAI統合
- 認証機能なし

### main_okawa_20250724 (改修後 - 計画)
```
src/
├── routers/
│   ├── auth.py          # OAuth2認証エンドポイント (新規)
│   └── minutes.py       # 議事録API (既存)
├── modules/
│   ├── auth.py          # JWT + リフレッシュトークン認証 (新規)
│   ├── user_store.py    # 永続ユーザーストア (新規)
│   ├── azure_openai_client.py (既存)
│   ├── transcript_processor.py (既存)
│   └── logger.py (既存)
├── dependencies/
│   └── auth.py          # 認証依存関係 (新規)
├── schemas/
│   ├── auth.py          # 認証スキーマ (新規)
│   ├── transcript.py (既存)
│   └── minutes.py (既存)
└── config.py            # JWT + Azure OpenAI設定 (更新)
```

**新機能:**
- OAuth2 JWT認証 (main_okawa_20250722から移植)
- **リフレッシュトークン** による永続ログイン
- **Remember Me** 機能 (長期間有効なトークン)
- **セッション管理** (オプション)
- ファイルベース永続ユーザーストレージ
- 認証付き議事録API

## 実装計画

### Phase 1: OAuth2基本機能移植
1. 認証関連ファイルの移植と適応
2. config.pyにJWT設定追加
3. 基本テストの移植

### Phase 2: 永続ログイン機能追加
1. リフレッシュトークン機能実装
2. Remember Me機能実装
3. 永続ユーザーストレージ実装

### Phase 3: 統合とテスト
1. 議事録APIに認証追加
2. 包括的テスト実装
3. ドキュメント更新

## セキュリティ考慮事項
- リフレッシュトークンの安全な保存
- トークンローテーション
- セッション管理
- CSRF保護

## 実装詳細
[実装中に詳細を追記]

## テスト計画
[実装中にテスト計画を追記]

## 実装結果
[実装完了後に結果を記録]
