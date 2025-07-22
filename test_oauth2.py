#!/usr/bin/env python3
"""
OAuth2 authentication testing script
Tests the complete OAuth2 flow including registration, token generation, and protected endpoints
"""
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_user_registration():
    """Test user registration"""
    print("\nTesting user registration...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print(f"Registration: {response.status_code}")
    if response.status_code == 200:
        print(f"User created: {response.json()}")
        return True
    else:
        print(f"Registration failed: {response.text}")
        return False

def test_token_generation():
    """Test OAuth2 token generation"""
    print("\nTesting OAuth2 token generation...")
    token_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/auth/token", data=token_data)
    print(f"Token generation: {response.status_code}")
    if response.status_code == 200:
        token_info = response.json()
        print(f"Token received: {token_info['token_type']} {token_info['access_token'][:20]}...")
        return token_info['access_token']
    else:
        print(f"Token generation failed: {response.text}")
        return None

def test_protected_endpoint(token):
    """Test protected endpoint with OAuth2 token"""
    print("\nTesting protected endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/users/me", headers=headers)
    print(f"Protected endpoint: {response.status_code}")
    if response.status_code == 200:
        print(f"User info: {response.json()}")
        return True
    else:
        print(f"Protected endpoint failed: {response.text}")
        return False

def test_minutes_generation(token):
    """Test meeting minutes generation with OAuth2 authentication"""
    print("\nTesting meeting minutes generation...")
    headers = {"Authorization": f"Bearer {token}"}
    minutes_data = {
        "meeting_title": "OAuth2 Test Meeting",
        "transcript": "This is a test transcript for OAuth2 authentication testing.",
        "participants": ["testuser"]
    }
    response = requests.post(f"{BASE_URL}/api/v1/minutes/generate", json=minutes_data, headers=headers)
    print(f"Minutes generation: {response.status_code}")
    if response.status_code == 200:
        print("Minutes generation successful!")
        return True
    else:
        print(f"Minutes generation failed: {response.text}")
        return False

def main():
    print("OAuth2 Authentication Testing")
    print("=" * 40)
    
    if not test_health():
        print("Server not responding. Make sure it's running.")
        sys.exit(1)
    
    test_user_registration()
    
    token = test_token_generation()
    if not token:
        print("Cannot proceed without valid token")
        sys.exit(1)
    
    test_protected_endpoint(token)
    test_minutes_generation(token)
    
    print("\nOAuth2 testing completed!")

if __name__ == "__main__":
    main()
