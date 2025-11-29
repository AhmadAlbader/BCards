# 🚀 Quick Start - Subscription System

## ⚡ للبدء السريع (5 دقائق)

### 1. تنصيب Dependencies

```bash
# Backend
cd backend && poetry add stripe

# Frontend
cd frontend && npm install @stripe/stripe-js @stripe/react-stripe-js @heroicons/react
```

### 2. إعداد Stripe (Test Mode)

1. سجل في Stripe: https://dashboard.stripe.com
2. احصل على Test Keys من: Developers → API Keys
3. أضف في `.env`:

```bash
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_key
STRIPE_WEBHOOK_SECRET=whsec_test_secret  # من Stripe CLI
```

### 3. تشغيل Migration

```bash
python migrate_subscriptions.py
```

### 4. إنشاء Stripe Products

في Stripe Dashboard → Products:

**Professional Plan:**
- USD Monthly: $29 → احفظ `price_id`
- USD Yearly: $290 → احفظ `price_id`
- KWD Monthly: 8.90 KD → احفظ `price_id`
- KWD Yearly: 89 KD → احفظ `price_id`

**Enterprise Plan:**
- USD Monthly: $99 → احفظ `price_id`
- USD Yearly: $990 → احفظ `price_id`
- KWD Monthly: 30.50 KD → احفظ `price_id`
- KWD Yearly: 305 KD → احفظ `price_id`

حدّث Price IDs في: `backend/subscription_config.py`

### 5. تشغيل الموقع

```bash
# Terminal 1 - Backend
cd backend && poetry run uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev

# Terminal 3 - Stripe Webhooks (optional)
stripe listen --forward-to localhost:8000/api/webhooks/stripe
```

### 6. اختبار

1. افتح: http://localhost:3000/pricing
2. اختر خطة واشترك
3. استخدم بطاقة Test: `4242 4242 4242 4242`
4. تحقق من Dashboard

---

## 📝 الملفات المهمة

| ملف | وصف |
|-----|-----|
| `backend/subscription_config.py` | **الأسعار والحدود** - عدّل هنا |
| `backend/stripe_service.py` | Stripe API integration |
| `backend/subscription_service.py` | Business logic |
| `backend/routes.py` | API endpoints (lines 600+) |
| `migrate_subscriptions.py` | Database migration |
| `PRICING_CHANGE_GUIDE.md` | كيف تغير الأسعار |

---

## 🎯 Features الرئيسية

✅ **3 Plans:**
- Free: 2 employees
- Professional: $29/mo (50 employees)
- Enterprise: $99/mo (unlimited)

✅ **3-day trial** على الخطط المدفوعة

✅ **Multi-currency:** USD + KWD

✅ **Payment methods:**
- Credit Cards (Visa, Mastercard, Amex)
- PayPal (via Stripe)
- Bank Transfer

✅ **Frontend pages:**
- `/pricing` - عرض الأسعار
- `/company-admin/checkout` - الدفع
- `/company-admin/subscription` - إدارة الاشتراك
- `/company-admin/billing` - الفواتير

✅ **Automatic enforcement:**
- Employee limits checked before adding
- Free subscription created on signup

---

## 🔌 API Endpoints

```
GET  /api/subscriptions/plans         - Get all pricing plans
GET  /api/subscriptions/current       - Get active subscription
POST /api/subscriptions/create-checkout  - Create Stripe checkout
POST /api/subscriptions/cancel        - Cancel subscription
POST /api/subscriptions/portal        - Open customer portal
GET  /api/subscriptions/invoices      - List invoices
POST /api/webhooks/stripe            - Handle Stripe events
```

---

## 🧪 Test Cards

```
✅ Success:      4242 4242 4242 4242
❌ Decline:      4000 0000 0000 0002
🔐 3D Secure:    4000 0027 6000 3184
💸 No Funds:     4000 0000 0000 9995
```

---

## 🐛 Quick Troubleshooting

**Webhook لا يعمل:**
```bash
stripe listen --forward-to localhost:8000/api/webhooks/stripe
# Copy the signing secret to .env
```

**أسعار لا تظهر:**
- تحقق من Price IDs في `subscription_config.py`
- تحقق من Stripe Products
- أعد تشغيل Backend

**Employee limit لا يعمل:**
- تحقق من Migration: `SELECT * FROM subscriptions;`
- تحقق من API: `/api/subscriptions/current`

**Frontend error:**
- تحقق من `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` في `.env.local`
- افتح Console للأخطاء
- أعد تشغيل Frontend

---

## 📚 Docs الكاملة

للتفاصيل الكاملة: [`SUBSCRIPTION_SETUP_GUIDE.md`](./SUBSCRIPTION_SETUP_GUIDE.md)

لتغيير الأسعار: [`PRICING_CHANGE_GUIDE.md`](./PRICING_CHANGE_GUIDE.md)

---

## ✅ Ready?

```bash
# 1. Install
poetry add stripe && cd ../frontend && npm install @stripe/stripe-js @stripe/react-stripe-js @heroicons/react

# 2. Configure .env (add Stripe keys)

# 3. Migrate
python migrate_subscriptions.py

# 4. Update Price IDs in subscription_config.py

# 5. Run!
docker-compose up
```

🎉 **Done!** افتح: http://localhost:3000/pricing

---

**وقت الإعداد:** ~5 دقائق  
**الحالة:** ✅ جاهز للاستخدام
