# 🔷 Stripe Setup - خطوة بخطوة

## 📋 ما تحتاجه

- حساب Stripe (مجاني)
- 15 دقيقة من وقتك

---

## 🚀 الخطوات

### 1️⃣ إنشاء حساب Stripe

1. اذهب إلى: https://dashboard.stripe.com/register
2. املأ البيانات:
   - Email
   - Password
   - Country (اختر بلدك)
3. أكمل التسجيل

---

### 2️⃣ الحصول على API Keys

#### Test Keys (للتطوير):

1. في Dashboard → **Developers** → **API keys**
2. اضغط على **Reveal test key**
3. انسخ:
   - **Publishable key**: `pk_test_51...`
   - **Secret key**: `sk_test_51...`

#### ضع في `.env`:

```bash
STRIPE_SECRET_KEY=sk_test_51xxxxxxxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_51xxxxxxxxxxxxx
```

#### ضع في `frontend/.env.local`:

```bash
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_51xxxxxxxxxxxxx
```

---

### 3️⃣ إنشاء Products & Prices

#### A. Professional Plan

**خطوات:**

1. Dashboard → **Products** → **Add Product**

2. **Product Information:**
   - Name: `Professional Plan - USD`
   - Description: `Up to 50 employees with full features`
   - Image: (اختياري)

3. **Pricing:**
   - Model: **Standard pricing**
   - Price: `29.00`
   - Billing period: **Monthly**
   - Currency: **USD**
   - اضغط **Save product**

4. **احفظ Price ID:**
   - بعد الحفظ، ستجد: `price_1NxxxxxxxxxxxT4V`
   - انسخه

5. **أضف Yearly Price:**
   - في نفس المنتج → **Add another price**
   - Price: `290.00`
   - Billing period: **Yearly**
   - احفظ Price ID الثاني

6. **كرر للـ KWD:**
   - أنشئ منتج جديد: `Professional Plan - KWD`
   - Monthly: `8.90 KWD`
   - Yearly: `89.00 KWD`

#### B. Enterprise Plan

كرر نفس الخطوات:

- **USD Monthly**: $99.00
- **USD Yearly**: $990.00
- **KWD Monthly**: KD 30.50
- **KWD Yearly**: KD 305.00

---

### 4️⃣ تحديث Price IDs في الكود

افتح: `backend/subscription_config.py`

ابحث عن:

```python
STRIPE_PRICE_IDS = {
    "USD": {
        f"{PLAN_PROFESSIONAL}_monthly": "price_xxxxx",  # ← هنا
        f"{PLAN_PROFESSIONAL}_yearly": "price_xxxxx",   # ← هنا
        f"{PLAN_ENTERPRISE}_monthly": "price_xxxxx",    # ← هنا
        f"{PLAN_ENTERPRISE}_yearly": "price_xxxxx",     # ← هنا
    },
    "KWD": {
        f"{PLAN_PROFESSIONAL}_monthly": "price_xxxxx",  # ← هنا
        f"{PLAN_PROFESSIONAL}_yearly": "price_xxxxx",   # ← هنا
        f"{PLAN_ENTERPRISE}_monthly": "price_xxxxx",    # ← هنا
        f"{PLAN_ENTERPRISE}_yearly": "price_xxxxx",     # ← هنا
    },
}
```

استبدل `price_xxxxx` بالـ IDs الحقيقية من Stripe.

---

### 5️⃣ إعداد Webhooks

#### A. تنصيب Stripe CLI (للتطوير المحلي)

```bash
# macOS
brew install stripe/stripe-cli/stripe

# Windows
scoop install stripe

# Linux
https://stripe.com/docs/stripe-cli
```

#### B. تسجيل الدخول

```bash
stripe login
```

سيفتح متصفح للمصادقة.

#### C. تشغيل Webhook Forwarding

```bash
stripe listen --forward-to localhost:8000/api/webhooks/stripe
```

**سيعطيك Signing Secret:**

```
> Ready! Your webhook signing secret is whsec_xxxxxxxxxxxxx
```

#### D. ضعه في `.env`:

