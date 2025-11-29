# 🔔 إعداد Stripe Webhook - دليل مفصل

## 📋 نظرة عامة

الـ Webhook يسمح لـ Stripe بإرسال إشعارات لنظامك عند حدوث أحداث (مثل: اكتمال الدفع، إلغاء اشتراك، فشل دفع).

---

## 🎯 متى تحتاج لتحديث Webhook؟

### ✅ عند النشر على Production:
- بعد نشر Backend على Railway
- بعد إعداد Custom Domain
- عند تفعيل Live Mode في Stripe

### ✅ عند تغيير Domain:
- من Railway default domain → Custom domain
- من Test → Production

---

## 📍 الـ Webhook URL المطلوب

```
https://api.digitalbc.sword-academy.net/api/webhooks/stripe
```

**مهم:** هذا هو رابط الـ Backend (ليس Frontend)

---

## 🛠️ خطوات التحديث في Stripe

### 1️⃣ سجل دخول Stripe Dashboard

انتقل إلى: https://dashboard.stripe.com

**اختر Mode:**
- **Test Mode** للتجريب
- **Live Mode** للـ Production الحقيقي

---

### 2️⃣ افتح Webhooks

**المسار:**
```
Developers → Webhooks
```

أو مباشرة: https://dashboard.stripe.com/webhooks

---

### 3️⃣ إنشاء Webhook جديد

انقر: **"+ Add endpoint"**

#### A. أدخل Endpoint URL:
```
https://api.digitalbc.sword-academy.net/api/webhooks/stripe
```

#### B. اختر Events:

انقر: **"Select events"**

ثم اختر هذه الأحداث:

##### ✅ Checkout Events:
- ☑️ `checkout.session.completed` - اكتمال عملية الدفع
- ☑️ `checkout.session.expired` - انتهاء صلاحية Session

##### ✅ Customer Events:
- ☑️ `customer.subscription.created` - إنشاء اشتراك
- ☑️ `customer.subscription.updated` - تحديث اشتراك
- ☑️ `customer.subscription.deleted` - إلغاء اشتراك
- ☑️ `customer.subscription.trial_will_end` - اقتراب نهاية التجربة

##### ✅ Invoice Events:
- ☑️ `invoice.payment_succeeded` - نجاح الدفع
- ☑️ `invoice.payment_failed` - فشل الدفع
- ☑️ `invoice.upcoming` - فاتورة قادمة
- ☑️ `invoice.created` - إنشاء فاتورة
- ☑️ `invoice.finalized` - اكتمال الفاتورة

##### ✅ Payment Events:
- ☑️ `payment_intent.succeeded` - نجاح النية للدفع
- ☑️ `payment_intent.payment_failed` - فشل الدفع

#### C. احفظ الـ Endpoint:
انقر: **"Add endpoint"**

---

### 4️⃣ احصل على Signing Secret

بعد إنشاء الـ Endpoint:

1. انقر على Endpoint الذي أنشأته
2. ابحث عن: **"Signing secret"**
3. انقر: **"Reveal"** أو **"Click to reveal"**
4. انسخ القيمة (تبدأ بـ `whsec_...`)

**مثال:**
```
whsec_1234567890abcdefghijklmnopqrstuvwxyz
```

---

### 5️⃣ أضف Secret في Railway

#### انتقل لـ Railway Dashboard:
```
Project → Backend Service → Variables
```

#### أضف Variable جديد:
```bash
Name:  STRIPE_WEBHOOK_SECRET
Value: whsec_1234567890abcdefghijklmnopqrstuvwxyz
```

**انقر:** "Add" أو "Save"

⚠️ **مهم:** Railway سيعيد تشغيل Service تلقائياً

---

### 6️⃣ اختبر الـ Webhook

#### من Stripe Dashboard:

1. اذهب لصفحة Webhook
2. انقر: **"Send test webhook"**
3. اختر Event مثل: `checkout.session.completed`
4. انقر: **"Send test webhook"**

#### النتيجة المتوقعة:
- ✅ Status: **200 OK**
- ✅ Response time: < 2 seconds
- ✅ Response body: `{"status": "success"}`

#### إذا فشل:
- تحقق من URL صحيح
- تحقق من STRIPE_WEBHOOK_SECRET في Railway
- تحقق من Backend Service يعمل
- تحقق من Logs في Railway

---

## 🔍 التحقق من عمل Webhook

### طريقة 1: من Stripe Dashboard

```
Developers → Webhooks → [Your Endpoint] → Recent deliveries
```

يجب أن ترى:
- ✅ Green checkmarks للنجاح
- ❌ Red X للفشل

