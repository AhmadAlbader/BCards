# 🎯 نظام الاشتراكات - دليل التنصيب والإعداد الكامل

## 📋 نظرة عامة

تم إضافة نظام اشتراكات كامل مع تكامل Stripe للمدفوعات. النظام يشمل:

- ✅ 3 خطط: Free (2 موظفين)، Professional ($29/mo)، Enterprise ($99/mo)
- ✅ فترة تجريبية 3 أيام
- ✅ دعم عملتين: USD و KWD
- ✅ تكامل كامل مع Stripe (بطاقات، PayPal عبر Stripe، تحويل بنكي)
- ✅ واجهات أمامية كاملة (Pricing, Checkout, Subscription Management, Billing)
- ✅ فرض حدود الموظفين تلقائياً
- ✅ إدارة الفواتير والدفعات

---

## 🚀 خطوات التنصيب

### المرحلة 1: تحديث الاعتماديات

#### Backend
```bash
cd backend
poetry add stripe
# أو
pip install stripe
```

#### Frontend
```bash
cd frontend
npm install @stripe/stripe-js @stripe/react-stripe-js @heroicons/react
# أو
yarn add @stripe/stripe-js @stripe/react-stripe-js @heroicons/react
```

---

### المرحلة 2: إعداد Stripe

#### 1. إنشاء حساب Stripe
1. اذهب إلى: https://dashboard.stripe.com/register
2. أنشئ حساب جديد أو سجل دخول

#### 2. الحصول على API Keys
```
Dashboard → Developers → API keys

Test Keys (للتطوير):
- Publishable key: pk_test_...
- Secret key: sk_test_...

Live Keys (للإنتاج):
- Publishable key: pk_live_...
- Secret key: sk_live_...
```

#### 3. إنشاء Products & Prices في Stripe Dashboard

**خطوات:**

1. اذهب إلى: **Products** → **Add Product**

2. **Professional Plan - USD Monthly:**
   - Name: `Professional Plan - USD`
   - Description: `Up to 50 employees with full features`
   - Pricing:
     - Price: `$29.00`
     - Billing: `Recurring - Monthly`
   - احفظ Price ID: `price_xxxxxxxxxxxxx`

3. **Professional Plan - USD Yearly:**
   - نفس المنتج، أضف سعر جديد:
     - Price: `$290.00`
     - Billing: `Recurring - Yearly`
   - احفظ Price ID: `price_yyyyyyyyyyyyy`

4. **Professional Plan - KWD Monthly:**
   - Name: `Professional Plan - KWD`
   - Price: `KD 8.90`
   - Billing: `Recurring - Monthly`
   - احفظ Price ID

5. **Professional Plan - KWD Yearly:**
   - Price: `KD 89.00`
   - Billing: `Recurring - Yearly`
   - احفظ Price ID

6. **كرر نفس الخطوات لـ Enterprise Plan**
   - USD Monthly: $99.00
   - USD Yearly: $990.00
   - KWD Monthly: KD 30.50
   - KWD Yearly: KD 305.00

#### 4. تحديث Price IDs في الكود

افتح: `backend/subscription_config.py`

```python
STRIPE_PRICE_IDS = {
    "USD": {
        f"{PLAN_PROFESSIONAL}_monthly": "price_1234abcd",  # ← ضع Price ID هنا
        f"{PLAN_PROFESSIONAL}_yearly": "price_5678efgh",
        f"{PLAN_ENTERPRISE}_monthly": "price_9012ijkl",
        f"{PLAN_ENTERPRISE}_yearly": "price_3456mnop",
    },
    "KWD": {
        f"{PLAN_PROFESSIONAL}_monthly": "price_qrst1234",
        f"{PLAN_PROFESSIONAL}_yearly": "price_uvwx5678",
        f"{PLAN_ENTERPRISE}_monthly": "price_yzab9012",
        f"{PLAN_ENTERPRISE}_yearly": "price_cdef3456",
    },
}
```

#### 5. إعداد Webhooks

**خطوات:**

1. اذهب إلى: **Developers** → **Webhooks** → **Add endpoint**

2. **Endpoint URL:**
   ```
   Development: http://localhost:8000/api/webhooks/stripe
   Production: https://your-domain.com/api/webhooks/stripe
   ```

3. **Select events to listen to:**
   - ✅ `checkout.session.completed`
   - ✅ `invoice.paid`
   - ✅ `invoice.payment_failed`
   - ✅ `customer.subscription.updated`
   - ✅ `customer.subscription.deleted`
   - ✅ `customer.subscription.trial_will_end`

4. **احفظ Signing Secret:**
   ```
   whsec_xxxxxxxxxxxxxxxxxxxxx
   ```

---

### المرحلة 3: تحديث ملفات البيئة

#### Development (.env)

