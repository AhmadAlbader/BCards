# 💰 دليل تغيير أسعار الاشتراكات

## 📋 نظرة عامة

الأسعار الحالية:
- **Free Plan**: مجاني (2 موظفين)
- **Professional**: $29/month أو KD 8.90/month
- **Enterprise**: $99/month أو KD 30.50/month

---

## 🔧 كيفية تغيير الأسعار

### الطريقة 1: تعديل ملف الإعدادات (الأسهل)

افتح ملف: `backend/subscription_config.py`

```python
# Pricing (USD)
PLAN_PRICES_USD = {
    PLAN_FREE: {
        "monthly": 0,
        "yearly": 0,
    },
    PLAN_PROFESSIONAL: {
        "monthly": 29.00,      # ← غير هنا
        "yearly": 290.00,      # ← غير هنا (12 شهر - خصم 17%)
    },
    PLAN_ENTERPRISE: {
        "monthly": 99.00,      # ← غير هنا
        "yearly": 990.00,      # ← غير هنا
    },
}

# Pricing (KWD - Kuwaiti Dinar)
PLAN_PRICES_KWD = {
    PLAN_FREE: {
        "monthly": 0,
        "yearly": 0,
    },
    PLAN_PROFESSIONAL: {
        "monthly": 8.90,       # ← غير هنا
        "yearly": 89.00,       # ← غير هنا
    },
    PLAN_ENTERPRISE: {
        "monthly": 30.50,      # ← غير هنا
        "yearly": 305.00,      # ← غير هنا
    },
}
```

**✅ احفظ الملف وأعد تشغيل Backend**

---

### الطريقة 2: تغيير الأسعار في Stripe Dashboard

#### ⚠️ مهم جداً: تحديث Stripe

بعد تغيير الأسعار في ملف الإعدادات، يجب تحديث Stripe:

**الخطوات:**

1. **اذهب إلى Stripe Dashboard**
   ```
   https://dashboard.stripe.com/products
   ```

2. **أنشئ منتج جديد أو عدل الموجود**
   - Product Name: Professional Plan
   - Price: $29 (أو السعر الجديد)
   - Billing: Recurring monthly

3. **احصل على Price ID الجديد**
   ```
   مثال: price_1234abcd5678efgh
   ```

4. **حدث ملف `subscription_config.py`**
   ```python
   STRIPE_PRICE_IDS = {
       "USD": {
           f"{PLAN_PROFESSIONAL}_monthly": "price_NEW_ID_HERE",
           # ... الباقي
       }
   }
   ```

---

## 🔄 تغيير حدود الخطط

في نفس الملف `subscription_config.py`:

```python
# Plan Limits
PLAN_LIMITS = {
    PLAN_FREE: {
        "employees": 2,              # ← عدد الموظفين
        "analytics_days": 30,        # ← أيام التحليلات
        "custom_logo": False,        # ← شعار مخصص
        "api_access": False,         # ← وصول API
        # ... الباقي
    },
    PLAN_PROFESSIONAL: {
        "employees": 50,             # ← غير هنا
        "analytics_days": 365,
        "custom_logo": True,
        # ...
    },
    # ...
}
```

---

## 🎁 تغيير فترة التجربة المجانية

في ملف `.env`:

```bash
DEFAULT_TRIAL_DAYS=3    # ← غير هنا (الأيام)
```

أو في `subscription_config.py`:

```python
TRIAL_DAYS = 3  # ← غير هنا
```

---

## 💱 إضافة عملة جديدة

### 1. أضف الأسعار في `subscription_config.py`:

```python
# Pricing (SAR - Saudi Riyal)
PLAN_PRICES_SAR = {
    PLAN_FREE: {
        "monthly": 0,
        "yearly": 0,
    },
    PLAN_PROFESSIONAL: {
        "monthly": 109.00,
        "yearly": 1090.00,
    },
    PLAN_ENTERPRISE: {
        "monthly": 375.00,
        "yearly": 3750.00,
    },
}

# أضف Stripe Price IDs
STRIPE_PRICE_IDS = {
    "USD": {...},
    "KWD": {...},
    "SAR": {  # ← جديد
        f"{PLAN_PROFESSIONAL}_monthly": "price_sar_pro_monthly",
        f"{PLAN_PROFESSIONAL}_yearly": "price_sar_pro_yearly",
        f"{PLAN_ENTERPRISE}_monthly": "price_sar_ent_monthly",
        f"{PLAN_ENTERPRISE}_yearly": "price_sar_ent_yearly",
    },
}

# أضف رمز العملة
CURRENCY_SYMBOLS = {
    "USD": "$",
    "KWD": "KD",
    "SAR": "﷼",  # ← جديد
}

# أضف اسم العملة
CURRENCY_NAMES = {
    "USD": "US Dollar",
    "KWD": "Kuwaiti Dinar",
    "SAR": "Saudi Riyal",  # ← جديد
}
```

### 2. حدث القائمة المدعومة:

```python
SUPPORTED_CURRENCIES = ["USD", "KWD", "SAR"]  # ← أضف هنا
```

### 3. حدث `.env`:

```bash
SUPPORTED_CURRENCIES=USD,KWD,SAR
```

---

## 🎨 تخصيص ميزات الخطط

في `subscription_config.py`:

