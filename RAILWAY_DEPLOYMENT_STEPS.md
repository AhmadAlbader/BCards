# 🚀 خطوات النشر السريعة على Railway

## ✅ قبل النشر - Checklist

تأكد من:

- [ ] جميع الاختبارات تعمل محلياً
- [ ] Migration تم تشغيله بنجاح
- [ ] Stripe Products تم إنشاؤها
- [ ] Price IDs محدّثة في الكود
- [ ] `.env` محدّث بـ Keys صحيحة
- [ ] Frontend يعمل بدون أخطاء
- [ ] Backend API يعمل بنجاح

---

## 📝 خطوة 1: تجهيز Railway

### 1.1 تنصيب Railway CLI

```bash
npm install -g @railway/cli
```

### 1.2 تسجيل الدخول

```bash
railway login
```

سيفتح متصفح للمصادقة.

### 1.3 إنشاء مشروع جديد

```bash
cd BCards
railway init
```

اختر:
- Create new project
- اسم المشروع: `bcards-production`

---

## 📝 خطوة 2: إنشاء Services

### 2.1 إنشاء PostgreSQL Database

في Railway Dashboard:

1. اضغط **New** → **Database** → **PostgreSQL**
2. انتظر حتى ينتهي الإنشاء
3. انسخ **DATABASE_URL** من Variables tab

### 2.2 Deploy Backend

```bash
# من مجلد المشروع
railway up

# اختر backend service
```

### 2.3 Deploy Frontend

```bash
# من نفس المجلد
railway up

# اختر frontend service  
```

---

## 📝 خطوة 3: إعداد Environment Variables

### 3.1 Backend Variables

في Railway Dashboard → Backend Service → Variables:

```bash
# Database
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Security
SECRET_KEY=your_secure_production_key_min_32_chars
ENVIRONMENT=production

# Stripe (LIVE KEYS!)
STRIPE_SECRET_KEY=sk_live_your_live_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_live_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_production_webhook_secret

# Frontend URL (سيتم تحديثه لاحقاً)
FRONTEND_URL=${{frontend.RAILWAY_PUBLIC_DOMAIN}}

# Subscription Config
FREE_PLAN_EMPLOYEE_LIMIT=2
DEFAULT_TRIAL_DAYS=3
SUPPORTED_CURRENCIES=USD,KWD

# CORS
CORS_ORIGINS=http://localhost:3000,${{frontend.RAILWAY_PUBLIC_DOMAIN}}
```

### 3.2 Frontend Variables

في Railway Dashboard → Frontend Service → Variables:

```bash
# Backend API
NEXT_PUBLIC_API_URL=${{backend.RAILWAY_PUBLIC_DOMAIN}}

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_your_live_publishable_key

# Environment
NODE_ENV=production
```

---

## 📝 خطوة 4: تشغيل Migration على Production

### من Terminal:

```bash
# Connect to Railway project
railway link

# Run migration
railway run -s backend python migrate_subscriptions.py
```

**أو** استخدم Railway Shell:

1. اذهب لـ Backend Service → Settings
2. افتح **Shell**
3. شغّل:
   ```bash
   python migrate_subscriptions.py
   ```

---

## 📝 خطوة 5: تحديث Stripe Webhook

### 5.1 احصل على URL النهائي

من Railway Dashboard → Backend Service:
```
https://your-backend-production-url.railway.app
```

### 5.2 حدّث Webhook في Stripe

1. اذهب لـ: https://dashboard.stripe.com/webhooks
2. اضغط **Add endpoint**
3. Endpoint URL:
   ```
   https://your-backend-production-url.railway.app/api/webhooks/stripe
   ```
4. اختر Events:
   - ✅ `checkout.session.completed`
   - ✅ `invoice.paid`
   - ✅ `invoice.payment_failed`
   - ✅ `customer.subscription.updated`
   - ✅ `customer.subscription.deleted`
5. احفظ **Signing Secret**: `whsec_...`

### 5.3 حدّث Webhook Secret في Railway

في Backend Variables:
```bash
STRIPE_WEBHOOK_SECRET=whsec_new_production_secret
```

---

## 📝 خطوة 6: اختبار Production

### 6.1 افتح الموقع

```
https://your-frontend-url.railway.app
```

### 6.2 اختبار التسجيل

1. اذهب لـ `/auth/signup`
2. سجّل شركة جديدة
3. تحقق من إنشاء Free subscription

### 6.3 اختبار Pricing

1. اذهب لـ `/pricing`
2. تحقق من عرض الأسعار
3. اختر Professional Plan

