#!/usr/bin/env python3
"""
WSL compatibility testing script
Tests various networking configurations to identify WSL issues
"""
import urllib.request
import urllib.error
import json
import sys

def test_endpoint(url, description):
    """Test an endpoint and return results"""
    print(f"\n--- {description} ---")
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.getcode()
            content = response.read().decode('utf-8')
            print(f"✅ Status: {status}")
            if status == 200:
                print(f"   Content length: {len(content)}")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        if e.code == 404:
            print("   🚨 404 ERROR - This confirms the WSL networking issue!")
        return False
    except Exception as e:
        print(f"⚠️  Connection failed: {e}")
        return False

def main():
    print("🔍 WSL COMPATIBILITY TEST")
    print("=" * 50)
    print("This script tests various URLs to identify WSL networking issues.")
    print("Run this after starting the server with different host bindings.\n")
    
    test_urls = [
        ("http://localhost:8000/health", "Health check via localhost"),
        ("http://127.0.0.1:8000/health", "Health check via 127.0.0.1"),
        ("http://localhost:8000/login", "Login page via localhost"),
        ("http://127.0.0.1:8000/login", "Login page via 127.0.0.1"),
        ("http://localhost:8000/debug/routes", "Debug routes"),
        ("http://localhost:8000/debug/network", "Debug network info"),
    ]
    
    results = []
    for url, description in test_urls:
        success = test_endpoint(url, description)
        results.append((url, success))
    
    print("\n📊 SUMMARY")
    print("=" * 50)
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)
    
    print(f"Successful requests: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("✅ All tests passed! WSL networking is working correctly.")
    elif success_count == 0:
        print("❌ All tests failed! Check if the server is running.")
        print("   Try starting with: python start_wsl.py")
    else:
        print("⚠️  Mixed results. Some URLs work, others don't.")
        print("   This may indicate partial WSL networking issues.")
    
    print("\n🔧 TROUBLESHOOTING STEPS:")
    print("1. Ensure server is running with WSL-compatible binding:")
    print("   python start_wsl.py")
    print("2. Try different host bindings if issues persist")
    print("3. Check Windows Defender firewall settings")
    print("4. Verify WSL version: wsl --version")

if __name__ == "__main__":
    main()
