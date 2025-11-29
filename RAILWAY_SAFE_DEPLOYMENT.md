# 🚀 Railway Deployment - دليل النشر الآمن

## ⚠️ ملاحظة مهمة جداً

**لديك مشاريع أخرى نشطة على Railway!**

هذا الدليل يضمن:
- ✅ إنشاء مشروع **جديد منفصل** تماماً
- ✅ **لن يؤثر** على المشاريع الأخرى
- ✅ كل مشروع له **Environment Variables** خاصة به
- ✅ كل مشروع له **Database** خاص به
- ✅ كل مشروع له **Domains** خاصة به

---

## 📋 طريقة النشر الآمنة

### الخيار 1: عبر Railway Dashboard (موصى به ⭐)

#### لماذا هذه الطريقة أفضل؟
- ✅ تحكم بصري كامل
- ✅ ترى جميع المشاريع
- ✅ لا خطر من تعديل مشروع خطأ
- ✅ سهل التراجع

#### الخطوات:

**1. افتح Railway Dashboard:**
```
https://railway.app/dashboard
```

**2. إنشاء Project جديد:**
- انقر **"New Project"**
- اختر **"Deploy from GitHub repo"**
- اختر: **AhmadAlbader/BCards**
- سمّه: **BCards SaaS** (أو أي اسم واضح)

**3. إضافة PostgreSQL:**
- في نفس المشروع، انقر **"+ New"**
- اختر **"Database"** → **"PostgreSQL"**
- Railway سيضيف DATABASE_URL تلقائياً

**4. إنشاء Backend Service:**
- انقر **"+ New"** → **"GitHub Repo"**
- اختر: **AhmadAlbader/BCards**
- Service Name: `bcards-backend`

**5. إعدادات Backend:**
- انقر على Service → **Settings**
- **Root Directory:** `/backend` ⚠️ مهم!
- **Build Command:** سيستخدم Dockerfile تلقائياً
- **Deploy Trigger:** اتركه Auto-deploy

**6. إضافة Environment Variables للـ Backend:**

انقر **Variables** → **RAW Editor** → الصق:

```bash
# Security
SECRET_KEY=<GENERATE_NEW_64_CHARS>

# Stripe (ابدأ بـ Test Mode)
STRIPE_SECRET_KEY=sk_test_YOUR_KEY
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY
STRIPE_WEBHOOK_SECRET=whsec_test_YOUR_SECRET

# URLs
FRONTEND_URL=https://digitalbc.sword-academy.net
CORS_ORIGINS=https://digitalbc.sword-academy.net
ALLOWED_HOSTS=digitalbc.sword-academy.net,api.digitalbc.sword-academy.net

# Config
ENVIRONMENT=production
DEBUG=false
DEFAULT_TRIAL_DAYS=3
FREE_PLAN_EMPLOYEE_LIMIT=2
PRO_PLAN_EMPLOYEE_LIMIT=50
ENTERPRISE_PLAN_EMPLOYEE_LIMIT=999999
PRO_PLAN_PRICE_USD=29.00
ENTERPRISE_PLAN_PRICE_USD=99.00
PRO_PLAN_PRICE_KWD=8.90
ENTERPRISE_PLAN_PRICE_KWD=30.50
DEFAULT_CURRENCY=USD
SUPPORTED_CURRENCIES=USD,KWD
```

**توليد SECRET_KEY:**
```bash
openssl rand -base64 64
```

**7. إنشاء Frontend Service:**
- في نفس المشروع، انقر **"+ New"** → **"GitHub Repo"**
- اختر نفس الـ repo: **AhmadAlbader/BCards**
- Service Name: `bcards-frontend`

**8. إعدادات Frontend:**
- انقر على Service → **Settings**
- **Root Directory:** `/frontend` ⚠️ مهم!
- **Build Command:** سيستخدم Dockerfile تلقائياً

**9. إضافة Environment Variables للـ Frontend:**

```bash
NEXT_PUBLIC_API_URL=https://api.digitalbc.sword-academy.net
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY
NODE_ENV=production
```

**10. انتظر Deploy:**
- Railway سينشر تلقائياً
- تابع في **Deployments** tab
- انتظر ✅ "Success"

---

### الخيار 2: عبر Railway CLI (متقدم)

⚠️ **تحذير:** استخدم هذا فقط إذا كنت متأكد!

```bash
# 1. تأكد من المجلد الصحيح
cd /Users/ahmadalbader/Projects/BCards/BCards

# 2. إنشاء مشروع جديد (لن يؤثر على الموجود)
railway init

# سيسألك:
# - اختر "Create a new Project"
# - اسم المشروع: "BCards SaaS"

# 3. ربط بـ GitHub
railway link

# 4. إضافة PostgreSQL
railway add --service postgresql

# 5. Deploy
railway up

# 6. إضافة Variables (بعد Deploy)
railway variables set SECRET_KEY="..." STRIPE_SECRET_KEY="..." ...
```

