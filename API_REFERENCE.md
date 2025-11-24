# 🔌 API Quick Reference

## Base URL
```
http://localhost:8000/api
```

## Authentication

### Get Token (Signup)
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@mycompany.com",
    "password": "SecurePassword123",
    "full_name": "John Admin",
    "role": "admin"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "company_id": "550e8400-e29b-41d4-a716-446655440001",
  "role": "admin"
}
```

### Get Token (Login)
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@mycompany.com",
    "password": "SecurePassword123"
  }'
```

## Using Token in Requests
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/company/{company_id}/employees
```

---

## Company Management

### Create Company (Admin)
```bash
curl -X POST http://localhost:8000/api/company \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corp",
    "domain": "acme.com",
    "logo_url": "https://example.com/logo.png",
    "brand_color": "#3B82F6"
  }'
```

### Get Company Details (Admin)
```bash
curl -H "Authorization: Bearer {token}" \
  http://localhost:8000/api/company/{company_id}
```

---

## Employee Management

### Add Employee (Admin)
```bash
curl -X POST http://localhost:8000/api/company/{company_id}/employees \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Jane Smith",
    "job_title": "Sales Manager",
    "email": "jane@acme.com",
    "phone": "+1234567890",
    "whatsapp": "+1234567890",
    "photo_url": "https://example.com/jane.jpg",
    "bio": "Experienced sales professional with 10+ years",
    "social_links": {
      "linkedin": "https://linkedin.com/in/janesmith",
      "twitter": "https://twitter.com/janesmith"
    }
  }'
```

### List Company Employees (Admin)
```bash
curl -H "Authorization: Bearer {token}" \
  "http://localhost:8000/api/company/{company_id}/employees?skip=0&limit=100"
```

### Get Employee Details (Admin/Employee)
```bash
curl -H "Authorization: Bearer {token}" \
  http://localhost:8000/api/employees/{employee_id}
```

### Update Employee Profile
```bash
curl -X PUT http://localhost:8000/api/employees/{employee_id} \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Senior Sales Manager",
    "bio": "Now with 15+ years of experience"
  }'
```

---

## Public Card Endpoints (No Auth Required)

### View Public Card
```bash
curl http://localhost:8000/api/card/{company_slug}/{employee_slug}
```

**Response:**
```json
{
  "employee_id": "550e8400-e29b-41d4-a716-446655440000",
  "employee_name": "Jane Smith",
  "company_name": "Acme Corp",
  "company_id": "550e8400-e29b-41d4-a716-446655440001",
  "job_title": "Sales Manager",
  "email": "jane@acme.com",
  "phone": "+1234567890",
  "whatsapp": "+1234567890",
  "bio": "Experienced sales professional",
  "photo_url": "https://example.com/jane.jpg",
  "social_links": {
    "linkedin": "https://linkedin.com/in/janesmith",
    "twitter": "https://twitter.com/janesmith"
  },
  "qr_code": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=...",
  "vcard_url": "/card/acme-corp/jane-smith-abc123/vcard",
  "company_logo": "https://example.com/logo.png",
  "company_brand_color": "#3B82F6"
}
```

---

## Analytics

### Track Event (No Auth Required)
```bash
curl -X POST "http://localhost:8000/api/analytics/track?company_slug=acme-corp&employee_slug=jane-smith-abc123" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "view",
    "device": "mobile",
    "region": "US"
  }'
```

**Supported Actions:**
- `view` — Card page view
- `call` — Phone call initiated
- `email` — Email clicked
- `whatsapp` — WhatsApp opened
- `download_vcard` — vCard downloaded
- `scan_qr` — QR code scanned

### Get Company Analytics (Admin)
```bash
curl -H "Authorization: Bearer {token}" \
  "http://localhost:8000/api/analytics/company/{company_id}?skip=0&limit=1000"
```

**Response:**
```json
{
  "events": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "employee_id": "550e8400-e29b-41d4-a716-446655440001",
      "company_id": "550e8400-e29b-41d4-a716-446655440002",
      "timestamp": "2025-11-18T10:30:00",
      "device": "mobile",
      "region": "US",
      "action": "view"
    }
  ],
  "summary": {
    "view": 45,
    "call": 12,
    "whatsapp": 8,
    "email": 5,
    "download_vcard": 3,
    "scan_qr": 2
  }
}
```

### Get Employee Analytics (Admin/Employee)
```bash
curl -H "Authorization: Bearer {token}" \
  "http://localhost:8000/api/analytics/employee/{employee_id}?skip=0&limit=1000"
```

---

## Health Check (Public)
```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "ok"
}
```

---

## Common Response Codes

| Code | Meaning |
|------|---------|
| `200` | Success |
| `201` | Created |
| `400` | Bad request (validation error) |
| `401` | Unauthorized (missing/invalid token) |
| `403` | Forbidden (insufficient permissions) |
| `404` | Not found |
| `500` | Server error |

---

## Error Response Format

```json
{
  "detail": "Invalid credentials"
}
```

---

## Testing in cURL

### Save token to variable
```bash
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@acme.com", "password": "pass"}' \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

echo "Token: $TOKEN"
```

### Use token in subsequent requests
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/company/{company_id}/employees
```

---

## API Documentation (Interactive)

Visit: **http://localhost:8000/docs**

- Swagger UI (interactive testing)
- Real-time API documentation
- Try endpoints directly from browser

---

## Useful Tips

1. **Get your company_id** from signup/login response
2. **Replace {company_slug}** with your company's slug (e.g., "acme-corp")
3. **Replace {employee_slug}** with employee's slug (auto-generated)
4. **Pagination:** Use `skip` and `limit` query parameters (default: skip=0, limit=100)
5. **All endpoints return JSON** — use `Content-Type: application/json`
6. **Tokens expire** after 7 days — need to login again

---

## Testing Workflow

```bash
# 1. Signup (creates company + user)
SIGNUP_RESPONSE=$(curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123",
    "full_name": "Test User",
    "role": "admin"
  }')

# 2. Extract token and company_id
TOKEN=$(echo $SIGNUP_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
COMPANY_ID=$(echo $SIGNUP_RESPONSE | grep -o '"company_id":"[^"]*' | cut -d'"' -f4)

# 3. Add employee
curl -X POST http://localhost:8000/api/company/$COMPANY_ID/employees \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Employee",
    "job_title": "Developer"
  }'

# 4. List employees
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/company/$COMPANY_ID/employees
```

---

**Happy coding! 🎉**
