# 🎯 Digital Business Cards SaaS Platform

A **production-ready**, **multi-tenant SaaS** platform for creating beautiful digital business cards. Companies can manage their employees, generate QR codes, track analytics, and share branded digital cards.

---

## 🚀 Features

### For Companies
- ✅ Company dashboard to manage employees
- ✅ Bulk employee management
- ✅ Branding customization (colors, logo)
- ✅ Analytics dashboard (track card views, clicks, calls, WhatsApp)
- ✅ Role-based access control (Admin, Employee, SuperAdmin)

### For Employees
- ✅ Personal digital business card (branded by company)
- ✅ Edit own profile
- ✅ QR code (auto-generated)
- ✅ vCard download
- ✅ Social media links
- ✅ Direct contact buttons (Call, Email, WhatsApp)

### For Platform Owners
- ✅ SuperAdmin dashboard (manage all companies)
- ✅ Platform-wide analytics
- ✅ Subscription management (Starter, Professional, Enterprise)
- ✅ Multi-tenant isolation with row-level security
- ✅ JWT authentication

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Frontend (Next.js 14 + React + TailwindCSS)           │
│  - Public card view (/{company_slug}/{employee_slug})  │
│  - Company admin dashboard                              │
│  - Employee profile                                     │
│  - Authentication (Login/Signup)                        │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP/REST API
┌──────────────────▼──────────────────────────────────────┐
│  Backend (FastAPI + SQLAlchemy)                         │
│  - Multi-tenant API with JWT auth                       │
│  - RESTful endpoints                                    │
│  - Analytics tracking                                   │
│  - Async/await for scalability                          │
└──────────────────┬──────────────────────────────────────┘
                   │ SQL
┌──────────────────▼──────────────────────────────────────┐
│  Database (PostgreSQL)                                  │
│  - companies, employees, cards, users, analytics       │
│  - Multi-tenant schema with company_id isolation       │
│  - Row-level security ready                            │
└─────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

### Tables
- **companies**: Company profiles (name, slug, branding)
- **employees**: Company employees (full_name, job_title, contact info)
- **cards**: Digital card metadata (URL, QR code, vCard)
- **users**: Admin/employee accounts (email, password, role)
- **subscriptions**: Company subscription plans (starter, pro, enterprise)
- **analytics**: Event tracking (views, clicks, calls, downloads)

---

## 📋 Setup Instructions

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local dev)
- Node.js 18+ (for frontend local dev)
- PostgreSQL 15+ (if running without Docker)

### 🐳 Quick Start with Docker Compose

1. **Clone the repo**
   ```bash
   git clone <repo-url>
   cd Digital\ Business\ Cards
   ```

2. **Create `.env` file** (copy from `.env.example`)
   ```bash
   cp .env.example .env
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Initialize database** (run migrations)
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Database: postgres://localhost:5432/digital_cards

---

## 🛠️ Local Development

### Backend Setup

1. **Create Python virtual environment**
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate  # Windows
   ```

2. **Install dependencies**
   ```bash
   pip install poetry
   poetry install
   ```

3. **Create `.env` file**
   ```bash
   cp .env.example .env
   ```

4. **Start local PostgreSQL** (Docker)
   ```bash
   docker run -d \
     --name postgres-dev \
     -e POSTGRES_PASSWORD=password \
     -e POSTGRES_DB=digital_cards \
     -p 5432:5432 \
     postgres:15-alpine
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start backend server**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Create `.env.local`**
   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

3. **Start dev server**
   ```bash
   npm run dev
   ```

4. **Open browser**
   - http://localhost:3000

---

## 🔐 Authentication & Multi-Tenancy

### JWT Token Structure
```json
{
  "sub": "user-id",
  "company_id": "company-id",
  "role": "admin|employee|superadmin",
  "exp": 1234567890
}
```

### Row-Level Security
- Employees can only view/edit their own profile
- Admins can manage employees in their company only
- SuperAdmins have full access

### API Authentication
```bash
# Get token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@company.com", "password": "password"}'

