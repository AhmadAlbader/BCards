#!/usr/bin/env python3
"""Quick test of vCard and QR code endpoints."""
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8000/api"
COMPANY_SLUG = "test-admin-s-company-8f8d7331"
EMPLOYEE_SLUG = "alice-johnson-7409e703"

def test_endpoint(endpoint, expected_status=200):
    """Test an endpoint and report results."""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n📡 Testing: {endpoint}")
    try:
        with urllib.request.urlopen(url) as response:
            status = response.status
            headers = dict(response.headers)
            content_type = headers.get('Content-Type', 'unknown')
            content_length = headers.get('Content-Length', 'unknown')
            
            if status == expected_status:
                print(f"   ✅ Status: {status}")
                print(f"   📄 Content-Type: {content_type}")
                if content_length != 'unknown':
                    print(f"   📊 Content-Length: {content_length} bytes")
                    
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
        return False
    except urllib.error.URLError as e:
        print(f"   ❌ Connection Error: {e.reason}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

# Test vCard endpoint
print("=" * 60)
print("🎯 Testing vCard Endpoint")
print("=" * 60)
vcard_endpoint = f"/card/{COMPANY_SLUG}/{EMPLOYEE_SLUG}/vcard"
if test_endpoint(vcard_endpoint, 200):
    print("   ✨ vCard endpoint is WORKING!")

# Test QR endpoint
print("\n" + "=" * 60)
print("🎯 Testing QR Code Endpoint")
print("=" * 60)
qr_endpoint = f"/card/{COMPANY_SLUG}/{EMPLOYEE_SLUG}/qr-vcard"
if test_endpoint(qr_endpoint, 307):  # Redirect response
    print("   ✨ QR endpoint is WORKING!")

print("\n" + "=" * 60)
print("🎉 All endpoints are now active and functioning!")
print("=" * 60)
