# 🏗️ System Architecture Deep Dive

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    END USERS                               │
│  (Public Cards, Company Admins, Employees, Analytics)      │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────────┐  ┌──────▼────────────────┐
│  Browser/Mobile      │  │  Mobile Browser      │
│  (React Frontend)    │  │  (Public Card View)  │
└───────┬──────────────┘  └──────┬────────────────┘
        │ HTTP/S REST API        │
        │ (Bearer Token JWT)     │
        └────────────┬───────────┘
                     │
        ┌────────────▼────────────┐
        │   API Gateway / LB      │
        │   (CORS Middleware)     │
        └────────────┬────────────┘
                     │
┌────────────────────▼─────────────────────────┐
│         FASTAPI BACKEND SERVICES             │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ Routes Layer                         │   │
│  │ - /auth (signup, login)              │   │
│  │ - /company (CRUD)                    │   │
│  │ - /employees (CRUD)                  │   │
│  │ - /card (public view)                │   │
│  │ - /analytics (tracking)              │   │
│  └──────────────────────────────────────┘   │
│                 ▲                            │
│                 │                            │
│  ┌──────────────▼──────────────────────┐   │
│  │ Services Layer                      │   │
│  │ - CompanyService                    │   │
│  │ - EmployeeService                   │   │
│  │ - CardService                       │   │
│  │ - UserService                       │   │
│  │ - AnalyticsService                  │   │
│  └──────────────────────────────────────┘   │
│                 ▲                            │
│                 │                            │
│  ┌──────────────▼──────────────────────┐   │
│  │ Security Layer                      │   │
│  │ - JWT Token Validation              │   │
│  │ - RBAC (admin, employee, superadmin)│   │
│  │ - Multi-tenant Isolation            │   │
│  │ - Password Hashing (bcrypt)         │   │
│  └──────────────────────────────────────┘   │
│                 ▲                            │
│                 │                            │
│  ┌──────────────▼──────────────────────┐   │
│  │ Database Abstraction Layer          │   │
│  │ - Pydantic Models (validation)      │   │
│  │ - SQLAlchemy ORM (async)            │   │
│  └──────────────────────────────────────┘   │
└────────────────────┬─────────────────────────┘
                     │
                     │ asyncpg driver
                     │ (Async SQL)
                     │
        ┌────────────▼─────────────┐
        │   PostgreSQL Database    │
        │                          │
        │  ┌────────────────────┐  │
        │  │ companies          │  │
        │  ├────────────────────┤  │
        │  │ employees          │  │
        │  ├────────────────────┤  │
        │  │ cards              │  │
        │  ├────────────────────┤  │
        │  │ users              │  │
        │  ├────────────────────┤  │
        │  │ subscriptions      │  │
        │  ├────────────────────┤  │
        │  │ analytics          │  │
        │  └────────────────────┘  │
        │                          │
        │ Indexes on company_id    │
        │ Foreign key constraints  │
        │ Automatic timestamps     │
        └──────────────────────────┘
```

---

## Request Flow (Step by Step)

### 1️⃣ Authentication Flow (Signup)

```
Browser
  │
  ├─→ POST /api/auth/signup
  │   {email, password, full_name, role: "admin"}
  │
API
  │
  ├─→ [Security] Create JWT token
  ├─→ [Service] Create Company
  │   ├─→ Generate company_slug
  │   └─→ INSERT INTO companies
  ├─→ [Service] Create User
  │   ├─→ Hash password (bcrypt)
  │   └─→ INSERT INTO users
  ├─→ [Security] Generate JWT (sub=user_id, company_id, role)
  │
  └─← Response: {access_token, token_type, company_id, user_id, role}
```

### 2️⃣ Multi-Tenant Request Flow (Add Employee)

```
Browser
  │
  ├─→ POST /api/company/{company_id}/employees
  │   Headers: Authorization: Bearer {token}
  │   Body: {full_name, job_title, email, ...}
  │
API [Routes]
  │
  ├─→ Extract token → decode JWT
  │   {user_id, company_id, role}
  │
  ├─→ [Security] Verify Authorization
  │   ✓ Is admin or superadmin?
  │   ✓ company_id matches URL param?
  │
  ├─→ [Service] create_employee()
  │   ├─→ Generate public_slug
  │   ├─→ INSERT INTO employees
  │   │   (company_id=extracted_company_id, full_name, ...)
  │   ├─→ [Service] create_card() for employee
  │   │   ├─→ Generate QR code URL
  │   │   ├─→ Generate vCard URL
  │   │   └─→ INSERT INTO cards
  │   └─→ COMMIT transaction
  │
  └─← Response: {employee object with id, public_slug}

