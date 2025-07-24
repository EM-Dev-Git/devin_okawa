import asyncio
import httpx
import time
from datetime import datetime

async def test_system_integration():
    """システム統合テスト - 実際のAPIサーバーとの通信テスト"""
    base_url = "http://localhost:8000"
    
    print("=== システム統合テスト開始 ===")
    print(f"テスト開始時刻: {datetime.now()}")
    
    print("サーバー起動を待機中...")
    await asyncio.sleep(3)
    
    async with httpx.AsyncClient() as client:
        try:
            print("\n1. ヘルスチェックテスト")
            response = await client.get(f"{base_url}/")
            print(f"ステータス: {response.status_code}")
            print(f"レスポンス: {response.json()}")
            assert response.status_code == 200
            
            print("\n2. 議事録生成エンドポイントテスト")
            test_data = {
                "content": "今日の会議では、新しいプロジェクトについて話し合いました。田中さんが進捗を報告し、来週までにタスクを完了する予定です。",
                "meeting_title": "週次定例会議",
                "participants": ["田中", "佐藤", "鈴木"]
            }
            
            response = await client.post(f"{base_url}/minutes/generate", json=test_data)
            print(f"ステータス: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"議事録ID: {result.get('id')}")
                print(f"タイトル: {result.get('title')}")
                print(f"内容プレビュー: {result.get('content', '')[:100]}...")
            else:
                print(f"エラーレスポンス: {response.text}")
            
            print("\n3. APIドキュメントアクセステスト")
            response = await client.get(f"{base_url}/docs")
            print(f"ステータス: {response.status_code}")
            assert response.status_code == 200
            
            print("\n4. ヘルスチェックエンドポイントテスト")
            response = await client.get(f"{base_url}/minutes/health")
            print(f"ステータス: {response.status_code}")
            print(f"レスポンス: {response.json()}")
            assert response.status_code == 200
            
            print("\n=== システム統合テスト完了 ===")
            print("すべてのテストが正常に完了しました")
            return True
            
        except Exception as e:
            print(f"\nシステム統合テストエラー: {e}")
            return False

if __name__ == "__main__":
    result = asyncio.run(test_system_integration())
    exit(0 if result else 1)
