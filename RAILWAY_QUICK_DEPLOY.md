# 🚀 Railway Deployment Guide - Quick Start

## 📋 Pre-Deployment Checklist

### ✅ Code Ready:
- [x] Backend code complete
- [x] Frontend code complete
- [x] Dockerfiles optimized for production
- [x] Health checks configured
- [x] Railway configuration files ready

---

## 🎯 Deployment Steps

### 1️⃣ Create Railway Account

1. Go to: https://railway.app
2. Sign up with GitHub (recommended)
3. Verify email

---

### 2️⃣ Create New Project

1. Click **"New Project"**
2. Select **"Empty Project"**
3. Name it: `bcards-saas`

---

### 3️⃣ Add PostgreSQL Database

1. Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway will auto-provision database
3. Note: `DATABASE_URL` will be auto-injected

---

### 4️⃣ Deploy Backend Service

#### A. Add Service:
```
+ New → GitHub Repo → Select: AhmadAlbader/BCards
```

#### B. Configure Backend:
```
Service Name: bcards-backend
Root Directory: /backend
Build: Docker (uses backend/Dockerfile)
```

#### C. Add Environment Variables:

Click **Variables** → **Raw Editor** → Paste:

```bash
# Security
SECRET_KEY=<GENERATE_NEW_64_CHAR_KEY>

# Stripe (Test Mode first)
STRIPE_SECRET_KEY=sk_test_YOUR_TEST_KEY
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_TEST_KEY
STRIPE_WEBHOOK_SECRET=whsec_test_YOUR_WEBHOOK_SECRET

# Subscription Config
DEFAULT_TRIAL_DAYS=3
FREE_PLAN_EMPLOYEE_LIMIT=2
PRO_PLAN_EMPLOYEE_LIMIT=50
ENTERPRISE_PLAN_EMPLOYEE_LIMIT=999999

# Pricing (USD)
PRO_PLAN_PRICE_USD=29.00
ENTERPRISE_PLAN_PRICE_USD=99.00

# Pricing (KWD)
PRO_PLAN_PRICE_KWD=8.90
ENTERPRISE_PLAN_PRICE_KWD=30.50

# Currency
DEFAULT_CURRENCY=USD
SUPPORTED_CURRENCIES=USD,KWD

# Frontend (will update after frontend deploy)
FRONTEND_URL=https://digitalbc.sword-academy.net
CORS_ORIGINS=https://digitalbc.sword-academy.net
ALLOWED_HOSTS=digitalbc.sword-academy.net,api.digitalbc.sword-academy.net

# Environment
ENVIRONMENT=production
DEBUG=false
```

**Generate SECRET_KEY:**
```bash
openssl rand -base64 64
```

#### D. Deploy:
Railway will auto-deploy. Wait ~5 minutes.

---

### 5️⃣ Add Custom Domain to Backend

1. Go to Backend Service → **Settings** → **Domains**
2. Click **"+ Custom Domain"**
3. Enter: `api.digitalbc.sword-academy.net`
4. Copy the **CNAME target** (e.g., `railway.app`)

**Note:** Keep this for DNS setup!

---

### 6️⃣ Deploy Frontend Service

#### A. Add Service:
```
+ New → GitHub Repo → Same repo: AhmadAlbader/BCards
```

#### B. Configure Frontend:
```
Service Name: bcards-frontend
Root Directory: /frontend
Build: Docker (uses frontend/Dockerfile)
```

#### C. Add Environment Variables:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://api.digitalbc.sword-academy.net

# Stripe (same as backend)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_TEST_KEY

# Environment
NODE_ENV=production
```

#### D. Deploy:
Railway will auto-deploy. Wait ~5 minutes.

---

### 7️⃣ Add Custom Domain to Frontend

1. Go to Frontend Service → **Settings** → **Domains**
2. Click **"+ Custom Domain"**
3. Enter: `digitalbc.sword-academy.net`
4. Copy the **CNAME target**

---

### 8️⃣ Configure DNS in Hostinger

1. Login: https://hpanel.hostinger.com
2. Go to: **Domains** → **sword-academy.net** → **DNS / Name Servers**
3. Click **"Manage"**

#### Add CNAME Records:

**Record 1 (Frontend):**
```
Type: CNAME
Name: digitalbc
Target: <Railway-Frontend-CNAME-Target>
TTL: 14400
```

**Record 2 (Backend API):**
```
Type: CNAME
Name: api.digitalbc
Target: <Railway-Backend-CNAME-Target>
TTL: 14400
```

4. Click **"Add Record"** for each
5. Wait 10-60 minutes for DNS propagation

---

### 9️⃣ Verify DNS Propagation

```bash
# Check Frontend
nslookup digitalbc.sword-academy.net

# Check Backend
nslookup api.digitalbc.sword-academy.net