```python
PLAN_FEATURES = {
    PLAN_FREE: [
        "Up to 2 employees",
        "Basic branding (color only)",
        "Basic analytics (30 days)",
        "QR codes & vCards",
        "Email support",
    ],
    PLAN_PROFESSIONAL: [
        "Up to 50 employees",           # ← عدل هنا
        "Full branding (color + logo)",
        "Advanced analytics",
        "Priority support",             # ← أضف ميزة جديدة
        # أضف المزيد...
    ],
}
```

---

## 📊 أمثلة على التغييرات الشائعة

### مثال 1: زيادة السعر 10%

```python
# قبل
PLAN_PRICES_USD = {
    PLAN_PROFESSIONAL: {
        "monthly": 29.00,
        "yearly": 290.00,
    },
}

# بعد
PLAN_PRICES_USD = {
    PLAN_PROFESSIONAL: {
        "monthly": 31.90,   # 29 + 10%
        "yearly": 319.00,   # 290 + 10%
    },
}
```

### مثال 2: زيادة حد الموظفين

```python
# قبل
PLAN_LIMITS = {
    PLAN_FREE: {
        "employees": 2,
    },
}

# بعد
PLAN_LIMITS = {
    PLAN_FREE: {
        "employees": 5,  # زيادة من 2 إلى 5
    },
}
```

### مثال 3: إضافة خطة جديدة

```python
# أضف في subscription_config.py

# 1. أضف اسم الخطة
PLAN_STARTER = "starter"

# 2. أضف السعر
PLAN_PRICES_USD = {
    # ... الخطط الموجودة
    PLAN_STARTER: {
        "monthly": 15.00,
        "yearly": 150.00,
    },
}

# 3. أضف الحدود
PLAN_LIMITS = {
    # ... الخطط الموجودة
    PLAN_STARTER: {
        "employees": 10,
        "analytics_days": 90,
        "custom_logo": False,
    },
}

# 4. أضف الميزات
PLAN_FEATURES = {
    # ... الخطط الموجودة
    PLAN_STARTER: [
        "Up to 10 employees",
        "Basic branding",
        "90 days analytics",
    ],
}
```

---

## ⚠️ تحذيرات مهمة

### 1. تغيير أسعار المشتركين الحاليين
```
❌ لا تغير الأسعار مباشرة في Stripe للمشتركين الحاليين
✅ أنشئ أسعار جديدة وأعط المشتركين القدامى خيار الترقية
```

### 2. Stripe Price IDs
```
⚠️ Price IDs في Stripe ثابتة (immutable)
✅ إذا غيرت السعر، يجب إنشاء Price ID جديد
```

### 3. اختبار التغييرات
```
✅ اختبر دائماً في Development أولاً
✅ استخدم Stripe Test Mode
✅ تأكد من التحديثات في Frontend أيضاً
```

---

## 🧪 الاختبار بعد التغيير

### 1. اختبار محلي
```bash
# أعد تشغيل Backend
docker-compose restart backend

# تحقق من API
curl http://localhost:8000/api/subscriptions/plans

# يجب أن ترى الأسعار الجديدة
```

### 2. اختبار في Frontend
```
افتح: http://localhost:3000/pricing
تأكد من ظهور الأسعار الجديدة
```

### 3. اختبار الدفع
```
استخدم Stripe Test Cards:
- 4242 4242 4242 4242 (Success)
- 4000 0000 0000 0002 (Decline)
```

---

## 📱 تحديث Frontend

بعد تغيير الأسعار في Backend، حدث Frontend:

### ملف: `frontend/src/app/pricing/page.tsx`

```typescript
// السعر يأتي من API تلقائياً
// لكن إذا كان ثابت في الكود، غيره هنا:

const plans = [
  {
    name: "Professional",
    priceUSD: 29,  // ← غير هنا
    priceKWD: 8.90, // ← غير هنا
  }
];
```

---

## 🔄 الخطوات الكاملة لتغيير الأسعار

### ✅ Checklist

- [ ] 1. غير الأسعار في `subscription_config.py`
- [ ] 2. أنشئ أسعار جديدة في Stripe Dashboard
- [ ] 3. حدث `STRIPE_PRICE_IDS` مع IDs الجديدة
- [ ] 4. اختبر في Development
- [ ] 5. حدث `.env.production` على Railway
- [ ] 6. حدث Frontend إذا لزم الأمر
- [ ] 7. اختبر في Production
- [ ] 8. أخبر العملاء عن التغييرات

---

## 🆘 الأسئلة الشائعة

**س: هل يؤثر تغيير السعر على المشتركين الحاليين؟**
ج: لا، المشتركين الحاليين يبقون على نفس السعر حتى نهاية دورتهم.

**س: كيف أعطي خصم لعميل معين؟**
ج: استخدم Stripe Coupons أو أنشئ price custom من Stripe Dashboard.

**س: هل يمكن تغيير الحدود فقط دون الأسعار؟**
ج: نعم، غير `PLAN_LIMITS` فقط ولا تغير الأسعار.

**س: كيف أختبر الأسعار الجديدة؟**
ج: استخدم Stripe Test Mode واختبر checkout flow كاملاً.

---

## 📞 الدعم

إذا واجهت مشكلة:
1. تحقق من logs: `docker-compose logs backend`
2. تحقق من Stripe Dashboard: Events tab
3. راجع هذا الدليل مرة أخرى

---

**آخر تحديث:** نوفمبر 2025
**الإصدار:** 1.0.0
