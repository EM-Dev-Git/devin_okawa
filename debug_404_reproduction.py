#!/usr/bin/env python3
"""
Debug script to try reproducing the 404 error the user is experiencing
"""
import sys
import time
import subprocess
import urllib.request
import urllib.error
import threading
import json

def test_rapid_requests():
    """Test rapid consecutive requests to see if there's a race condition"""
    print("\n🚀 TESTING RAPID CONSECUTIVE REQUESTS")
    print("=" * 50)
    
    results = []
    for i in range(10):
        try:
            req = urllib.request.Request("http://localhost:8000/login")
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.getcode()
                results.append(status)
                print(f"Request {i+1}: {status}")
        except urllib.error.HTTPError as e:
            results.append(e.code)
            print(f"Request {i+1}: {e.code} ERROR")
        except Exception as e:
            results.append(None)
            print(f"Request {i+1}: FAILED - {e}")
        time.sleep(0.1)  # Small delay between requests
    
    error_count = sum(1 for r in results if r == 404)
    if error_count > 0:
        print(f"❌ Found {error_count} 404 errors in rapid requests!")
    else:
        print("✅ No 404 errors in rapid requests")
    
    return results

def test_concurrent_requests():
    """Test concurrent requests to see if there's a threading issue"""
    print("\n🔄 TESTING CONCURRENT REQUESTS")
    print("=" * 50)
    
    results = []
    threads = []
    
    def make_request(thread_id):
        try:
            req = urllib.request.Request("http://localhost:8000/login")
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.getcode()
                results.append((thread_id, status))
                print(f"Thread {thread_id}: {status}")
        except urllib.error.HTTPError as e:
            results.append((thread_id, e.code))
            print(f"Thread {thread_id}: {e.code} ERROR")
        except Exception as e:
            results.append((thread_id, None))
            print(f"Thread {thread_id}: FAILED - {e}")
    
    for i in range(5):
        thread = threading.Thread(target=make_request, args=(i+1,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    error_count = sum(1 for _, status in results if status == 404)
    if error_count > 0:
        print(f"❌ Found {error_count} 404 errors in concurrent requests!")
    else:
        print("✅ No 404 errors in concurrent requests")
    
    return results

def test_server_restart_timing():
    """Test if there's a timing issue during server startup"""
    print("\n⏰ TESTING SERVER RESTART TIMING")
    print("=" * 50)
    print("Note: This test requires manual server restart")
    
    print("Testing request timing after server startup...")
    
    for delay in [0.1, 0.5, 1.0, 2.0, 5.0]:
        print(f"\nTesting with {delay}s delay:")
        time.sleep(delay)
        try:
            req = urllib.request.Request("http://localhost:8000/login")
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.getcode()
                print(f"  Delay {delay}s: {status}")
        except urllib.error.HTTPError as e:
            print(f"  Delay {delay}s: {e.code} ERROR")
            if e.code == 404:
                print("  ❌ 404 ERROR FOUND!")
        except Exception as e:
            print(f"  Delay {delay}s: FAILED - {e}")

def test_different_paths():
    """Test different path variations that might cause issues"""
    print("\n🛤️  TESTING PATH VARIATIONS")
    print("=" * 50)
    
    test_paths = [
        "/login",
        "/login/",
        "/Login",
        "/LOGIN",
        "//login",
        "/login//",
        "/login?",
        "/login#",
    ]
    
    results = {}
    for path in test_paths:
        url = f"http://localhost:8000{path}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.getcode()
                results[path] = status
                print(f"Path '{path}': {status}")
        except urllib.error.HTTPError as e:
            results[path] = e.code
            print(f"Path '{path}': {e.code}")
            if e.code == 404:
                print(f"  ❌ 404 ERROR for path '{path}'!")
        except Exception as e:
            results[path] = None
            print(f"Path '{path}': FAILED - {e}")
    
    return results

def test_headers_and_user_agents():
    """Test with different headers and user agents"""
    print("\n🌐 TESTING DIFFERENT HEADERS/USER AGENTS")
    print("=" * 50)
    
    test_configs = [
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
        {"User-Agent": "curl/7.81.0"},
        {"User-Agent": "Python-urllib/3.12"},
        {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
        {"Accept": "application/json"},
        {"Connection": "close"},
        {"Connection": "keep-alive"},
    ]
    
    for i, headers in enumerate(test_configs):
        try:
            req = urllib.request.Request("http://localhost:8000/login")
            for key, value in headers.items():
                req.add_header(key, value)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.getcode()
                print(f"Config {i+1} {headers}: {status}")
        except urllib.error.HTTPError as e:
            print(f"Config {i+1} {headers}: {e.code}")
            if e.code == 404:
                print(f"  ❌ 404 ERROR with headers {headers}!")
        except Exception as e:
            print(f"Config {i+1} {headers}: FAILED - {e}")

def main():
    print("🔍 ADVANCED 404 ERROR REPRODUCTION TESTING")
    print("=" * 60)
    print("Attempting to reproduce the user's 404 error...")
    
    rapid_results = test_rapid_requests()
    concurrent_results = test_concurrent_requests()
    test_server_restart_timing()
    path_results = test_different_paths()
    test_headers_and_user_agents()
    
    print("\n📊 FINAL SUMMARY")
    print("=" * 60)
    
    total_404s = 0
    total_404s += sum(1 for r in rapid_results if r == 404)
    total_404s += sum(1 for _, r in concurrent_results if r == 404)
    total_404s += sum(1 for r in path_results.values() if r == 404)
    
    if total_404s > 0:
        print(f"🚨 FOUND {total_404s} 404 ERRORS!")
        print("This may help explain the user's issue.")
    else:
        print("✅ NO 404 ERRORS FOUND")
        print("Unable to reproduce the user's 404 error.")
        print("The issue may be:")
        print("- Environment-specific configuration")
        print("- Browser cache/cookies")
        print("- Network/proxy issues")
        print("- Server startup timing")
        print("- Different FastAPI/Python versions")

if __name__ == "__main__":
    main()