### طريقة 2: من Railway Logs

```
Project → Backend Service → Logs
```

ابحث عن:
```
Webhook received: checkout.session.completed
Subscription created for company: ...
```

### طريقة 3: اختبار حقيقي

1. اذهب لصفحة Pricing في موقعك
2. اختر خطة
3. أكمل الدفع (test card في Test Mode)
4. تحقق من تحديث الاشتراك في Database

---

## 🔐 Security Best Practices

### ✅ احم Webhook Secret:

**لا تشارك أبداً:**
- في Git repository
- في Slack/Teams
- في screenshots
- مع أشخاص غير مصرح لهم

### ✅ استخدم Modes منفصلة:

| Mode | استخدام | Webhook Secret |
|------|---------|---------------|
| **Test** | Development & Testing | `whsec_test_...` |
| **Live** | Production Real Money | `whsec_live_...` |

### ✅ تحديث Secret دورياً:

يمكنك تدوير (Rotate) Secret كل 6-12 شهر:
1. احصل على Secret جديد من Stripe
2. حدّث في Railway
3. احذف القديم من Stripe

---

## 🛠️ Troubleshooting

### ❌ مشكلة: Webhook returns 401/403

**السبب:** STRIPE_WEBHOOK_SECRET خاطئ أو غير موجود

**الحل:**
```bash
# تحقق من Railway Variables
Railway → Backend Service → Variables → STRIPE_WEBHOOK_SECRET

# تحقق من Stripe Dashboard
Developers → Webhooks → [Endpoint] → Signing secret
```

---

### ❌ مشكلة: Webhook returns 404

**السبب:** URL خاطئ

**الحل:**
تحقق من URL في Stripe:
```
✅ صحيح: https://api.digitalbc.sword-academy.net/api/webhooks/stripe
❌ خطأ: https://digitalbc.sword-academy.net/api/webhooks/stripe (Frontend)
❌ خطأ: https://api.digitalbc.sword-academy.net/webhooks/stripe (بدون /api)
```

---

### ❌ مشكلة: Webhook returns 500

**السبب:** خطأ في Backend Code

**الحل:**
```bash
# شاهد Logs في Railway
Railway → Backend Service → Logs

# ابحث عن Python errors
```

---

### ❌ مشكلة: Webhook لا يستجيب

**السبب:** Backend Service لا يعمل أو DNS غير صحيح

**الحل:**
```bash
# 1. تحقق من Backend يعمل
curl https://api.digitalbc.sword-academy.net/docs

# 2. تحقق من DNS
nslookup api.digitalbc.sword-academy.net

# 3. تحقق من Railway Service Status
Railway → Backend Service → Deployments
```

---

## 📋 Checklist - تحقق من كل شي

قبل ما تقول "خلاص، انتهيت":

### Backend:
- [ ] Backend Service يعمل على Railway
- [ ] Custom domain `api.digitalbc.sword-academy.net` مضاف
- [ ] DNS CNAME صحيح
- [ ] SSL Certificate صادر (https:// يعمل)

### Stripe:
- [ ] Webhook endpoint مضاف في Stripe Dashboard
- [ ] URL صحيح: `https://api.digitalbc.sword-academy.net/api/webhooks/stripe`
- [ ] Events محددة (checkout, subscription, invoice)
- [ ] Signing secret منسوخ

### Railway:
- [ ] `STRIPE_WEBHOOK_SECRET` مضاف في Variables
- [ ] Backend Service أعيد تشغيله
- [ ] Logs تظهر webhook events

### Testing:
- [ ] Test webhook من Stripe Dashboard يعمل (200 OK)
- [ ] Payment flow كامل يعمل
- [ ] Subscription يتحدث في Database
- [ ] Logs تظهر events صحيحة

---

## 🎉 انتهيت؟

إذا كل الـ Checkboxes ✅، يعني:

**🎊 Stripe Webhook جاهز للعمل!**

---

## 📚 مصادر إضافية

### Stripe Documentation:
- Webhooks Overview: https://stripe.com/docs/webhooks
- Webhook Events: https://stripe.com/docs/api/events/types
- Testing Webhooks: https://stripe.com/docs/webhooks/test

### BCards Guides:
- `CUSTOM_DOMAIN_SETUP.md` - Custom domain setup
- `RAILWAY_DEPLOYMENT_STEPS.md` - Railway deployment
- `SUBSCRIPTION_SETUP_GUIDE.md` - Full subscription guide

---

**Created:** 2025-11-29  
**Domain:** api.digitalbc.sword-academy.net  
**Webhook Path:** `/api/webhooks/stripe`
