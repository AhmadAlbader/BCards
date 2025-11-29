# 🌐 Custom Domain Setup - digitalbc.sword-academy.net

## ✅ تم الإعداد للـ Custom Domain الخاص بك!

---

## 📋 معلومات الـ Domain

```
Frontend: https://digitalbc.sword-academy.net
Backend:  https://api.digitalbc.sword-academy.net
```

---

## 🚀 خطوات التنفيذ

### المرحلة 1: إعداد DNS في Hostinger ⚙️

#### 1. تسجيل الدخول لـ Hostinger
1. اذهب إلى: https://hpanel.hostinger.com
2. سجل دخول
3. اذهب لـ **Domains** → اختر `sword-academy.net`

#### 2. إضافة DNS Records

اذهب لـ **DNS / Name Servers** → **Manage DNS Records**

أضف Record #1 (Frontend):
```
Type: CNAME
Name: digitalbc
Value: [سيتم تحديثه من Railway - انظر المرحلة 2]
TTL: 3600 (أو Auto)
```

أضف Record #2 (Backend API):
```
Type: CNAME
Name: api.digitalbc
Value: [سيتم تحديثه من Railway - انظر المرحلة 2]
TTL: 3600 (أو Auto)
```

**⏳ انتظر:** DNS propagation يأخذ 5-60 دقيقة

---

### المرحلة 2: إعداد Railway 🚂

#### A. Frontend Service

1. **Dashboard → Frontend Service → Settings → Networking**
2. اضغط **Generate Domain** (احفظ الـ domain المولد)
3. اضغط **Add Custom Domain**
4. أدخل: `digitalbc.sword-academy.net`
5. Railway سيعطيك CNAME target
6. **ارجع لـ Hostinger** وضع CNAME value للـ `digitalbc`

#### B. Backend Service

1. **Dashboard → Backend Service → Settings → Networking**
2. اضغط **Generate Domain** (احفظ الـ domain المولد)
3. اضغط **Add Custom Domain**
4. أدخل: `api.digitalbc.sword-academy.net`
5. Railway سيعطيك CNAME target
6. **ارجع لـ Hostinger** وضع CNAME value للـ `api.digitalbc`

---

### المرحلة 3: Environment Variables في Railway 🔧

#### Backend Service → Variables:

أضف/حدث:
```bash
FRONTEND_URL=https://digitalbc.sword-academy.net
CORS_ORIGINS=https://digitalbc.sword-academy.net
ALLOWED_HOSTS=digitalbc.sword-academy.net,api.digitalbc.sword-academy.net
```

#### Frontend Service → Variables:

أضف/حدث:
```bash
NEXT_PUBLIC_API_URL=https://api.digitalbc.sword-academy.net
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_your_live_key
```

**💡 Tip:** بعد التحديث، Railway سيعيد Deploy تلقائياً

---

### المرحلة 4: تحديث Stripe Webhook 🔷

#### في Stripe Dashboard:

1. اذهب لـ: https://dashboard.stripe.com/webhooks
2. اختر webhook الموجود (أو أنشئ جديد)
3. **غيّر Endpoint URL** من:
   ```
   https://bcards-backend-xxx.railway.app/api/webhooks/stripe
   ```
   إلى:
   ```
   https://api.digitalbc.sword-academy.net/api/webhooks/stripe
   ```
4. احفظ التغييرات
5. **احفظ Signing Secret الجديد** (إذا تغير)

#### حدّث في Railway Backend Variables:
```bash
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

---

### المرحلة 5: اختبار SSL Certificate 🔒

#### انتظر SSL (5-15 دقيقة):

1. افتح: https://digitalbc.sword-academy.net
2. افتح: https://api.digitalbc.sword-academy.net
3. تحقق من **القفل الأخضر** 🔒 في المتصفح

#### إذا لم يعمل SSL:
- انتظر 15 دقيقة إضافية
- تحقق من DNS propagation: https://dnschecker.org
- أدخل: `digitalbc.sword-academy.net`

---

### المرحلة 6: الاختبار الكامل ✅

#### A. Frontend Test:
1. افتح: https://digitalbc.sword-academy.net
2. يجب أن يظهر الموقع بشكل طبيعي
3. جرب التسجيل

#### B. Backend API Test:
```bash
curl https://api.digitalbc.sword-academy.net/docs
```
يجب أن ترى API documentation

#### C. CORS Test:
1. افتح Frontend
2. افتح Browser Console (F12)
3. جرب تسجيل الدخول
4. **لا يجب** أن ترى أي CORS errors

#### D. Stripe Test:
1. اذهب لـ: https://digitalbc.sword-academy.net/pricing
2. اختر Professional Plan
3. أكمل الدفع (Test Mode)
4. تحقق من Webhook في Stripe Events

---

## 📊 ملخص الـ Configuration

### DNS في Hostinger:
```
digitalbc.sword-academy.net → CNAME → [railway-frontend]
api.digitalbc.sword-academy.net → CNAME → [railway-backend]
```

### Railway Environment Variables:

**Backend:**
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=your_production_secret_key
STRIPE_SECRET_KEY=sk_live_xxxxx
STRIPE_PUBLISHABLE_KEY=pk_live_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
FRONTEND_URL=https://digitalbc.sword-academy.net
CORS_ORIGINS=https://digitalbc.sword-academy.net
ALLOWED_HOSTS=digitalbc.sword-academy.net,api.digitalbc.sword-academy.net
FREE_PLAN_EMPLOYEE_LIMIT=2
DEFAULT_TRIAL_DAYS=3
SUPPORTED_CURRENCIES=USD,KWD
ENVIRONMENT=production
```

