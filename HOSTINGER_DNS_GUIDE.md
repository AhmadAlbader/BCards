# 🔧 دليل إعداد DNS في Hostinger - خطوة بخطوة

## 📋 نظرة عامة

سنقوم بإضافة DNS Records لربط Custom Domain مع Railway:

```
digitalbc.sword-academy.net → Frontend
api.digitalbc.sword-academy.net → Backend
```

---

## 🚀 الخطوات بالصور والتفصيل

### الخطوة 1: تسجيل الدخول

1. اذهب إلى: **https://hpanel.hostinger.com**
2. أدخل Email & Password
3. اضغط **Log In**

---

### الخطوة 2: الوصول لإدارة الـ Domain

1. في Dashboard الرئيسي، اذهب لـ **Domains**
2. ستجد قائمة بجميع الـ domains
3. ابحث عن: **sword-academy.net**
4. اضغط على **Manage**

---

### الخطوة 3: فتح DNS Management

1. في صفحة Domain، ستجد tabs متعددة
2. اضغط على **DNS / Name Servers**
3. ثم اضغط **Manage DNS Records** أو **DNS Zone**

**ملاحظة:** قد تجد الزر باسم:
- "DNS Zone Editor"
- "Manage DNS"
- "Advanced DNS"

---

### الخطوة 4: إضافة Frontend DNS Record

#### A. اضغط زر **Add New Record** أو **Add DNS Record**

#### B. املأ البيانات:

```
Type: CNAME
Name: digitalbc
Target/Value: [انتظر - سيأتي من Railway]
TTL: 3600 (أو اتركه Auto/Default)
```

#### C. **لا تضغط Save بعد!** - انتظر Railway أولاً

---

### الخطوة 5: إضافة Backend API DNS Record

#### A. اضغط **Add New Record** مرة أخرى

#### B. املأ البيانات:

```
Type: CNAME
Name: api.digitalbc
Target/Value: [انتظر - سيأتي من Railway]
TTL: 3600 (أو اتركه Auto/Default)
```

#### C. **لا تضغط Save بعد!** - انتظر Railway

---

### الخطوة 6: الحصول على CNAME من Railway

الآن اذهب لـ Railway واتبع:

#### A. Frontend Service:

1. Railway Dashboard → **Frontend Service**
2. اذهب لـ **Settings** → **Networking**
3. في قسم **Public Networking**:
   - اضغط **Generate Domain** (إذا لم يكن موجود)
   - احفظ الـ domain (مثل: `frontend-production-abc123.up.railway.app`)
4. اضغط **Custom Domain**
5. أدخل: `digitalbc.sword-academy.net`
6. اضغط **Add**

**Railway سيعرض لك:**
```
CNAME Target: frontend-production-abc123.up.railway.app
```

#### B. انسخ هذا الـ Target

---

### الخطوة 7: تحديث Frontend DNS في Hostinger

1. ارجع لـ **Hostinger DNS Management**
2. في Record الأول (digitalbc):
   ```
   Type: CNAME
   Name: digitalbc
   Target: frontend-production-abc123.up.railway.app
   TTL: 3600
   ```
3. اضغط **Save** أو **Add Record**

---

### الخطوة 8: Backend Service في Railway

كرر نفس الخطوات:

1. Railway Dashboard → **Backend Service**
2. Settings → Networking → Custom Domain
3. أدخل: `api.digitalbc.sword-academy.net`
4. احفظ CNAME Target (مثل: `backend-production-xyz789.up.railway.app`)

---

### الخطوة 9: تحديث Backend DNS في Hostinger

1. في Hostinger DNS Management
2. في Record الثاني (api.digitalbc):
   ```
   Type: CNAME
   Name: api.digitalbc
   Target: backend-production-xyz789.up.railway.app
   TTL: 3600
   ```
3. اضغط **Save**

---

### الخطوة 10: التحقق من DNS Records

في Hostinger، يجب أن ترى الآن:

```
Name                          Type    Target
------------------------------------------------------
digitalbc                     CNAME   frontend-production-abc123.up.railway.app
api.digitalbc                 CNAME   backend-production-xyz789.up.railway.app
```

✅ ممتاز! DNS تم إعداده

---

## ⏳ انتظار DNS Propagation

### ما هو DNS Propagation؟

عملية نشر التغييرات عبر جميع DNS servers في العالم.

### كم يأخذ؟

- **عادة:** 5-30 دقيقة
- **أحياناً:** حتى 48 ساعة (نادر)
- **لدى Hostinger:** عادة 10-60 دقيقة