```bash
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

---

### 6️⃣ اختبار (Test Mode)

#### Test Cards:

| Card Number | النتيجة |
|-------------|---------|
| `4242 4242 4242 4242` | ✅ نجاح |
| `4000 0000 0000 0002` | ❌ رفض |
| `4000 0027 6000 3184` | 🔐 3D Secure |
| `4000 0000 0000 9995` | 💸 رصيد غير كاف |

#### تفاصيل أخرى:
- CVC: أي 3 أرقام (مثل: 123)
- Expiry: أي تاريخ مستقبلي (مثل: 12/25)
- ZIP: أي رمز (مثل: 12345)

---

### 7️⃣ التحويل لـ Live Mode (للإنتاج)

#### A. إكمال بيانات Stripe

في Dashboard → **Settings**:

1. **Business details:**
   - Company name
   - Business address
   - Phone number

2. **Bank account:**
   - أضف حساب بنكي لاستقبال الأموال

3. **Identity verification:**
   - ارفع المستندات المطلوبة

#### B. تفعيل Live Mode

1. Dashboard → toggle من **Test** إلى **Live**
2. احصل على Live Keys:
   - `pk_live_51...`
   - `sk_live_51...`

#### C. إنشاء Webhook في Live Mode

1. Dashboard (Live Mode) → **Developers** → **Webhooks**
2. **Add endpoint**
3. **Endpoint URL:**
   ```
   https://your-production-domain.com/api/webhooks/stripe
   ```
4. **Select events:**
   - `checkout.session.completed`
   - `invoice.paid`
   - `invoice.payment_failed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `customer.subscription.trial_will_end`
5. احفظ Signing Secret

#### D. حدّث Production Env

```bash
STRIPE_SECRET_KEY=sk_live_51xxxxx
STRIPE_PUBLISHABLE_KEY=pk_live_51xxxxx
STRIPE_WEBHOOK_SECRET=whsec_live_xxxxx
```

---

## 🎯 ملخص سريع

### Development:

```bash
# 1. Stripe Keys
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# 2. Webhook (من Stripe CLI)
stripe listen --forward-to localhost:8000/api/webhooks/stripe
STRIPE_WEBHOOK_SECRET=whsec_...

# 3. Products في Stripe Dashboard
# 4. Price IDs في subscription_config.py
# 5. Test card: 4242 4242 4242 4242
```

### Production:

```bash
# 1. Complete Stripe account verification
# 2. Get Live Keys
# 3. Create Webhook endpoint
# 4. Update env variables
# 5. Test with real card (small amount)
```

---

## 🐛 Troubleshooting

### مشكلة: "Invalid API Key"

**الحل:**
- تأكد من استخدام Test keys في development
- تأكد من عدم وجود مسافات في البداية/النهاية
- تأكد من أن الـ key يبدأ بـ `sk_test_` أو `pk_test_`

### مشكلة: Webhook لا يصل

**الحل:**
```bash
# تأكد من تشغيل Stripe CLI
stripe listen --forward-to localhost:8000/api/webhooks/stripe

# في terminal آخر، اختبر:
stripe trigger checkout.session.completed
```

### مشكلة: "No such price"

**الحل:**
- تأكد من أن Price IDs صحيحة في `subscription_config.py`
- تأكد من أن Products في Test Mode (أو Live حسب البيئة)
- في Stripe Dashboard، افتح Product واحفظ Price ID مرة أخرى

### مشكلة: "Invalid currency"

**الحل:**
- تأكد من أن Currency في الطلب يطابق Currency في Stripe Product
- مثلاً: إذا Product بـ USD، لا يمكن الدفع بـ KWD

---

## ✅ Checklist

قبل أن تبدأ الاختبار:

- [ ] حساب Stripe تم إنشاؤه
- [ ] Test API Keys في `.env`
- [ ] Products تم إنشاؤها (Professional, Enterprise)
- [ ] Prices تم إنشاؤها (USD Monthly/Yearly, KWD Monthly/Yearly)
- [ ] Price IDs تم تحديثها في الكود
- [ ] Stripe CLI تم تنصيبه
- [ ] Webhook forwarding يعمل
- [ ] Backend يعمل
- [ ] Frontend يعمل
- [ ] Test payment بنجاح

---

## 📞 مساعدة

إذا واجهت مشكلة:

1. راجع [Stripe Documentation](https://stripe.com/docs)
2. راجع [Stripe Events Dashboard](https://dashboard.stripe.com/test/events)
3. تحقق من Backend logs: `docker-compose logs backend`
4. اتصل بـ Stripe Support (ممتاز!)

---

## 🎓 موارد مفيدة

- [Stripe API Reference](https://stripe.com/docs/api)
- [Stripe Testing Cards](https://stripe.com/docs/testing)
- [Stripe Webhooks Guide](https://stripe.com/docs/webhooks)
- [Stripe CLI Commands](https://stripe.com/docs/stripe-cli)

---

**الوقت المتوقع:** 15 دقيقة  
**الصعوبة:** ⭐⭐ سهل  
**الحالة:** ✅ جاهز للاستخدام