```bash
# Stripe Keys (Test Mode)
STRIPE_SECRET_KEY=sk_test_your_test_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_test_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Subscription Configuration
FREE_PLAN_EMPLOYEE_LIMIT=2
DEFAULT_TRIAL_DAYS=3
SUPPORTED_CURRENCIES=USD,KWD

# Frontend URL for Stripe redirects
FRONTEND_URL=http://localhost:3000
```

#### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_test_publishable_key
```

#### Production (.env.production)

راجع ملف: `.env.production.example` للتفاصيل الكاملة

---

### المرحلة 4: تشغيل Migration

```bash
# من مجلد المشروع الرئيسي
python migrate_subscriptions.py

# إذا أردت التراجع (احذر!)
python migrate_subscriptions.py --rollback
```

**ما يفعله Migration:**
- يضيف أعمدة جديدة لجدول `subscriptions`
- ينشئ جدول `invoices`
- ينشئ جدول `payment_methods`
- يضيف indexes للأداء
- يضيف triggers لـ `updated_at`

---

### المرحلة 5: اختبار محلي

#### 1. تشغيل Backend & Frontend

```bash
# Terminal 1 - Backend
cd backend
poetry run uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

#### 2. اختبار Webhooks محلياً

```bash
# تنصيب Stripe CLI
brew install stripe/stripe-cli/stripe

# تسجيل دخول
stripe login

# تشغيل webhook forwarding
stripe listen --forward-to localhost:8000/api/webhooks/stripe

# سيعطيك Webhook Signing Secret، ضعه في .env
# whsec_xxxxxxxxxxxxx
```

#### 3. اختبار flow الكامل

**أ. التسجيل:**
1. افتح: http://localhost:3000/auth/signup
2. سجل شركة جديدة
3. تحقق من إنشاء subscription مجاني تلقائياً

**ب. عرض الأسعار:**
1. افتح: http://localhost:3000/pricing
2. تحقق من عرض الأسعار بشكل صحيح
3. بدّل بين Monthly/Yearly
4. بدّل بين USD/KWD

**ج. Checkout:**
1. اختر Professional Plan
2. سيتم توجيهك لـ Stripe Checkout
3. استخدم بطاقة اختبار: `4242 4242 4242 4242`
   - أي CVC
   - أي تاريخ مستقبلي
4. أكمل الدفع

**د. Subscription Management:**
1. بعد Checkout، ستعود لـ Dashboard
2. اذهب إلى: Subscription Management
3. تحقق من عرض التفاصيل
4. جرب "Manage Billing" (سيفتح Stripe Customer Portal)
5. جرب "Cancel Subscription"

**هـ. Billing & Invoices:**
1. افتح: Billing & Invoices
2. تحقق من عرض الفواتير
3. جرب تحميل PDF

**و. Employee Limits:**
1. في Dashboard، حاول إضافة موظفين
2. على Free Plan، بعد 2 موظفين ستحصل على رسالة خطأ
3. بعد الترقية لـ Professional، يمكنك إضافة حتى 50

---

### المرحلة 6: النشر على Railway

#### 1. تجهيز الملفات

تأكد من وجود:
- `railway.json` ✅
- `.env.production.example` ✅
- `Dockerfile` في backend & frontend ✅

#### 2. إنشاء مشروع على Railway

```bash
# تنصيب Railway CLI
npm install -g @railway/cli

# تسجيل دخول
railway login

# ربط المشروع
railway init

# نشر
railway up
```

#### 3. إعداد Environment Variables

في Railway Dashboard:

**Backend Service:**
```
DATABASE_URL=postgresql://...
SECRET_KEY=your_production_secret
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
FRONTEND_URL=https://your-frontend.railway.app
ENVIRONMENT=production
```

**Frontend Service:**
```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
```

#### 4. تحديث Stripe Webhook URL

في Stripe Dashboard:
- اذهب لـ Webhooks
- عدّل Endpoint URL إلى: `https://your-backend.railway.app/api/webhooks/stripe`

#### 5. تشغيل Migration على Production

```bash
# من Railway CLI
railway run python migrate_subscriptions.py
```

---

## 🧪 اختبارات مهمة

### 1. Test Cards (Stripe)

```
Success: 4242 4242 4242 4242
Decline: 4000 0000 0000 0002
3D Secure: 4000 0027 6000 3184
Insufficient Funds: 4000 0000 0000 9995
```

### 2. Test Webhooks

```bash
# محلي
stripe trigger checkout.session.completed

# إرسال webhook يدوي
curl -X POST http://localhost:8000/api/webhooks/stripe \
  -H "Content-Type: application/json" \
  -H "Stripe-Signature: whsec_..." \
  -d '{"type": "checkout.session.completed", ...}'
```

### 3. Test Employee Limits

```python
# في Python shell أو Postman
# Free Plan: يجب أن يفشل بعد 2 موظفين
POST /company/{id}/employees
{
  "full_name": "Employee 3",
  ...
}

# Expected Response: 403 Forbidden
{
  "detail": "Employee limit reached for Free plan. Upgrade to add more employees."
}
```

---

## 📂 ملفات جديدة تم إنشاؤها