# Use token
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/company/{company_id}/employees
```

---

## 📚 API Endpoints

### Authentication
- `POST /api/auth/signup` — Register new company
- `POST /api/auth/login` — Login

### Company Management
- `POST /api/company` — Create company (admin)
- `GET /api/company/{company_id}` — Get company details (admin)

### Employees
- `POST /api/company/{company_id}/employees` — Add employee (admin)
- `GET /api/company/{company_id}/employees` — List employees (admin)
- `GET /api/employees/{employee_id}` — Get employee (admin/employee)
- `PUT /api/employees/{employee_id}` — Update employee (admin/employee)

### Public Cards
- `GET /api/card/{company_slug}/{employee_slug}` — View public card (no auth)

### Analytics
- `POST /api/analytics/track` — Track event (no auth)
- `GET /api/analytics/company/{company_id}` — Get company analytics (admin)
- `GET /api/analytics/employee/{employee_id}` — Get employee analytics (admin/employee)

---

## 🚢 Deployment

### Deploy to Production

1. **Heroku Backend**
   ```bash
   heroku create digital-cards-api
   heroku addons:create heroku-postgresql:standard-0
   heroku config:set SECRET_KEY=your-production-key
   git push heroku main
   ```

2. **Vercel Frontend**
   ```bash
   npm install -g vercel
   cd frontend
   vercel --prod
   ```

3. **Environment Variables** (set in platform)
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=production-secret-key
   CORS_ORIGINS=https://yourdomain.com
   ```

---

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest tests/
```

### Run Frontend Tests
```bash
cd frontend
npm run test
```

---

## 📊 Example Usage

### 1. Sign Up Company
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@company.com",
    "password": "secure123",
    "full_name": "John Doe",
    "role": "admin"
  }'
```

### 2. Add Employee
```bash
curl -X POST http://localhost:8000/api/company/{company_id}/employees \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Jane Smith",
    "job_title": "Sales Manager",
    "email": "jane@company.com",
    "phone": "+1234567890",
    "whatsapp": "+1234567890",
    "bio": "Experienced sales professional"
  }'
```

### 3. View Public Card
```
http://localhost:3000/card/johns-company/jane-smith-abc123
```

### 4. Track Analytics
```bash
curl -X POST http://localhost:8000/api/analytics/track \
  -H "Content-Type: application/json" \
  -d '{
    "action": "view",
    "device": "mobile"
  }' \
  -G \
  --data-urlencode "company_slug=johns-company" \
  --data-urlencode "employee_slug=jane-smith-abc123"
```

---

## 🔄 Database Migrations

### Create New Migration
```bash
cd backend
alembic revision --autogenerate -m "add new column"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback
```bash
alembic downgrade -1
```

---

## 📝 Project Structure

```
Digital Business Cards/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Database config & connection
│   ├── database_models.py   # SQLAlchemy ORM models
│   ├── models.py            # Pydantic request/response models
│   ├── routes.py            # API endpoints
│   ├── services.py          # Business logic
│   ├── security.py          # JWT & password hashing
│   ├── pyproject.toml       # Python dependencies
│   ├── Dockerfile           # Backend container
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx           # Home page
│   │   │   ├── layout.tsx         # Root layout
│   │   │   ├── globals.css        # Global styles
│   │   │   ├── auth/
│   │   │   │   ├── signup/page.tsx
│   │   │   │   └── login/page.tsx
│   │   │   ├── company-admin/
│   │   │   │   └── dashboard/page.tsx
│   │   │   └── card/
│   │   │       └── [company_slug]/[employee_slug]/page.tsx
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── Dockerfile
│   └── .env.example
│
├── docker-compose.yml       # Orchestrate all services
├── .env.example
└── README.md
```

---

## 🤝 Contributing

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 💡 Future Enhancements

- [ ] NFC card support
- [ ] Advanced analytics (heatmaps, trends)
- [ ] Bulk CSV import/export
- [ ] Custom domain support
- [ ] API webhooks
- [ ] Mobile app (React Native)
- [ ] Payment integration (Stripe)
- [ ] Slack/Teams integration
- [ ] Email notifications

---

## 🆘 Support

For issues, bugs, or feature requests:
- Open an issue on GitHub
- Email: support@digitalcards.com
- Docs: https://docs.digitalcards.com

---

**Happy carding! 🎴✨**