**Frontend:**
```bash
NEXT_PUBLIC_API_URL=https://api.digitalbc.sword-academy.net
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxxxx
NODE_ENV=production
```

### Stripe:
```
Webhook URL: https://api.digitalbc.sword-academy.net/api/webhooks/stripe
Events: checkout.session.completed, invoice.paid, customer.subscription.*
```

---

## 🐛 Troubleshooting

### مشكلة: "DNS_PROBE_FINISHED_NXDOMAIN"

**الحل:**
1. تحقق من DNS Records في Hostinger
2. انتظر DNS propagation (حتى 60 دقيقة)
3. اختبر في: https://dnschecker.org

---

### مشكلة: "SSL Certificate Error"

**الحل:**
1. انتظر 15 دقيقة إضافية
2. في Railway → Service → Settings → Delete custom domain
3. أضف Domain مرة أخرى
4. Railway سيعيد إصدار certificate

---

### مشكلة: CORS Error

**الحل:**
```bash
# تحقق من Backend variables في Railway
CORS_ORIGINS=https://digitalbc.sword-academy.net

# تأكد من عدم وجود مسافات
# تأكد من https:// (مش http://)
```

---

### مشكلة: Stripe Webhook لا يصل

**الحل:**
1. تحقق من URL في Stripe Dashboard
2. يجب أن يكون: `https://api.digitalbc.sword-academy.net/api/webhooks/stripe`
3. اختبر Webhook من Stripe Dashboard → Send test webhook
4. راقب Events tab

---

### مشكلة: Backend لا يستجيب

**الحل:**
```bash
# اختبر مباشرة
curl https://api.digitalbc.sword-academy.net/docs

# إذا لم يعمل:
# 1. تحقق من DNS
# 2. تحقق من Railway Logs
# 3. تحقق من Backend deployment status
```

---

## 📞 خطوات ما بعد Setup

### 1. تحديث Documentation
- [ ] حدّث README مع الـ domain الجديد
- [ ] حدّث API documentation

### 2. Security
- [ ] تأكد من HTTPS يعمل على كل الصفحات
- [ ] تحقق من CORS settings
- [ ] اختبر جميع API endpoints

### 3. Monitoring
- [ ] راقب Railway Metrics
- [ ] راقب Stripe Events
- [ ] راقب Backend logs لأي أخطاء

### 4. Backup
- [ ] احفظ نسخة من DNS Records
- [ ] احفظ نسخة من Railway env variables
- [ ] خذ database backup

---

## ✅ Checklist النهائي

قبل الـ Launch:

- [ ] DNS Records مضافة في Hostinger
- [ ] Custom Domains مضافة في Railway
- [ ] SSL certificates تعمل (🔒 أخضر)
- [ ] Environment variables محدّثة
- [ ] Stripe webhook URL محدّث
- [ ] Frontend يفتح على: https://digitalbc.sword-academy.net
- [ ] Backend API يعمل على: https://api.digitalbc.sword-academy.net
- [ ] CORS لا يوجد به أخطاء
- [ ] Signup/Login يعمل
- [ ] Payment test نجح
- [ ] Webhook يصل من Stripe

---

## 🎯 الوقت المتوقع

- DNS Setup: 5 دقائق
- Railway Configuration: 10 دقائق
- DNS Propagation: 10-60 دقيقة
- SSL Certificate: 5-15 دقيقة
- Testing: 10 دقائق

**الإجمالي: 40 دقيقة - 2 ساعة**

---

## 💰 التكلفة

- Railway Hobby: $5/month
- Custom Domain (عندك already): $0
- SSL Certificate (من Railway): $0

**Total: $5/month فقط!** 🎉

---

## 🎓 موارد مفيدة

- [Railway Custom Domains Guide](https://docs.railway.app/deploy/custom-domains)
- [Hostinger DNS Management](https://support.hostinger.com/en/articles/1583227-how-to-manage-dns-records)
- [DNS Checker Tool](https://dnschecker.org)
- [SSL Checker](https://www.sslshopper.com/ssl-checker.html)

---

**تم التحديث:** 29 نوفمبر 2025  
**الحالة:** ✅ جاهز للتنفيذ  
**Domain:** digitalbc.sword-academy.net

🚀 **ابدأ الآن من المرحلة 1!**
