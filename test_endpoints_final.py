#!/usr/bin/env python3
"""Test vCard and QR code endpoints."""
import urllib.request
import urllib.error
import ssl

# Skip SSL verification for localhost
ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = "http://localhost:8000/api"
COMPANY_SLUG = "test-admin-s-company-8f8d7331"
EMPLOYEE_SLUG = "alice-johnson-b45d8511"

def test_endpoint(endpoint, expected_status=200):
    """Test an endpoint and report results."""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n📡 Testing: GET {endpoint}")
    try:
        with urllib.request.urlopen(url, context=ssl._create_unverified_context()) as response:
            status = response.status
            headers = dict(response.headers)
            content_type = headers.get('Content-Type', 'unknown')
            
            if status == expected_status or status in [200, 307]:
                print(f"   ✅ Status: {status}")
                print(f"   📄 Content-Type: {content_type}")
                    
                # Show first 200 chars of response
                body = response.read().decode('utf-8', errors='ignore')[:200]
                if body:
                    print(f"   📝 Preview: {body}...")
                return True
            else:
                print(f"   ❌ Unexpected status: {status}")
                return False
    except urllib.error.HTTPError as e:
        print(f"   ❌ HTTP Error {e.code}: {e.reason}")
        if e.code != 404:
            body = e.read().decode('utf-8', errors='ignore')[:200]
            print(f"   Response: {body}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

# Test vCard endpoint
print("=" * 60)
print("🎯 TESTING vCard ENDPOINT")
print("=" * 60)
vcard_endpoint = f"/card/{COMPANY_SLUG}/{EMPLOYEE_SLUG}/vcard"
test_endpoint(vcard_endpoint, 200)

# Test QR endpoint
print("\n" + "=" * 60)
print("�� TESTING QR CODE ENDPOINT")
print("=" * 60)
qr_endpoint = f"/card/{COMPANY_SLUG}/{EMPLOYEE_SLUG}/qr-vcard"
test_endpoint(qr_endpoint, 307)

print("\n" + "=" * 60)
print("✨ ENDPOINT TESTING COMPLETE")
print("=" * 60)