Database (Multi-Tenant Isolation)
  │
  └─ All queries automatically filtered by company_id:
     SELECT * FROM employees 
     WHERE company_id = extracted_company_id
```

### 3️⃣ Public Card View (No Auth)

```
Public URL: /card/{company_slug}/{employee_slug}

Browser
  │
  ├─→ GET /api/card/acme-corp/jane-smith-abc123
  │   (No authentication required)
  │
API [Routes]
  │
  ├─→ [Service] get_employee_by_slug(company_slug, employee_slug)
  │   └─→ SELECT e FROM employees e
  │       JOIN companies c ON e.company_id = c.id
  │       WHERE c.slug = 'acme-corp'
  │       AND e.public_slug = 'jane-smith-abc123'
  │
  ├─→ [Service] get_card_by_employee(employee_id)
  │   └─→ SELECT FROM cards WHERE employee_id = ?
  │
  ├─→ [Route] Respond with employee + card + company branding
  │
  └─← Response: {
        employee_name, job_title, email, phone, photo_url,
        company_name, company_logo, company_brand_color,
        qr_code, vcard_url, social_links
      }

Browser Renders
  │
  └─ Branded digital card with:
     - Company logo & color
     - Employee photo
     - Contact buttons
     - QR code
     - Social links
```

### 4️⃣ Analytics Tracking

```
User Action on Public Card
  │
  ├─→ Click "Call" button
  │   └─→ POST /api/analytics/track
  │       ?company_slug=acme-corp&employee_slug=jane-smith-abc123
  │       {action: "call", device: "mobile"}
  │
API
  │
  ├─→ [Service] Lookup employee by slug
  ├─→ [Service] track_event()
  │   └─→ INSERT INTO analytics
  │       (company_id, employee_id, action="call", device="mobile", timestamp)
  │
  └─← Response: {status: "tracked", event_id}

Analytics Dashboard (Admin)
  │
  ├─→ GET /api/analytics/company/{company_id}
  │   Headers: Authorization: Bearer {token}
  │
API
  │
  ├─→ [Security] Verify token.company_id == company_id
  ├─→ [Service] get_analytics_by_company(company_id)
  │   └─→ SELECT * FROM analytics
  │       WHERE company_id = {company_id}
  │       ORDER BY timestamp DESC
  ├─→ [Service] get_analytics_summary(company_id)
  │   └─→ SELECT action, COUNT(*) FROM analytics
  │       WHERE company_id = {company_id}
  │       GROUP BY action
  │
  └─← Response: {
        events: [{...}],
        summary: {view: 45, call: 12, whatsapp: 8, ...}
      }
