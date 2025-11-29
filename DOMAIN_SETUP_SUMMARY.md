# ✅ تم الإعداد للـ Custom Domain!

## 🎯 ما تم إنجازه:

### 1. ملفات الإعداد المحدّثة ✅
- `.env.production.example` - جاهز للـ production مع custom domain
- `.env` - محدّث مع تعليق للـ production URL
- `CUSTOM_DOMAIN_SETUP.md` - دليل التنفيذ الكامل
- `HOSTINGER_DNS_GUIDE.md` - دليل DNS خطوة بخطوة

### 2. الـ Domain Configuration ✅

```
Frontend: https://digitalbc.sword-academy.net
Backend:  https://api.digitalbc.sword-academy.net
```

---

## 📋 الخطوات التالية (بالترتيب):

### ✅ الآن (في Hostinger):

**اتبع:** `HOSTINGER_DNS_GUIDE.md`

1. سجل دخول Hostinger
2. اذهب لـ DNS Management لـ sword-academy.net
3. أضف 2 CNAME records (سيأتي الـ targets من Railway)

---

### ✅ ثم (في Railway):

**اتبع:** `CUSTOM_DOMAIN_SETUP.md` - المرحلة 2

1. أضف Custom Domain للـ Frontend
2. أضف Custom Domain للـ Backend
3. احصل على CNAME targets
4. حدّث DNS في Hostinger

---

### ✅ بعدها (Environment Variables):

**اتبع:** `CUSTOM_DOMAIN_SETUP.md` - المرحلة 3

نسخ هذه Variables في Railway:

**Backend Service:**
```bash
FRONTEND_URL=https://digitalbc.sword-academy.net
CORS_ORIGINS=https://digitalbc.sword-academy.net
ALLOWED_HOSTS=digitalbc.sword-academy.net,api.digitalbc.sword-academy.net
```

**Frontend Service:**
```bash
NEXT_PUBLIC_API_URL=https://api.digitalbc.sword-academy.net
```

---

### ✅ ثم (Stripe):

**اتبع:** `CUSTOM_DOMAIN_SETUP.md` - المرحلة 4

حدّث Webhook URL في Stripe:
```
https://api.digitalbc.sword-academy.net/api/webhooks/stripe
```

---

### ✅ أخيراً (Testing):

**اتبع:** `CUSTOM_DOMAIN_SETUP.md` - المرحلة 6

اختبر:
- Frontend: https://digitalbc.sword-academy.net
- Backend: https://api.digitalbc.sword-academy.net/docs
- Payment flow
- Webhooks

---

## 📚 الدليل الشامل

### للبدء:
📄 **[HOSTINGER_DNS_GUIDE.md](./HOSTINGER_DNS_GUIDE.md)**
- شرح مفصل بالصور لإعداد DNS

### للتنفيذ الكامل:
📄 **[CUSTOM_DOMAIN_SETUP.md](./CUSTOM_DOMAIN_SETUP.md)**
- جميع المراحل من البداية للنهاية
- Troubleshooting
- Testing checklist

---

## 🎯 الوقت المتوقع

| المرحلة | الوقت |
|---------|-------|
| DNS Setup (Hostinger) | 5 دقائق |
| Railway Configuration | 10 دقائق |
| DNS Propagation | 10-60 دقيقة |
| SSL Certificate | 5-15 دقيقة |
| Testing | 10 دقائق |
| **الإجمالي** | **40 دقيقة - 2 ساعة** |

---

## 💡 نصيحة مهمة

**لا تستعجل!**
- DNS Propagation يأخذ وقت (عادي)
- SSL Certificate يصدر تلقائياً (انتظر 15 دقيقة)
- اختبر كل مرحلة قبل الانتقال للتالية

---

## 🎉 جاهز للبدء؟

**افتح الآن:** [HOSTINGER_DNS_GUIDE.md](./HOSTINGER_DNS_GUIDE.md)

وابدأ من الخطوة 1! 🚀

---

**Domain:** digitalbc.sword-academy.net  
**الحالة:** ✅ جاهز للتنفيذ  
**التكلفة:** $5/month (Railway فقط)
