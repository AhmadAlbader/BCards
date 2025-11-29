# 📚 BCards - دليل الوثائق الشامل

## مرحباً بك في BCards! 👋

هذا الدليل يساعدك على التنقل بين جميع وثائق المشروع.

---

## 🚀 للبدء السريع

### 1. Setup محلي (5 دقائق)
📄 **[QUICK_START_SUBSCRIPTIONS.md](./QUICK_START_SUBSCRIPTIONS.md)**
- تنصيب Dependencies
- إعداد Stripe Test Mode
- تشغيل الموقع محلياً
- اختبار سريع

### 2. Script تلقائي
```bash
./setup-local.sh
```
يقوم بكل شيء تلقائياً!

---

## 📖 الوثائق الرئيسية

### 🔷 Stripe Integration

#### 1. **[STRIPE_SETUP_WALKTHROUGH.md](./STRIPE_SETUP_WALKTHROUGH.md)**
📍 **متى تستخدمه:** أول مرة تعمل مع Stripe
- إنشاء حساب Stripe
- الحصول على API Keys
- إنشاء Products & Prices
- إعداد Webhooks
- Test cards
- التحويل لـ Live Mode

#### 2. **[SUBSCRIPTION_SETUP_GUIDE.md](./SUBSCRIPTION_SETUP_GUIDE.md)**
📍 **متى تستخدمه:** لإعداد نظام الاشتراكات بالكامل
- التنصيب الكامل خطوة بخطوة
- تفاصيل Migration
- إعداد Railway
- Webhooks setup
- اختبارات شاملة
- Troubleshooting

---

### 💰 إدارة الأسعار

#### **[PRICING_CHANGE_GUIDE.md](./PRICING_CHANGE_GUIDE.md)**
📍 **متى تستخدمه:** لتغيير/تحديث الأسعار
- كيفية تغيير الأسعار
- تحديث Price IDs
- إضافة عملة جديدة
- إضافة خطة جديدة
- تخصيص الميزات
- أمثلة عملية

**مثال:**
```python
# في subscription_config.py
PLAN_PRICES_USD = {
    PLAN_PROFESSIONAL: {
        "monthly": 39.00,  # كان 29.00
        "yearly": 390.00,  # كان 290.00
    },
}
```

---

### 🚢 النشر (Deployment)

#### **[RAILWAY_DEPLOYMENT_STEPS.md](./RAILWAY_DEPLOYMENT_STEPS.md)**
📍 **متى تستخدمه:** للنشر على Railway
- خطوات النشر التفصيلية
- إعداد Services (Backend, Frontend, Database)
- Environment Variables
- Custom Domain
- Monitoring & Logs
- Troubleshooting

**التكلفة:** $5/month (Railway Hobby)

---

### 📊 المشروع

#### 1. **[README_UPDATED.md](./README_UPDATED.md)**
📍 **متى تستخدمه:** نظرة عامة على المشروع
- Features
- Tech Stack
- Pricing Plans
- API Endpoints
- Quick Start
- Project Structure

#### 2. **[SUBSCRIPTION_SYSTEM_COMPLETION_REPORT.md](./SUBSCRIPTION_SYSTEM_COMPLETION_REPORT.md)**
📍 **متى تستخدمه:** تقرير مفصل عما تم إنجازه
- ملخص الإنجاز
- الإحصائيات
- الميزات المنجزة
- ملفات جديدة/محدّثة
- User Flow
- نموذج الأعمال
- KPIs

---

## 🗂 حسب الاستخدام

### إذا كنت مطوّر جديد:

1. **ابدأ هنا:** [QUICK_START_SUBSCRIPTIONS.md](./QUICK_START_SUBSCRIPTIONS.md)
2. **افهم Stripe:** [STRIPE_SETUP_WALKTHROUGH.md](./STRIPE_SETUP_WALKTHROUGH.md)
3. **شغّل محلياً:**
   ```bash
   ./setup-local.sh
   ```