```

---

## Database Schema Design

### Entity Relationship Diagram

```
┌──────────────────┐
│   companies      │ ◄────┐
├──────────────────┤      │
│ id (PK, UUID)    │      │
│ name             │      │ Foreign Keys
│ domain (unique)  │      │
│ logo_url         │      │
│ brand_color      │      │
│ slug (unique)    │      │
│ created_at       │      │
│ updated_at       │      │
└──────────────────┘      │
       │                  │
       │ 1:N              │
       ├─────────────────►┤
       │                  │
       │         ┌────────▼─────────────┐
       │         │   employees          │
       │         ├──────────────────────┤
       │         │ id (PK, UUID)        │
       │         │ company_id (FK) ◄────┤
       │         │ full_name            │
       │         │ job_title            │
       │         │ email                │
       │         │ phone                │
       │         │ whatsapp             │
       │         │ photo_url            │
       │         │ bio                  │
       │         │ social_links (JSON)  │
       │         │ public_slug (unique) │
       │         │ created_at           │
       │         │ updated_at           │
       │         └─────────────────────┬┘
       │                               │
       │                    ┌──────────▼──────────┐
       │                    │ cards               │
       │                    ├─────────────────────┤
       │                    │ id (PK, UUID)       │
       │                    │ employee_id (FK)    │
       │                    │ url                 │
       │                    │ qr_code             │
       │                    │ vcard_url           │
       │                    │ created_at          │
       │                    │ updated_at          │
       │                    └─────────────────────┘
       │
       │ 1:N
       └──────────────────┬──────────────────┐
       │                  │                  │
       │         ┌────────▼─────────┐   ┌───▼──────────────┐
       │         │ users            │   │ subscriptions    │
       │         ├──────────────────┤   ├──────────────────┤
       │         │ id (PK, UUID)    │   │ id (PK, UUID)    │
       │         │ company_id (FK)  │   │ company_id (FK)  │
       │         │ email (unique)   │   │ plan             │
       │         │ password_hash    │   │ active           │
       │         │ full_name        │   │ started_at       │
       │         │ role             │   │ ended_at         │
       │         │ is_active        │   │ created_at       │
       │         │ created_at       │   └──────────────────┘
       │         └──────────────────┘
       │
       │ 1:N
       └──────────────────────┬──────────────────────┐
       │                      │                      │
       │        ┌─────────────▼────────────┐    ┌───▼──────────────────┐
       │        │ analytics                │    │ (more joins)         │
       │        ├──────────────────────────┤    │                      │
       │        │ id (PK, UUID)            │    │ employees ──┐        │
       │        │ company_id (FK)          │    │             │        │
       │        │ employee_id (FK, NULL ok)│◄───┤             │        │
       │        │ timestamp                │    │ cards ──┐   │        │
       │        │ device                   │    │         │   │        │
       │        │ region                   │    │ users ──┤   │        │
       │        │ action                   │    │         │   │        │
       │        │ ip_address               │    │ subscr..│   │        │
       │        └──────────────────────────┘    └─────────┴───┴────────┘
       │
       └─ Indexes on:
          - company_id (all tables)
          - employee_id
          - timestamp
          - slug fields

Multi-Tenant Isolation:
- ALL queries include WHERE company_id = {user_company_id}
- Prevents cross-tenant data leakage
- Row-Level Security (RLS) ready for Supabase
```

---

## API Layer Architecture

### Endpoint Organization

```
/api

├── /auth (Public)
│   ├── POST   /signup            → Create company + user + token
│   └── POST   /login             → Authenticate user + return token
│
├── /company (Protected: admin/superadmin)
│   ├── POST   /                  → Create new company
│   ├── GET    /{company_id}      → Get company details
│   └── GET    /{company_id}/employees → List company employees
│
├── /employees (Protected: admin/employee)
│   ├── POST   /company/{cid}/    → Add employee to company
│   ├── GET    /{employee_id}     → Get employee details
│   └── PUT    /{employee_id}     → Update employee profile
│
├── /card (Public)
│   └── GET    /{company_slug}/{employee_slug} → View public card
│
├── /analytics
│   ├── POST   /track?company_slug=X&employee_slug=Y (Public)
│   ├── GET    /company/{company_id} (Protected: admin)
│   └── GET    /employee/{employee_id} (Protected: admin/employee)
│
└── /health (Public)
    └── GET    /                  → Service status
```

### Dependency Injection Pattern

```python
# Routes layer uses FastAPI dependencies for:

@router.get("/company/{company_id}")
async def get_company(
    company_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),  # Auth check
    db: AsyncSession = Depends(get_db),              # DB session
):
    # Middleware automatically:
    # 1. Validates JWT token
    # 2. Extracts user info (id, company_id, role)
    # 3. Gets database session
    # 4. Provides both to route handler
```

---

## Security Model

### Token Structure

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",  // user_id
  "company_id": "660e8400-e29b-41d4-a716-446655440001",
  "role": "admin",  // admin | employee | superadmin
  "exp": 1700000000,  // expiration (7 days)
  "iat": 1699396000   // issued at
}
```

### RBAC Permission Matrix

```
                 | superadmin | admin | employee | public |
─────────────────┼────────────┼───────┼──────────┼────────┤
 View all        |     ✓      |       |          |        |
 companies       |            |       |          |        |
─────────────────┼────────────┼───────┼──────────┼────────┤
 Manage own      |     ✓      |   ✓   |          |        |
 company         |            |       |          |        |
─────────────────┼────────────┼───────┼──────────┼────────┤
 Add employees   |     ✓      |   ✓   |          |        |
─────────────────┼────────────┼───────┼──────────┼────────┤
 View own        |     ✓      |   ✓   |    ✓     |        |
 employees       |            |       |          |        |
─────────────────┼────────────┼───────┼──────────┼────────┤
 View/edit own   |     ✓      |   ✓   |    ✓     |        |
 profile         |            |       |          |        |
─────────────────┼────────────┼───────┼──────────┼────────┤
 View public     |     ✓      |   ✓   |    ✓     |    ✓   |
 card            |            |       |          |        |
─────────────────┼────────────┼───────┼──────────┼────────┤
 Track analytics |     ✓      |   ✓   |          |    ✓   |
─────────────────┼────────────┼───────┼──────────┼────────┤
 View analytics  |     ✓      |   ✓   |    ✓     |        |
─────────────────┼────────────┼───────┼──────────┼────────┤
```