### Backend:
1. `backend/subscription_config.py` - إعدادات الأسعار والخطط
2. `backend/stripe_service.py` - تكامل Stripe API
3. `backend/subscription_service.py` - منطق الاشتراكات
4. `backend/models.py` - إضافة Pydantic models
5. `backend/database_models.py` - توسيع جداول Database
6. `backend/routes.py` - إضافة 10+ endpoints
7. `backend/services.py` - تحديث مع subscription checks

### Frontend:
8. `frontend/src/app/pricing/page.tsx` - صفحة الأسعار
9. `frontend/src/app/company-admin/checkout/page.tsx` - صفحة Checkout
10. `frontend/src/app/company-admin/subscription/page.tsx` - إدارة الاشتراك
11. `frontend/src/app/company-admin/billing/page.tsx` - الفواتير
12. `frontend/src/app/company-admin/dashboard/page.tsx` - تحديث بعرض الحدود

### Configuration:
13. `.env` - محدّث
14. `.env.production.example` - جديد
15. `railway.json` - جديد
16. `migrate_subscriptions.py` - جديد
17. `PRICING_CHANGE_GUIDE.md` - دليل تغيير الأسعار

---

## 🔧 API Endpoints الجديدة

```
GET    /api/subscriptions/plans              - قائمة الخطط
GET    /api/subscriptions/current            - الاشتراك الحالي
POST   /api/subscriptions/create-checkout    - إنشاء checkout session
POST   /api/subscriptions/cancel             - إلغاء اشتراك
POST   /api/subscriptions/portal             - فتح Stripe portal
GET    /api/subscriptions/invoices           - قائمة الفواتير
POST   /api/webhooks/stripe                  - Stripe webhooks handler
```

---

## ⚠️ نقاط مهمة

### 1. Security
- ✅ Webhook signature verification مفعّل
- ✅ لا تخزن أرقام بطاقات كاملة
- ✅ استخدم HTTPS في Production
- ✅ اختبر Stripe في Test Mode أولاً

### 2. Database
- ✅ شغّل Migration قبل أي شيء
- ✅ احتفظ بنسخة احتياطية قبل Migration
- ✅ تحقق من Indexes للأداء

### 3. Pricing
- ⚠️ Price IDs في Stripe immutable - لتغيير السعر، أنشئ Price جديد
- ✅ استخدم `PRICING_CHANGE_GUIDE.md` لتغيير الأسعار
- ✅ أخبر العملاء قبل أي تغيير

### 4. Testing
- ✅ اختبر كل flow محلياً أولاً
- ✅ استخدم Stripe Test Mode
- ✅ اختبر Webhooks بـ Stripe CLI
- ✅ اختبر Employee limits

---

## 🐛 Troubleshooting

### مشكلة: Webhook لا يعمل

**الحل:**
```bash
# تحقق من Signing Secret
echo $STRIPE_WEBHOOK_SECRET

# اختبر محلياً
stripe listen --forward-to localhost:8000/api/webhooks/stripe

# تحقق من logs
docker-compose logs backend | grep webhook
```

### مشكلة: Price IDs خاطئة

**الحل:**
1. اذهب لـ Stripe Dashboard → Products
2. افتح المنتج → Pricing
3. انسخ Price ID الصحيح
4. حدّث `backend/subscription_config.py`
5. أعد تشغيل Backend

### مشكلة: Employee limit لا يعمل

**الحل:**
```bash
# تحقق من Subscription
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/subscriptions/current

# تحقق من Database
docker-compose exec postgres psql -U postgres -d digital_cards
SELECT * FROM subscriptions;
```

### مشكلة: Frontend لا يعرض الأسعار

**الحل:**
1. تحقق من `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` في `.env.local`
2. تحقق من Backend API: `http://localhost:8000/api/subscriptions/plans`
3. افتح Console في المتصفح للأخطاء
4. أعد تشغيل Frontend: `npm run dev`

---

## 📞 الدعم

إذا واجهت مشكلة:

1. راجع هذا الدليل
2. راجع `PRICING_CHANGE_GUIDE.md` لتغيير الأسعار
3. تحقق من Logs:
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```
4. راجع Stripe Dashboard → Events
5. اختبر بـ Postman أو cURL

---

## ✅ Checklist قبل Production

- [ ] جميع Price IDs محدّثة في `subscription_config.py`
- [ ] Stripe Live Keys موضوعة في `.env.production`
- [ ] Webhook URL محدّث في Stripe Dashboard
- [ ] Migration تم تشغيله على Production
- [ ] Frontend env variables محدّثة
- [ ] HTTPS مفعّل
- [ ] Database backup جاهز
- [ ] Testing كامل تم
- [ ] Customer Portal مفعّل في Stripe
- [ ] Email notifications جاهزة (optional)

---

**آخر تحديث:** نوفمبر 2025
**الإصدار:** 1.0.0
**الحالة:** ✅ جاهز للإنتاج