4. **راجع الكود:** [README_UPDATED.md](./README_UPDATED.md)

### إذا كنت Business Owner:

1. **نظرة عامة:** [README_UPDATED.md](./README_UPDATED.md) - Pricing section
2. **التقرير:** [SUBSCRIPTION_SYSTEM_COMPLETION_REPORT.md](./SUBSCRIPTION_SYSTEM_COMPLETION_REPORT.md)
3. **تغيير الأسعار:** [PRICING_CHANGE_GUIDE.md](./PRICING_CHANGE_GUIDE.md)

### إذا كنت DevOps:

1. **النشر:** [RAILWAY_DEPLOYMENT_STEPS.md](./RAILWAY_DEPLOYMENT_STEPS.md)
2. **الإعداد الكامل:** [SUBSCRIPTION_SETUP_GUIDE.md](./SUBSCRIPTION_SETUP_GUIDE.md)
3. **Environment Variables:** جميع الملفات أعلاه

---

## 📁 هيكل الوثائق

```
docs/
├── QUICK_START_SUBSCRIPTIONS.md       ⚡ بدء سريع (5 دقائق)
├── STRIPE_SETUP_WALKTHROUGH.md        🔷 إعداد Stripe خطوة بخطوة
├── SUBSCRIPTION_SETUP_GUIDE.md        📖 دليل التنصيب الكامل
├── PRICING_CHANGE_GUIDE.md            💰 كيف تغير الأسعار
├── RAILWAY_DEPLOYMENT_STEPS.md        🚢 النشر على Railway
├── README_UPDATED.md                  📄 نظرة عامة على المشروع
├── SUBSCRIPTION_SYSTEM_COMPLETION_REPORT.md  📊 تقرير الإنجاز
└── DOCUMENTATION_INDEX.md             📚 هذا الملف
```

---

## 🎯 سيناريوهات شائعة

### 1. "أريد تشغيل الموقع محلياً"

```bash
# الطريقة السريعة
./setup-local.sh

# الطريقة اليدوية
# اقرأ: QUICK_START_SUBSCRIPTIONS.md
```

### 2. "أريد تغيير سعر Professional من $29 إلى $39"

📖 اقرأ: [PRICING_CHANGE_GUIDE.md](./PRICING_CHANGE_GUIDE.md) - "تغيير الأسعار"

الخطوات:
1. غيّر في `subscription_config.py`
2. أنشئ Price جديد في Stripe
3. حدّث Price ID في الكود

### 3. "أريد إضافة عملة جديدة (SAR مثلاً)"

📖 اقرأ: [PRICING_CHANGE_GUIDE.md](./PRICING_CHANGE_GUIDE.md) - "إضافة عملة جديدة"

### 4. "أريد النشر على الإنتاج"

📖 اقرأ بالترتيب:
1. [SUBSCRIPTION_SETUP_GUIDE.md](./SUBSCRIPTION_SETUP_GUIDE.md) - Phase 6
2. [RAILWAY_DEPLOYMENT_STEPS.md](./RAILWAY_DEPLOYMENT_STEPS.md)

### 5. "Webhook لا يعمل"

🔧 Troubleshooting في:
- [STRIPE_SETUP_WALKTHROUGH.md](./STRIPE_SETUP_WALKTHROUGH.md) - Troubleshooting
- [SUBSCRIPTION_SETUP_GUIDE.md](./SUBSCRIPTION_SETUP_GUIDE.md) - Troubleshooting

### 6. "أريد إضافة خطة رابعة (Starter)"

📖 اقرأ: [PRICING_CHANGE_GUIDE.md](./PRICING_CHANGE_GUIDE.md) - "إضافة خطة جديدة"

---

## 🔍 بحث سريع