### Multi-Tenant Isolation Enforcement

```python
# Every service method checks company_id:

async def update_employee(
    session: AsyncSession,
    employee_id: uuid.UUID,
    current_user_company_id: uuid.UUID,  # From JWT
    new_data: EmployeeUpdate
):
    # Step 1: Fetch employee
    employee = await session.execute(
        select(Employee).where(Employee.id == employee_id)
    )
    
    # Step 2: Verify company_id matches
    if employee.company_id != current_user_company_id:
        raise PermissionError("Not authorized")  # 403
    
    # Step 3: Update safely
    ...
```

---

## Deployment Architecture

### Docker Compose Network

```
Digital Cards Network (digital-cards-network)
│
├─ postgres:5432
│  ├─ Image: postgres:15-alpine
│  ├─ Volume: postgres_data:/var/lib/postgresql/data
│  ├─ Environment:
│  │  ├─ POSTGRES_USER
│  │  ├─ POSTGRES_PASSWORD
│  │  └─ POSTGRES_DB
│  └─ Health Check: pg_isready
│
├─ backend:8000
│  ├─ Build: ./backend/Dockerfile
│  ├─ Environment:
│  │  ├─ DATABASE_URL
│  │  ├─ SECRET_KEY
│  │  └─ CORS_ORIGINS
│  ├─ Depends On: postgres (health check)
│  ├─ Volume: ./backend:/app (live reload)
│  └─ Command: uvicorn main:app --reload
│
└─ frontend:3000
   ├─ Build: ./frontend/Dockerfile
   ├─ Environment:
   │  └─ NEXT_PUBLIC_API_URL
   ├─ Depends On: backend (service_started)
   ├─ Volume: ./frontend:/app (live reload)
   └─ Command: npm run dev
```

### Production Deployment (Simplified)

```
                    Users
                     │
        ┌────────────┴────────────┐
        │                         │
   CDN (Static)           Load Balancer (nginx)
        │                         │
        │              ┌──────────┼──────────┐
        │              │          │          │
        │         ┌────▼──┐ ┌────▼──┐ ┌────▼──┐
        │         │Backend│ │Backend│ │Backend│  (Horizontal Scale)
        │         │  Pod1 │ │  Pod2 │ │  Pod3 │
        │         └────┬──┘ └────┬──┘ └────┬──┘
        │              │         │         │
        │              └────┬────┴────┬────┘
        │                   │        │
        │                   │   ┌────▼─────────────┐
        │                   │   │ PostgreSQL       │
        │                   │   │ (Primary)        │
        │                   │   ├──────────────────┤
        │                   │   │ Replicas (Read)  │
        │                   │   ├──────────────────┤
        │                   │   │ Backups (Nightly)│
        │                   │   └──────────────────┘
        │                   │
        │         ┌─────────┴─────────┐
        │         │                   │
        │    ┌────▼────┐         ┌────▼──────┐
        │    │ Redis   │         │ ElasticSrch│
        │    │ (Cache) │         │ (Analytics)│
        │    └─────────┘         └────────────┘
        │
   ┌────▼────────────────────┐
   │ Frontend (Next.js)       │
   │ on Vercel/Netlify/       │
   │ AWS CloudFront           │
   └──────────────────────────┘
```

---

## Scalability Roadmap

### Current (Small Scale: < 10K users)
- Single FastAPI instance
- Single PostgreSQL instance
- No caching
- ✓ All-in-one docker-compose

### Phase 1 (Medium Scale: 10K - 100K users)
- Horizontal scaling (multiple API instances)
- Database read replicas
- Redis caching layer
- Separate analytics processing (async jobs)

### Phase 2 (Large Scale: 100K+ users)
- Microservices architecture
- Elasticsearch for analytics
- Message queue (RabbitMQ/Kafka)
- GraphQL API layer
- Multi-region deployment

---

**This architecture is designed for growth while maintaining simplicity at launch.** 🚀

