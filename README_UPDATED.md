# 💼 BCards - Digital Business Cards SaaS Platform

<div align="center">

![BCards](https://img.shields.io/badge/BCards-SaaS%20Platform-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Stripe](https://img.shields.io/badge/Stripe-Integrated-purple)

**منصة SaaS متكاملة لإنشاء وإدارة بطاقات الأعمال الرقمية**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Pricing](#-pricing)

</div>

---

## 🎯 Overview

BCards هي منصة SaaS حديثة تتيح للشركات إنشاء وإدارة بطاقات أعمال رقمية لموظفيها. مع نظام اشتراكات متكامل ودعم متعدد الشركات (Multi-tenant).

### ✨ Key Features

#### 🏢 Multi-Tenant Architecture
- شركات متعددة مع بيانات معزولة
- إدارة مستقلة لكل شركة
- Custom branding (لوجو، ألوان، نطاق مخصص)

#### 👥 Employee Management
- CRUD كامل للموظفين
- بطاقات مخصصة لكل موظف
- روابط اجتماعية متعددة (Instagram, LinkedIn, Facebook, YouTube, Twitter, TikTok, Snapchat)
- معلومات الاتصال (هاتف، واتساب، بريد)

#### 🎨 Digital Business Cards
- تصميم احترافي responsive
- QR codes قابلة للمسح
- vCard download (إضافة للجهات)
- مشاركة مباشرة عبر واتساب
- Analytics للزيارات

#### 💳 Subscription System (NEW!)
- 3 خطط: **Free** (2 employees), **Professional** ($29/mo, 50 employees), **Enterprise** ($99/mo, unlimited)
- تكامل كامل مع **Stripe**
- فترة تجريبية **3 أيام**
- دعم عملتين: **USD** و **KWD**
- إدارة الفواتير والدفعات
- Customer Portal
- Automatic employee limit enforcement

#### 🎨 Advanced Branding
- Custom colors (primary, secondary, text, background)
- Logo upload
- Brand consistency عبر جميع البطاقات
- Preview في الوقت الفعلي

#### 📊 Analytics & Reporting
- تتبع الزيارات
- إحصائيات الموظفين
- تحليل الأداء
- Export data

---

## 🛠 Tech Stack

### Backend
- **FastAPI** 0.104+ - Modern async Python web framework
- **PostgreSQL** 15 - Relational database
- **SQLAlchemy** 2.0+ - ORM with async support
- **Pydantic** 2.0+ - Data validation
- **Stripe** 7.0+ - Payment processing
- **Docker** - Containerization

### Frontend
- **Next.js** 14 - React framework
- **TypeScript** - Type safety
- **TailwindCSS** 3.4 - Utility-first CSS
- **Stripe Elements** - Secure payment forms
- **Axios** - HTTP client
- **Zustand** - State management

### Infrastructure
- **Docker Compose** - Local development
- **Railway** - Production deployment (Hobby plan: $5/mo)
- **Nginx** - Reverse proxy (optional)

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- Stripe account (for subscriptions)

### Installation

```bash
# 1. Clone repository
git clone <repository-url>
cd BCards

# 2. Setup environment
cp .env.example .env
# Edit .env with your values

# 3. Install dependencies
cd backend && poetry install
cd ../frontend && npm install

# 4. Setup Stripe (for subscriptions)
# See SUBSCRIPTION_SETUP_GUIDE.md

# 5. Run migrations
python migrate_subscriptions.py

# 6. Start services
docker-compose up -d

# 7. Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Quick Test

```bash
# Sign up
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@company.com",
    "password": "securepass123",
    "company_name": "My Company",
    "company_slug": "my-company"
  }'

# View your card
http://localhost:3000/card/my-company/employee-name
```

---

## 📂 Project Structure

```
BCards/
├── backend/
│   ├── main.py                    # FastAPI app
│   ├── database.py                # Database config
│   ├── database_models.py         # SQLAlchemy models
│   ├── models.py                  # Pydantic schemas
│   ├── routes.py                  # API endpoints
│   ├── services.py                # Business logic
│   ├── security.py                # Authentication
│   ├── subscription_config.py     # Pricing & plans ⭐
│   ├── stripe_service.py          # Stripe integration ⭐
│   ├── subscription_service.py    # Subscription logic ⭐
│   └── vcard_utils.py             # vCard generation
├── frontend/
│   └── src/
│       └── app/
│           ├── pricing/           # Pricing page ⭐
│           ├── company-admin/
│           │   ├── checkout/      # Stripe checkout ⭐
│           │   ├── subscription/  # Manage subscription ⭐
│           │   ├── billing/       # Invoices ⭐
│           │   ├── dashboard/     # Admin panel
│           │   ├── settings/      # Company settings
│           │   └── branding/      # Brand customization
│           ├── card/              # Public card view
│           └── auth/              # Login/Signup
├── migrate_subscriptions.py       # DB migration ⭐
├── docker-compose.yml
├── railway.json                   # Railway config ⭐
├── .env                           # Environment variables
├── SUBSCRIPTION_SETUP_GUIDE.md    # Full setup guide ⭐
├── PRICING_CHANGE_GUIDE.md        # How to change prices ⭐
└── QUICK_START_SUBSCRIPTIONS.md   # Quick start ⭐