| الموضوع | الملف | القسم |
|---------|-------|-------|
| Test Cards | STRIPE_SETUP_WALKTHROUGH.md | Test Mode |
| Price IDs | PRICING_CHANGE_GUIDE.md | تحديث Price IDs |
| Migration | SUBSCRIPTION_SETUP_GUIDE.md | Phase 4 |
| Webhooks | STRIPE_SETUP_WALKTHROUGH.md | إعداد Webhooks |
| Deployment | RAILWAY_DEPLOYMENT_STEPS.md | جميع الخطوات |
| Environment Variables | SUBSCRIPTION_SETUP_GUIDE.md | Phase 3 |
| API Endpoints | README_UPDATED.md | API Endpoints |
| Database Schema | SUBSCRIPTION_SYSTEM_COMPLETION_REPORT.md | Database Schema |
| Employee Limits | PRICING_CHANGE_GUIDE.md | تغيير حدود الخطط |
| Currencies | PRICING_CHANGE_GUIDE.md | إضافة عملة جديدة |

---

## 📞 الدعم

إذا لم تجد ما تبحث عنه:

1. **تحقق من Troubleshooting** في كل ملف
2. **راجع Backend logs:**
   ```bash
   docker-compose logs backend
   ```
3. **راجع Stripe Dashboard:** Events tab
4. **راجع هذا الملف** مرة أخرى للتأكد

---

## ✅ Checklists السريعة

### Local Setup ✅
- [ ] Docker installed
- [ ] Dependencies installed
- [ ] `.env` configured
- [ ] Stripe Test Keys
- [ ] Migration run
- [ ] Site running

### Production Deployment ✅
- [ ] Railway account
- [ ] Services created
- [ ] Env variables set
- [ ] Migration run
- [ ] Stripe Live Keys
- [ ] Webhooks configured
- [ ] Domain setup (optional)
- [ ] Tested payment

### Stripe Setup ✅
- [ ] Account created
- [ ] API Keys
- [ ] Products created
- [ ] Price IDs updated
- [ ] Webhooks setup
- [ ] Test payment successful

---

## 📈 خريطة الطريق

### تم إنجازه ✅
- Core subscription system
- Stripe integration
- 3 pricing plans
- Multi-currency (USD, KWD)
- Employee limits enforcement
- Frontend pages (4 pages)
- Documentation (7 files)

### قيد التطوير 🔄
- Email notifications
- Analytics dashboard
- Automated tests

### مخطط للمستقبل 📅
- Mobile app
- Referral program
- Custom domains for Enterprise
- Advanced analytics
- API access

---

## 🎓 موارد إضافية

### External Links:
- [Stripe Documentation](https://stripe.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [Railway Docs](https://docs.railway.app/)

### Internal Code:
- `backend/subscription_config.py` - الأسعار والخطط
- `backend/stripe_service.py` - Stripe API
- `backend/subscription_service.py` - Business logic
- `migrate_subscriptions.py` - Database migration

---

## 🗺 Navigation Map

```
Start Here
    ↓
QUICK_START_SUBSCRIPTIONS.md (5 min)
    ↓
STRIPE_SETUP_WALKTHROUGH.md (15 min)
    ↓
SUBSCRIPTION_SETUP_GUIDE.md (full setup)
    ↓
RAILWAY_DEPLOYMENT_STEPS.md (deployment)
    ↓
PRICING_CHANGE_GUIDE.md (maintenance)
```

---

## 💡 Tips

1. **ابدأ بالـ Quick Start** - لا تقفز مباشرة للتفاصيل
2. **اختبر في Test Mode أولاً** - قبل Live Mode
3. **اقرأ Troubleshooting** - يوفر عليك وقت كثير
4. **احفظ Price IDs** - ستحتاجها كثيراً
5. **راقب Stripe Events** - لفهم ما يحدث

---

**آخر تحديث:** نوفمبر 2025  
**الإصدار:** v1.0.0  
**الحالة:** ✅ شامل وجاهز

🎉 **Happy Building!**
