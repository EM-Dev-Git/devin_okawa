#!/usr/bin/env python3
"""
Comprehensive debugging script to investigate /login 404 error discrepancy
"""
import sys
import time
import subprocess
import urllib.request
import urllib.error

def test_endpoint(url, description):
    """Test an endpoint and return detailed results"""
    print(f"\n=== {description} ===")
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            headers = dict(response.headers)
            content = response.read().decode('utf-8')
            
            print(f"Status Code: {status_code}")
            print(f"Headers: {headers}")
            if status_code == 404:
                print("❌ 404 ERROR DETECTED!")
                print(f"Response text: {content[:200]}...")
            elif status_code == 200:
                print("✅ 200 OK - Success")
                print(f"Content length: {len(content)}")
            else:
                print(f"⚠️  Unexpected status: {status_code}")
            return status_code
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        if e.code == 404:
            print("❌ 404 ERROR DETECTED!")
        return e.code
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def test_curl_command(url, description):
    """Test using curl command"""
    print(f"\n=== {description} ===")
    try:
        result = subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', url],
            capture_output=True, text=True, timeout=10
        )
        status_code = result.stdout.strip()
        print(f"Curl status code: {status_code}")
        if status_code == "404":
            print("❌ 404 ERROR DETECTED via curl!")
        elif status_code == "200":
            print("✅ 200 OK via curl")
        return status_code
    except Exception as e:
        print(f"❌ Curl failed: {e}")
        return None

def main():
    base_url = "http://localhost:8000"
    
    print("🔍 COMPREHENSIVE /login ENDPOINT DEBUG")
    print("=" * 50)
    
    test_urls = [
        (f"{base_url}/login", "Direct /login access"),
        (f"http://127.0.0.1:8000/login", "127.0.0.1 /login access"),
        (f"{base_url}/", "Root path (should redirect)"),
        (f"{base_url}/register", "Register page"),
        (f"{base_url}/health", "Health check"),
        (f"{base_url}/api/v1/auth/login", "API login endpoint (should be 405)"),
    ]
    
    results = {}
    
    print("\n🐍 TESTING WITH PYTHON REQUESTS")
    for url, desc in test_urls:
        results[f"requests_{desc}"] = test_endpoint(url, f"Requests: {desc}")
    
    print("\n🌐 TESTING WITH CURL")
    for url, desc in test_urls:
        results[f"curl_{desc}"] = test_curl_command(url, f"Curl: {desc}")
    
    print("\n📊 SUMMARY OF RESULTS")
    print("=" * 50)
    login_404_count = 0
    login_200_count = 0
    
    for test_name, status in results.items():
        if "/login" in test_name and not "api" in test_name:
            if status == 404 or status == "404":
                login_404_count += 1
                print(f"❌ {test_name}: 404 NOT FOUND")
            elif status == 200 or status == "200":
                login_200_count += 1
                print(f"✅ {test_name}: 200 OK")
            else:
                print(f"⚠️  {test_name}: {status}")
    
    print(f"\n📈 LOGIN ENDPOINT RESULTS:")
    print(f"   200 OK responses: {login_200_count}")
    print(f"   404 NOT FOUND responses: {login_404_count}")
    
    if login_404_count > 0:
        print("\n🚨 404 ERRORS DETECTED!")
        print("This matches the user's reported issue.")
    elif login_200_count > 0 and login_404_count == 0:
        print("\n✅ ALL LOGIN TESTS SUCCESSFUL")
        print("No 404 errors found - discrepancy with user's experience.")
    
    print("\n🔧 NEXT STEPS:")
    if login_404_count > 0:
        print("- 404 errors reproduced - investigate route registration")
        print("- Check middleware interference")
        print("- Verify FastAPI app configuration")
    else:
        print("- Unable to reproduce 404 error in this environment")
        print("- May be timing-related or environment-specific")
        print("- Consider server restart or configuration differences")

if __name__ == "__main__":
    main()
