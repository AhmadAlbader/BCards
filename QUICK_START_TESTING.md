# ⚡ Quick Reference - Admin Dashboard Testing

## 🎯 Access the Dashboard

```
URL: http://localhost:3000/company-admin/dashboard
```

## 📋 Current Status

| Component | Status |
|-----------|--------|
| Backend API | ✅ Running on port 8000 |
| Frontend | ✅ Running on port 3000 |
| Database | ✅ PostgreSQL healthy |
| Authentication | ✅ Bearer tokens working |
| Add Employee | ✅ **NOW FIXED** |

## 🔑 Test Credentials (Create New)

If you want to test:

1. Go to: http://localhost:3000/auth/signup
2. Enter:
   - Email: `test{timestamp}@example.com` (use unique email)
   - Password: `TestPass123!`
   - Full Name: Your name
3. Click Sign Up

## 📝 To Add an Employee

1. Dashboard loads with "Admin Dashboard" header
2. Click blue "+ Add Employee" button
3. Fill the form:
   ```
   Full Name:   John Smith (required)
   Job Title:   Developer
   Email:       john@company.com
   Phone:       +1-555-1234
   ```
4. Click "Add Employee"
5. ✅ Employee appears in the list below

## 🔄 What's Happening Behind the Scenes

### Frontend sends:
```
POST /api/company/{companyId}/employees
Authorization: Bearer {jwtToken}
Content-Type: application/json

{
  "full_name": "John Smith",
  "job_title": "Developer",
  "email": "john@company.com",
  "phone": "+1-555-1234"
}
```

### Backend does:
1. Extracts Bearer token from Authorization header ✅ (this was the bug)
2. Validates JWT signature and expiration
3. Checks multi-tenant permissions
4. Creates employee record
5. Returns employee data with public_slug

### Frontend receives:
```json
{
  "id": "uuid-here",
  "full_name": "John Smith",
  "job_title": "Developer",
  "email": "john@company.com",
  "phone": "+1-555-1234",
  "public_slug": "john-smith-random",
  "company_id": "your-company-uuid"
}
```

Then displays in the list!

## 🐛 If Something Still Doesn't Work

### Check Docker Containers
```bash
docker ps
```

Should show:
- `digital-cards-frontend` (port 3000)
- `digital-cards-backend` (port 8000)
- `digital-cards-db` (PostgreSQL)

### Check Backend Logs
```bash
docker logs digital-cards-backend -f
```

### Restart Backend (if needed)
```bash
docker restart digital-cards-backend
```

### View Frontend Console
- Open http://localhost:3000
- Press F12 for DevTools
- Check Console tab for errors

## 📱 Employee Card URLs

Once you add an employee, their public card URL will be:

```
http://localhost:3000/card/{company-slug}/{employee-slug}

Example:
http://localhost:3000/card/alice-johnson-s-company-c3d4a08b/john-smith-random
```

## 🧪 API Testing Tools

### Using curl:
```bash
# Get your token first (from localStorage after login)
TOKEN="eyJhbGciOiJIUzI1NiIs..."

# Add employee
curl -X POST http://localhost:8000/api/company/{companyId}/employees \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Jane Developer",
    "job_title": "DevOps Engineer",
    "email": "jane@company.com",
    "phone": "+1-555-5678"
  }'
```

### Using Postman:
1. Set Authorization type to "Bearer Token"
2. Paste your JWT in the token field
3. POST to `http://localhost:8000/api/company/{companyId}/employees`
4. Add JSON body with employee data

## ✅ Success Indicators

You'll know it's working when:

1. ✅ Dashboard loads without redirect to login
2. ✅ "+ Add Employee" button is clickable
3. ✅ Form submits without error
4. ✅ New employee appears in list immediately
5. ✅ Employee has a "View Card" link
6. ✅ No console errors in browser DevTools

## 🚨 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| "Missing token" error | Ensure token is stored in localStorage |
| "Not authorized" error | Login again with correct credentials |
| 500 error on list employees | Restart backend: `docker restart digital-cards-backend` |
| Form won't submit | Check browser console for CORS errors |
| Employee doesn't appear | Refresh page (F5) or check backend logs |

## 📚 Documentation Files

- **TEST_REPORT.md** - Comprehensive test results
- **FIXES_APPLIED.md** - Detailed fix explanations
- **API_REFERENCE.md** - Full API documentation
- **ARCHITECTURE.md** - System architecture details

---

**Everything is ready to use!** 🎉

Start testing by going to: **http://localhost:3000/company-admin/dashboard**