⭐ = New files for subscription system
```

---

## 💰 Pricing

### Free Plan
- **Price:** Free forever
- **Employees:** Up to 2
- **Branding:** Basic (color only)
- **Analytics:** 30 days
- **QR Codes:** ✅
- **vCard Download:** ✅
- **Support:** Email

### Professional Plan
- **Price:** $29/month or KD 8.90/month
- **Employees:** Up to 50
- **Branding:** Full (color + logo)
- **Analytics:** 365 days
- **Custom QR:** ✅
- **API Access:** ✅
- **Support:** Priority email
- **Free Trial:** 3 days

### Enterprise Plan
- **Price:** $99/month or KD 30.50/month
- **Employees:** Unlimited
- **Branding:** Custom domain + white-label
- **Analytics:** Lifetime
- **Dedicated Manager:** ✅
- **24/7 Support:** Phone + Email
- **Custom Integrations:** ✅
- **SLA:** 99.9% uptime
- **Free Trial:** 3 days

💡 **Note:** All paid plans include a 3-day free trial. No credit card required to start.

---

## 📚 Documentation

### Setup Guides
- [**SUBSCRIPTION_SETUP_GUIDE.md**](./SUBSCRIPTION_SETUP_GUIDE.md) - Complete setup with Stripe
- [**QUICK_START_SUBSCRIPTIONS.md**](./QUICK_START_SUBSCRIPTIONS.md) - Quick 5-minute setup
- [**PRICING_CHANGE_GUIDE.md**](./PRICING_CHANGE_GUIDE.md) - How to modify pricing

### Additional Docs
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
- [API_REFERENCE.md](./API_REFERENCE.md) - API documentation
- [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) - Production deployment
- [DIGITALOCEAN_DEPLOYMENT.md](./DIGITALOCEAN_DEPLOYMENT.md) - DigitalOcean guide

---

## 🔌 API Endpoints

### Authentication
```
POST /api/auth/signup              - Register company
POST /api/auth/login               - Login
```

### Companies
```
GET    /api/companies              - List companies
GET    /api/companies/{id}         - Get company
PUT    /api/companies/{id}         - Update company
DELETE /api/companies/{id}         - Delete company
```

### Employees
```
GET    /api/company/{id}/employees        - List employees
POST   /api/company/{id}/employees        - Create employee
GET    /api/employee/{id}                 - Get employee
PUT    /api/employee/{id}                 - Update employee
DELETE /api/employee/{id}                 - Delete employee
GET    /api/card/{company}/{employee}     - Get public card
```

### Subscriptions (NEW!)
```
GET    /api/subscriptions/plans           - Get pricing plans
GET    /api/subscriptions/current         - Get active subscription
POST   /api/subscriptions/create-checkout - Create Stripe checkout
POST   /api/subscriptions/cancel          - Cancel subscription
POST   /api/subscriptions/portal          - Open customer portal
GET    /api/subscriptions/invoices        - List invoices
POST   /api/webhooks/stripe              - Stripe webhook handler
```

### QR & vCard
```
GET /api/qrcode/{company}/{employee}      - Generate QR code
GET /api/vcard/{company}/{employee}       - Generate vCard
```

📖 Full API docs: `http://localhost:8000/docs`

---

## 🧪 Testing

### Test Stripe Integration

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks locally
stripe listen --forward-to localhost:8000/api/webhooks/stripe

# Test checkout flow
# Use test card: 4242 4242 4242 4242
```

### Test Cards
```
✅ Success:        4242 4242 4242 4242
❌ Decline:        4000 0000 0000 0002
🔐 3D Secure:      4000 0027 6000 3184
💸 No Funds:       4000 0000 0000 9995
```

### Run Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

---

## 🚢 Deployment

### Railway (Recommended - $5/mo)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Init project
railway init

# Deploy
railway up

# Set environment variables in Railway Dashboard
```

### Environment Variables (Production)

```bash
# Backend
DATABASE_URL=postgresql://...
SECRET_KEY=your_production_secret_key
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
FRONTEND_URL=https://your-domain.com
ENVIRONMENT=production

# Frontend
NEXT_PUBLIC_API_URL=https://api.your-domain.com
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
```

See: [DIGITALOCEAN_DEPLOYMENT.md](./DIGITALOCEAN_DEPLOYMENT.md) for detailed guide.

---

## 🔒 Security

- ✅ JWT authentication
- ✅ Password hashing (bcrypt)
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ CORS configuration
- ✅ Stripe webhook signature verification
- ✅ HTTPS in production
- ✅ Environment variables for secrets
- ✅ Rate limiting (optional)

---

## 📈 Roadmap

### Phase 1: Core Platform ✅
- [x] Multi-tenant architecture
- [x] Employee CRUD
- [x] Digital business cards
- [x] QR codes & vCards
- [x] Custom branding

### Phase 2: Subscription System ✅
- [x] Stripe integration
- [x] Multiple pricing plans
- [x] Employee limits enforcement
- [x] Invoice management
- [x] Customer portal

### Phase 3: Advanced Features (Coming Soon)
- [ ] Email notifications
- [ ] Analytics dashboard
- [ ] Custom domains
- [ ] API access for Enterprise
- [ ] Mobile app (React Native)
- [ ] Bulk employee import
- [ ] Team collaboration
- [ ] Advanced analytics

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is proprietary software. All rights reserved.

---

## 💬 Support

- 📧 Email: support@bcards.com
- 💬 Discord: [Join our community](#)
- 📚 Docs: [Full Documentation](#)
- 🐛 Issues: [GitHub Issues](#)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Amazing Python framework
- [Next.js](https://nextjs.org/) - React framework
- [Stripe](https://stripe.com/) - Payment processing
- [TailwindCSS](https://tailwindcss.com/) - CSS framework
- [Railway](https://railway.app/) - Deployment platform

---

<div align="center">

**Made with ❤️ for modern businesses**

[Website](#) • [Documentation](#) • [Twitter](#) • [LinkedIn](#)

</div>