---

## ✅ ضمانات السلامة

### 1. عزل المشاريع:
```
Railway Dashboard:
├── مشروع 1 (موجود مسبقاً)
│   ├── Services
│   ├── Database
│   └── Variables
│
├── مشروع 2 (موجود مسبقاً)
│   ├── Services
│   └── Variables
│
└── BCards SaaS (جديد - منفصل تماماً) ← هذا
    ├── bcards-backend
    ├── bcards-frontend
    ├── PostgreSQL
    └── Variables (خاصة به فقط)
```

### 2. لا مشاركة في:
- ❌ Environment Variables
- ❌ Databases
- ❌ Domains
- ❌ Deployments
- ❌ Logs

### 3. كل مشروع مستقل:
- ✅ له Git repo خاص (يمكن نفس الـ repo، فروع مختلفة)
- ✅ له Build settings خاصة
- ✅ له Deployment history خاص
- ✅ له Billing خاص

---

## 🔍 التحقق من عدم المساس بالمشاريع الأخرى

### قبل النشر:
```bash
# شاهد المشاريع الحالية
railway list

# تأكد أنك في مشروع جديد
railway status
```

### أثناء النشر:
- ✅ تأكد أن اسم المشروع جديد
- ✅ تأكد أن Database جديد
- ✅ لا تستخدم Variables من مشروع آخر

### بعد النشر:
```bash
# تحقق من المشاريع
railway list

# يجب أن ترى:
# - مشاريعك القديمة (لم تتغير)
# - BCards SaaS (جديد)
```

---

## 🎯 الخطوات بعد النشر

### 1. إضافة Custom Domains:

**Backend:**
```
Railway Dashboard → BCards SaaS → bcards-backend → Settings → Domains
Add: api.digitalbc.sword-academy.net
```

**Frontend:**
```
Railway Dashboard → BCards SaaS → bcards-frontend → Settings → Domains
Add: digitalbc.sword-academy.net
```

### 2. نسخ CNAME Targets:
Railway سيعطيك targets مثل:
```
Backend:  xyz123.railway.app
Frontend: abc456.railway.app
```

احفظها للخطوة التالية!

### 3. إعداد DNS في Hostinger:

افتح: `HOSTINGER_DNS_GUIDE.md`

### 4. إعداد Stripe Webhook:

افتح: `STRIPE_WEBHOOK_SETUP.md`

---

## 📊 مراقبة النشر

### في Railway Dashboard:

**Backend Service:**
```
BCards SaaS → bcards-backend → Logs
```

ابحث عن:
- ✅ "Database initialized successfully"
- ✅ "Application startup complete"
- ❌ أي errors

**Frontend Service:**
```
BCards SaaS → bcards-frontend → Logs
```

ابحث عن:
- ✅ "Server listening on port 3000"
- ✅ "Compiled successfully"
- ❌ أي errors

---

## 🚨 إذا حدث خطأ

### مشكلة: تأثر مشروع آخر

**مستحيل!** لكن إذا حدث:

1. Railway Dashboard → المشروع المتأثر
2. Settings → Redeploy
3. كل شي سيرجع

### مشكلة: Deploy فشل

1. تحقق من Logs
2. تحقق من Root Directory صحيح
3. تحقق من Dockerfile موجود
4. تحقق من Environment Variables

### مشكلة: Database connection failed

1. تأكد PostgreSQL service موجود
2. تأكد DATABASE_URL موجود في Variables (auto-injected)
3. انتظر 2-3 دقائق للـ retry logic

---

## 💰 التكلفة

### هذا المشروع الجديد:
```
Backend Service:   $5/month (Hobby Plan)
Frontend Service:  $5/month (Hobby Plan)
PostgreSQL:        Included
Total:            $10/month
```

### مشاريعك الأخرى:
- ✅ **لن تتغير** تكلفتها
- ✅ ستبقى كما هي

---

## ✅ Checklist - قبل البدء

- [ ] لديك Stripe Account
- [ ] لديك Test Keys جاهزة
- [ ] فتحت Railway Dashboard
- [ ] تأكدت من عدم وجود مشروع بنفس الاسم
- [ ] جاهز لإضافة Environment Variables
- [ ] قرأت هذا الدليل كاملاً

---

## 🎉 ابدأ الآن

**الطريقة الموصى بها:**

1. افتح: https://railway.app/dashboard
2. انقر: **"New Project"**
3. اختر: **"Deploy from GitHub repo"**
4. اتبع الخطوات أعلاه ☝️

---

**ضمان 100%: لن يتأثر أي مشروع موجود!** ✅

**وقت النشر:** 20-30 دقيقة (بدون DNS)