### كيف تتحقق؟

#### الطريقة 1: DNS Checker Online

1. اذهب إلى: **https://dnschecker.org**
2. أدخل: `digitalbc.sword-academy.net`
3. اختر Type: **CNAME**
4. اضغط **Search**

**يجب أن ترى:** ✅ علامات خضراء في معظم المواقع

#### الطريقة 2: Terminal Command

```bash
# macOS/Linux
dig digitalbc.sword-academy.net

# Windows
nslookup digitalbc.sword-academy.net
```

#### الطريقة 3: Ping

```bash
ping digitalbc.sword-academy.net
```

إذا رجع IP address أو CNAME، معناها DNS يعمل! ✅

---

## 🔒 SSL Certificate من Railway

### بعد DNS Propagation:

1. Railway **تلقائياً** سيصدر SSL certificate
2. يأخذ **5-15 دقيقة**
3. ستشوف 🔒 أخضر في المتصفح

### كيف تتحقق؟

1. افتح: `https://digitalbc.sword-academy.net`
2. اضغط على 🔒 في address bar
3. اقرأ Certificate details

يجب أن ترى:
```
Issued to: digitalbc.sword-academy.net
Issued by: Let's Encrypt (via Railway)
Valid: ✅
```

---

## 🐛 مشاكل شائعة

### مشكلة 1: "This site can't be reached"

**السبب:** DNS لم ينتشر بعد

**الحل:**
1. انتظر 30 دقيقة إضافية
2. تحقق من DNS Records في Hostinger (صح؟)
3. تحقق من CNAME في dnschecker.org

---

### مشكلة 2: "Not Secure" أو "Your connection is not private"

**السبب:** SSL Certificate لم يصدر بعد

**الحل:**
1. تأكد أن DNS يعمل (الخطوة السابقة)
2. انتظر 15 دقيقة للـ SSL
3. إذا استمرت المشكلة:
   - Railway → Service → Settings → Remove custom domain
   - أضفه مرة أخرى

---

### مشكلة 3: "ERR_NAME_NOT_RESOLVED"

**السبب:** خطأ في DNS Record

**الحل:**
1. تحقق من اسم Record:
   - ✅ `digitalbc` (صح)
   - ❌ `digitalbc.sword-academy.net` (خطأ - لا تضف full domain)
2. تحقق من Type:
   - ✅ `CNAME` (صح)
   - ❌ `A` (خطأ)
3. احذف Record وأعد إنشاؤه

---

### مشكلة 4: يفتح domain لكن صفحة فارغة

**السبب:** Frontend لم يُنشر أو خطأ في deployment

**الحل:**
1. Railway → Frontend Service → Deployments
2. تحقق من آخر deployment (Success ✅؟)
3. اقرأ Logs
4. إذا فيه error، أعد Deploy

---

## ✅ Checklist DNS Setup

- [ ] سجلت دخول Hostinger
- [ ] فتحت DNS Management لـ sword-academy.net
- [ ] أضفت CNAME للـ Frontend (digitalbc)
- [ ] أضفت CNAME للـ Backend (api.digitalbc)
- [ ] حصلت على CNAME targets من Railway
- [ ] حدثت DNS Records بالـ targets
- [ ] حفظت التغييرات
- [ ] انتظرت DNS propagation (10-60 دقيقة)
- [ ] تحققت من DNS في dnschecker.org
- [ ] SSL Certificate صدر (🔒 أخضر)
- [ ] Frontend يفتح: https://digitalbc.sword-academy.net
- [ ] Backend يفتح: https://api.digitalbc.sword-academy.net/docs

---

## 📞 إذا احتجت مساعدة

### Hostinger Support:
- Live Chat: في Dashboard أسفل اليمين
- Email: support@hostinger.com
- متاح 24/7

### Railway Support:
- Discord: https://discord.gg/railway
- Help Center: https://help.railway.app

---

## 🎯 بعد DNS Setup

**التالي:** ارجع لـ `CUSTOM_DOMAIN_SETUP.md` واكمل:
- المرحلة 3: Environment Variables
- المرحلة 4: Stripe Webhook
- المرحلة 5: SSL Verification
- المرحلة 6: Testing

---

**وقت التنفيذ:** 5-10 دقائق (setup) + 10-60 دقيقة (propagation)

**الصعوبة:** ⭐⭐ متوسط

**الحالة:** ✅ جاهز للتنفيذ

🚀 **ابدأ الآن!**
