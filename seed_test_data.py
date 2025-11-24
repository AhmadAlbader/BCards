#!/usr/bin/env python3
"""
Seed test data for Digital Business Cards
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
    # 1. Sign up
    print("📝 Signing up test user...")
    status, resp = make_request("POST", "/auth/signup", {
        "email": "test@example.com",
        "password": "Test123!@#",
        "full_name": "Test Admin",
    })
    
    if status == 400:
        print("⚠️ User already exists, logging in...")
        status, resp = make_request("POST", "/auth/login", {
            "email": "test@example.com",
            "password": "Test123!@#",
        })
        if status != 200:
            print(f"❌ Login failed: {resp}")
            return
    elif status != 200:
        print(f"❌ Signup failed: {resp}")
        return
    
    token = resp["access_token"]
    company_id = resp["company_id"]
    print(f"✅ Authenticated! Company ID: {company_id}")
    
    # 2. Get company info
    print("\n📋 Getting company info...")
    status, company = make_request("GET", f"/company/{company_id}", token=token)
    if status != 200:
        print(f"❌ Failed to get company: {company}")
        return
    
    company_slug = company.get("slug", "unknown")
    print(f"✅ Company slug: {company_slug}")
    print(f"   Name: {company['name']}")
    
    # 3. Create test employees
    print("\n👥 Creating test employees...")
    employees_data = [
        {
            "full_name": "Alice Johnson",
            "job_title": "CEO",
            "email": "alice@example.com",
            "phone": "+1234567890",
            "whatsapp": "12345678900",
            "bio": "CEO with 15 years of experience",
            "social_links": {
                "linkedin": "https://linkedin.com/in/alice",
                "twitter": "https://twitter.com/alice"
            }
        },
        {
            "full_name": "Bob Smith",
            "job_title": "Senior Developer",
            "email": "bob@example.com",
            "phone": "+1234567891",
            "whatsapp": "12345678901",
            "bio": "Full-stack developer passionate about innovation",
            "social_links": {
                "linkedin": "https://linkedin.com/in/bob",
                "github": "https://github.com/bob"
            }
        },
        {
            "full_name": "Carol White",
            "job_title": "Designer",
            "email": "carol@example.com",
            "phone": "+1234567892",
            "whatsapp": "12345678902",
            "bio": "Creative designer focused on user experience",
            "social_links": {
                "instagram": "https://instagram.com/carol",
                "linkedin": "https://linkedin.com/in/carol"
            }
        }
    ]
    
    created_employees = []
    for emp_data in employees_data:
        status, emp = make_request("POST", f"/company/{company_id}/employees", emp_data, token=token)
        
        if status != 200:
            print(f"❌ Failed to create employee: {emp}")
            continue
        
        created_employees.append(emp)
        print(f"✅ Created: {emp['full_name']}")
        print(f"   Public slug: {emp['public_slug']}")
        print(f"   Card URL: http://localhost:3000/card/{company_slug}/{emp['public_slug']}")
    
    print("\n📱 Generated Card URLs:")
    for emp in created_employees:
        print(f"  • {emp['full_name']}")
        print(f"    URL: http://localhost:3000/card/{company_slug}/{emp['public_slug']}")
    
    print("\n✅ Test data seeded successfully!")
    if created_employees:
        print(f"\n🔗 Try visiting: http://localhost:3000/card/{company_slug}/{created_employees[0]['public_slug']}")

if __name__ == "__main__":
    main()