# Or use online tool
# https://dnschecker.org
```

**Expected:** Should show Railway IP addresses

---

### 🔟 Verify SSL Certificates

After DNS propagates, Railway will auto-issue SSL:

```bash
# Check Frontend
curl -I https://digitalbc.sword-academy.net

# Check Backend API
curl https://api.digitalbc.sword-academy.net/api/health
```

**Expected:** Status 200 OK

---

### 1️⃣1️⃣ Configure Stripe Webhook

1. Go to: https://dashboard.stripe.com/webhooks
2. Click **"+ Add endpoint"**
3. **Endpoint URL:**
```
https://api.digitalbc.sword-academy.net/api/webhooks/stripe
```

4. **Events to send:** Select:
   - ✅ checkout.session.completed
   - ✅ customer.subscription.*
   - ✅ invoice.*
   - ✅ payment_intent.*

5. Click **"Add endpoint"**
6. Copy **Signing secret** (starts with `whsec_`)
7. Add to Railway Backend Variables:
```bash
STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET
```

8. Backend will auto-redeploy

---

### 1️⃣2️⃣ Test Webhook

From Stripe Dashboard:
1. Go to webhook you created
2. Click **"Send test webhook"**
3. Select: `checkout.session.completed`
4. Click **"Send test webhook"**

**Expected:** ✅ 200 OK

---

## 🧪 Testing Checklist

### Frontend:
- [ ] https://digitalbc.sword-academy.net loads
- [ ] Signup works
- [ ] Login works
- [ ] Dashboard loads
- [ ] Pricing page shows plans

### Backend:
- [ ] https://api.digitalbc.sword-academy.net/docs loads
- [ ] Health check: `curl https://api.digitalbc.sword-academy.net/api/health`
- [ ] Company endpoints work
- [ ] Employee endpoints work

### Subscription Flow:
- [ ] Can access pricing page
- [ ] Can click "Subscribe"
- [ ] Redirects to Stripe checkout
- [ ] After test payment, redirects back
- [ ] Subscription shows "Active" in dashboard
- [ ] Webhook received (check Railway logs)

---

## 📊 Monitor Deployment

### Railway Logs:

**Backend:**
```
Project → bcards-backend → Logs
```

**Frontend:**
```
Project → bcards-frontend → Logs
```

**Look for:**
- ✅ "Database initialized successfully"
- ✅ "Application startup complete"
- ✅ "Webhook received"
- ❌ Any errors or warnings

---

## 🔧 Troubleshooting

### Issue: Backend won't start

**Check:**
1. Railway Logs for errors
2. DATABASE_URL is set (auto-injected)
3. All required env variables present
4. Dockerfile builds successfully

**Fix:**
```bash
# Manually trigger redeploy
Settings → Redeploy
```

---

### Issue: Frontend won't connect to Backend

**Check:**
1. NEXT_PUBLIC_API_URL is correct
2. CORS_ORIGINS includes frontend domain
3. Backend is running
4. DNS propagated

**Fix:**
```bash
# Update Backend env
CORS_ORIGINS=https://digitalbc.sword-academy.net

# Update Frontend env
NEXT_PUBLIC_API_URL=https://api.digitalbc.sword-academy.net
```

---

### Issue: SSL Certificate not working

**Reason:** DNS not propagated yet

**Wait:** 10-60 minutes, then check:
```bash
curl -I https://digitalbc.sword-academy.net
```

---

### Issue: Webhook returns 401

**Reason:** STRIPE_WEBHOOK_SECRET incorrect or missing

**Fix:**
1. Get correct secret from Stripe Dashboard
2. Update in Railway Backend variables
3. Wait for redeploy

---

## 💰 Railway Pricing

### Hobby Plan: $5/month per user
- Includes: 512MB RAM, 1 vCPU per service
- PostgreSQL: Included
- Custom domains: Included
- SSL: Free
- Uptime: 99.9%

### Estimated Monthly Cost:
```
Backend Service:   $5
Frontend Service:  $5
PostgreSQL:        Included
Total:            $10/month
```

---

## 🎉 Deployment Complete!

### Your URLs:
- **Frontend:** https://digitalbc.sword-academy.net
- **Backend:** https://api.digitalbc.sword-academy.net
- **API Docs:** https://api.digitalbc.sword-academy.net/docs

### Next Steps:
1. Test complete signup/payment flow
2. Monitor logs for errors
3. Set up Stripe Live Mode (when ready)
4. Add monitoring/alerts
5. Configure backups

---

## 📚 Additional Resources

- Railway Docs: https://docs.railway.app
- Stripe Webhooks: https://stripe.com/docs/webhooks
- DNS Checker: https://dnschecker.org

---

**Created:** 2025-11-29  
**Status:** Ready to Deploy 🚀