### 6.4 اختبار Checkout

⚠️ **استخدم LIVE Mode في Stripe!**

1. اختر خطة مدفوعة
2. ادخل بطاقة حقيقية
3. أكمل الدفع
4. تحقق من:
   - Redirect للـ Dashboard
   - Subscription status = "trialing" أو "active"
   - Webhook وصل في Stripe Dashboard → Events

### 6.5 اختبار Webhooks

راقب Events في Stripe Dashboard:
- `checkout.session.completed` ✅
- `invoice.paid` ✅

إذا لم يصل webhook:
1. تحقق من URL
2. تحقق من Signing Secret
3. راجع Backend Logs في Railway

---

## 📝 خطوة 7: Custom Domain (اختياري)

### 7.1 في Railway

1. اذهب لـ Frontend Service → Settings
2. اضغط **Generate Domain** (مجاني)
3. أو أضف Custom Domain:
   - Domain: `www.bcards.com`
   - يعطيك CNAME record

### 7.2 في DNS Provider

أضف CNAME record:
```
Type: CNAME
Name: www
Value: your-app.railway.app
```

### 7.3 حدّث Variables

في Backend:
```bash
FRONTEND_URL=https://www.bcards.com
CORS_ORIGINS=https://www.bcards.com
```

في Frontend:
```bash
NEXT_PUBLIC_API_URL=https://api.bcards.com
```

---

## 📝 خطوة 8: Monitoring & Logs

### 8.1 مراقبة Logs

```bash
# Backend logs
railway logs -s backend

# Frontend logs
railway logs -s frontend

# Follow live
railway logs -s backend --follow
```

### 8.2 في Railway Dashboard

- Metrics: CPU, Memory, Network
- Deployments: History
- Settings: Restart, Scale

---

## 📝 خطوة 9: Post-Deployment

### 9.1 تحديث Documentation

في Stripe Dashboard:
1. Webhook URL ✅
2. Live Mode enabled ✅
3. Customer Portal settings ✅

### 9.2 Backup Database

```bash
# من Railway
railway run -s postgres pg_dump > backup.sql

# أو استخدم Railway Backups (Paid plan)
```

### 9.3 Test Everything

- [ ] Signup flow
- [ ] Login
- [ ] Create employees (check limits)
- [ ] View public cards
- [ ] Subscribe to paid plan (LIVE payment)
- [ ] Check invoices
- [ ] Cancel subscription
- [ ] Upgrade/Downgrade

---

## 🐛 Troubleshooting

### مشكلة: Backend لا يشتغل

```bash
# Check logs
railway logs -s backend

# Check variables
railway variables -s backend

# Restart
railway service restart backend
```

### مشكلة: Database connection error

تأكد من:
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

### مشكلة: Webhook لا يصل

1. تحقق من URL في Stripe Dashboard
2. تحقق من Signing Secret
3. تحقق من Backend logs:
   ```bash
   railway logs -s backend | grep webhook
   ```

### مشكلة: CORS error

حدّث في Backend Variables:
```bash
CORS_ORIGINS=https://your-frontend.railway.app
```

### مشكلة: Frontend build fails

```bash
# Check frontend logs
railway logs -s frontend

# Common issues:
# - Missing env variables
# - TypeScript errors
# - Build timeout (increase in Settings)
```

---

## ✅ Deployment Complete!

إذا كل شيء يعمل:

🎉 **مبروك! موقعك الآن Live**

- Frontend: https://your-app.railway.app
- Backend: https://your-backend.railway.app
- API Docs: https://your-backend.railway.app/docs

---

## 📊 التكلفة المتوقعة على Railway

**Hobby Plan:**
- $5/month (flat rate)
- كافية لـ:
  - 1 Backend service
  - 1 Frontend service  
  - 1 PostgreSQL database
  - 500GB network
  - 512MB RAM per service

**إذا احتجت أكثر:**
- Pro Plan: $20/month
- Unlimited services
- Priority support

---

## 🔄 تحديثات مستقبلية

```bash
# Pull latest code
git pull origin main

# Deploy updates
railway up

# Monitor deployment
railway status
```

---

## 📞 مساعدة

إذا واجهت مشكلة:

1. راجع Logs: `railway logs -s backend`
2. تحقق من Variables
3. راجع Stripe Events
4. اتصل بـ Railway Support (في Dashboard)

---

**التكلفة الإجمالية:** $5/month (Railway Hobby)

**وقت النشر:** ~15 دقيقة

**الحالة:** ✅ جاهز للإنتاج
