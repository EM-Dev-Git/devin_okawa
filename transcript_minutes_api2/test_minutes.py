import requests
import json

login_response = requests.post("http://localhost:8001/auth/login", json={
    "username": "testuser",
    "password": "password123"
})

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"Login successful, token: {token[:20]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    minutes_data = {
        "title": "テスト会議",
        "transcript": "今日の会議では、プロジェクトの進捗について話し合いました。田中さんからは開発状況の報告があり、来週までにテスト環境の構築を完了する予定です。佐藤さんからはマーケティング戦略について提案がありました。"
    }
    
    response = requests.post("http://localhost:8001/minutes/generate", 
                           json=minutes_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print("Minutes generation successful!")
        print(f"Generated minutes ID: {result['id']}")
        print(f"Title: {result['title']}")
        print(f"Generated content length: {len(result['generated_minutes'])} characters")
    else:
        print(f"Minutes generation failed: {response.status_code}")
        print(response.text)
else:
    print(f"Login failed: {login_response.status_code}")
    print(login_response.text)
