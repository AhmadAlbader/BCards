# Railway Environment Variables Setup

## Required Variables for Backend Service

Add these variables in Railway Dashboard → Backend Service → Variables:

### 1. Security (REQUIRED)
```bash
SECRET_KEY=f4B67kq4lNKcpgpJHVcmrqXQvUAJ0okkAryA7lFVunqcTVGjiCLw+W8W0NUxKdg1m0Vdl9ClSQNJ6QgpXbv/SQ==
```

### 2. Stripe Keys (Use Test Keys First)
```bash
STRIPE_SECRET_KEY=sk_test_YOUR_TEST_KEY_HERE
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_TEST_PUBLISHABLE_KEY_HERE
STRIPE_WEBHOOK_SECRET=whsec_YOUR_TEST_WEBHOOK_SECRET_HERE
```

**Get test keys from:** https://dashboard.stripe.com/test/apikeys

### 3. Frontend URL
```bash
FRONTEND_URL=https://digitalbc.sword-academy.net
```

### 4. CORS & Allowed Hosts
```bash
CORS_ORIGINS=https://digitalbc.sword-academy.net,https://api.digitalbc.sword-academy.net
ALLOWED_HOSTS=digitalbc.sword-academy.net,api.digitalbc.sword-academy.net,*.railway.app
```

### 5. Environment Settings
```bash
ENVIRONMENT=production
DEBUG=false
```

### 6. Pricing Configuration
```bash
PRO_PLAN_PRICE_USD=29.00
ENTERPRISE_PLAN_PRICE_USD=99.00
PRO_PLAN_PRICE_KWD=8.90
ENTERPRISE_PLAN_PRICE_KWD=30.50
DEFAULT_CURRENCY=USD
```

### 7. Subscription Settings
```bash
DEFAULT_TRIAL_DAYS=3
FREE_PLAN_EMPLOYEE_LIMIT=2
PRO_PLAN_EMPLOYEE_LIMIT=50
ENTERPRISE_PLAN_EMPLOYEE_LIMIT=999999
```

---

## Notes:

1. **DATABASE_URL** - Auto-injected by Railway PostgreSQL plugin ✅
2. **SECRET_KEY** - Already generated above (use it as-is)
3. **Stripe Keys** - Start with TEST keys, switch to LIVE later
4. After adding these variables, Railway will automatically redeploy

---

## Quick Add (Copy-Paste Ready)

For quick setup, copy this entire block and add each line as a separate variable:

```env
SECRET_KEY=f4B67kq4lNKcpgpJHVcmrqXQvUAJ0okkAryA7lFVunqcTVGjiCLw+W8W0NUxKdg1m0Vdl9ClSQNJ6QgpXbv/SQ==
FRONTEND_URL=https://digitalbc.sword-academy.net
CORS_ORIGINS=https://digitalbc.sword-academy.net,https://api.digitalbc.sword-academy.net
ALLOWED_HOSTS=digitalbc.sword-academy.net,api.digitalbc.sword-academy.net,*.railway.app
ENVIRONMENT=production
DEBUG=false
PRO_PLAN_PRICE_USD=29.00
ENTERPRISE_PLAN_PRICE_USD=99.00
PRO_PLAN_PRICE_KWD=8.90
ENTERPRISE_PLAN_PRICE_KWD=30.50
DEFAULT_CURRENCY=USD
DEFAULT_TRIAL_DAYS=3
FREE_PLAN_EMPLOYEE_LIMIT=2
PRO_PLAN_EMPLOYEE_LIMIT=50
ENTERPRISE_PLAN_EMPLOYEE_LIMIT=999999
```

**Add Stripe keys later when ready to test payments.**
