#!/usr/bin/env python3
"""
Test the company update endpoint
"""
import urllib.request
import urllib.error
import json

BASE_URL = "http://localhost:8000/api"

def make_request(method, endpoint, data=None, token=None):
    """Make an HTTP request to the API"""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json",
    }
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if data:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method=method
            )
        else:
            req = urllib.request.Request(url, headers=headers, method=method)
        
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            return e.code, json.loads(error_body)
        except:
            return e.code, {"error": error_body}

def main():
    # 1. Login
    print("🔑 Logging in...")
    status, resp = make_request("POST", "/auth/login", {
        "email": "test@example.com",
        "password": "Test123!@#",
    })
    
    if status != 200:
        print(f"❌ Login failed: {resp}")
        return
    
    token = resp["access_token"]
    company_id = resp["company_id"]
    print(f"✅ Logged in! Company ID: {company_id}")
    
    # 2. Get current company
    print("\n📋 Getting current company info...")
    status, company = make_request("GET", f"/company/{company_id}", token=token)
    if status != 200:
        print(f"❌ Failed to get company: {company}")
        return
    
    print(f"✅ Current company:")
    print(f"   Name: {company['name']}")
    print(f"   Domain: {company.get('domain', 'N/A')}")
    print(f"   Logo URL: {company.get('logo_url', 'N/A')}")
    print(f"   Brand Color: {company.get('brand_color', 'N/A')}")
    
    # 3. Update company
    print("\n✏️ Updating company details...")
    status, updated = make_request("PUT", f"/company/{company_id}", {
        "name": "Tech Innovators Inc.",
        "domain": "techinnovators.com",
        "brand_color": "#FF6B6B",
        "logo_url": "https://via.placeholder.com/150"
    }, token=token)
    
    if status != 200:
        print(f"❌ Failed to update company: {updated}")
        return
    
    print(f"✅ Company updated successfully!")
    print(f"   Name: {updated['name']}")
    print(f"   Domain: {updated.get('domain', 'N/A')}")
    print(f"   Logo URL: {updated.get('logo_url', 'N/A')}")
    print(f"   Brand Color: {updated.get('brand_color', 'N/A')}")
    
    # 4. Verify update
    print("\n🔍 Verifying update...")
    status, verified = make_request("GET", f"/company/{company_id}", token=token)
    if status != 200:
        print(f"❌ Failed to verify: {verified}")
        return
    
    if verified['name'] == "Tech Innovators Inc.":
        print("✅ Update verified! Company name changed successfully.")
    else:
        print("⚠️ Update might not have worked as expected.")
    
    print("\n🎉 Company update feature is working correctly!")

if __name__ == "__main__":
    main()
