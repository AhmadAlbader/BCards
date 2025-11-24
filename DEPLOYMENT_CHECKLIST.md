# 🚀 Deployment Checklist

## Pre-Deployment

### Local Testing
- [ ] Run `docker-compose up -d` successfully
- [ ] All 3 services (postgres, backend, frontend) are running
- [ ] Frontend loads at http://localhost:3000
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Database migrations ran without errors
- [ ] Can signup with new account
- [ ] Can add employees
- [ ] Public card view works
- [ ] Analytics tracking works

### Code Quality
- [ ] No console errors in frontend
- [ ] No backend Python errors in logs
- [ ] Environment variables are set in `.env`
- [ ] `.gitignore` properly excludes node_modules, venv, .env
- [ ] Sensitive keys not committed (check git history)

---

## Production Environment Setup

### Secrets Management
```bash
# Generate strong SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Store in production secret manager (AWS Secrets, Heroku Config, etc)
```

### Environment Variables (Production)
```env
# Backend
DATABASE_URL=postgresql+asyncpg://user:password@prod-db.example.com:5432/digital_cards
SECRET_KEY=your-generated-secret-key-here
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
ALLOWED_HOSTS=yourdomain.com,app.yourdomain.com
ENV=production
DEBUG=false

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
```

---

## Database Setup (Production)

### PostgreSQL Hosting Options
1. **AWS RDS** (Recommended for scale)
2. **Supabase** (Managed PostgreSQL + Realtime)
3. **Heroku PostgreSQL**
4. **Neon** (Serverless PostgreSQL)
5. **Digital Ocean** (Self-managed)

### Database Initialization
```bash
# Create tables
docker run --rm -e DATABASE_URL="postgresql://..." \
  -v ./backend:/app digital-cards-backend \
  alembic upgrade head

# Or use Heroku Release Phase
# In Procfile: release: alembic upgrade head
```

### Backup Strategy
- [ ] Enable automated backups
- [ ] Test restore procedure
- [ ] Set retention to 30+ days
- [ ] Document backup recovery steps

---

## Backend Deployment

### Option 1: Heroku (Simplest)
```bash
# Install Heroku CLI
brew install heroku

# Login
heroku login

# Create app
heroku create digital-cards-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:standard-0 --app digital-cards-api

# Set environment variables
heroku config:set SECRET_KEY=your-key --app digital-cards-api
heroku config:set CORS_ORIGINS=https://yourdomain.com --app digital-cards-api

# Deploy
git push heroku main

# Run migrations
heroku run "alembic upgrade head" --app digital-cards-api
```

### Option 2: AWS (ECS + RDS)
```bash
# Build Docker image
docker build -t digital-cards-backend:latest ./backend

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker tag digital-cards-backend:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/digital-cards-backend:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/digital-cards-backend:latest

# Deploy to ECS cluster
# (Use AWS CloudFormation or Terraform)
```

### Option 3: Docker (Self-Managed)
```bash
# Build & push to Docker Hub
docker build -t yourname/digital-cards-backend:latest ./backend
docker push yourname/digital-cards-backend:latest

# On production server:
docker run -d \
  -e DATABASE_URL=postgresql://... \
  -e SECRET_KEY=... \
  -p 8000:8000 \
  --name api \
  yourname/digital-cards-backend:latest
```

### Post-Deployment Checks
- [ ] Health check endpoint responds
- [ ] Can authenticate (signup/login)
- [ ] Database queries work
- [ ] CORS headers correct
- [ ] Error logging configured

---

## Frontend Deployment

### Option 1: Vercel (Recommended - Built for Next.js)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel --prod

# Set environment variable
vercel env add NEXT_PUBLIC_API_URL https://api.yourdomain.com/api
```

### Option 2: Netlify
```bash
# Create netlify.toml
cat > frontend/netlify.toml << 'EOF'
[build]
command = "npm run build"
publish = ".next"

[[redirects]]
from = "/*"
to = "/index.html"
status = 200
EOF

# Deploy
netlify deploy --prod --dir=frontend/.next
```

### Option 3: AWS CloudFront + S3
```bash
# Build Next.js app
npm run build

# Deploy with static export (if applicable)
# Or use AWS Amplify for serverless hosting
```

### Option 4: Docker (Self-Managed)
```bash
docker build -t yourname/digital-cards-frontend:latest ./frontend
docker push yourname/digital-cards-frontend:latest

docker run -d \
  -e NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api \
  -p 3000:3000 \
  --name web \
  yourname/digital-cards-frontend:latest
```

### Post-Deployment Checks
- [ ] Frontend loads without errors
- [ ] Can signup/login
- [ ] API calls work
- [ ] Public cards accessible
- [ ] Analytics tracking works

---

## SSL/TLS & Domain Setup

### DNS Configuration
```
A Record: yourdomain.com → your-server-ip
A Record: api.yourdomain.com → your-api-ip
CNAME: www.yourdomain.com → yourdomain.com
```

### SSL Certificates
- [ ] Get certificate (Let's Encrypt free or commercial)
- [ ] Enable auto-renewal
- [ ] Test HTTPS endpoints
- [ ] Redirect HTTP → HTTPS

### For Vercel/Netlify
- Auto-configured, no action needed

---

## Monitoring & Logging

### Backend Monitoring
```bash
# Setup error tracking (Sentry)
pip install sentry-sdk
# Configure in main.py

# Log aggregation (CloudWatch, DataDog, etc)
# Setup in docker-compose for production
```

### Frontend Monitoring
```bash
# Install Sentry React SDK
npm install @sentry/react @sentry/tracing

# Configure in layout.tsx
```

### Health Checks
- [ ] Setup endpoint monitoring
- [ ] Alert on downtime
- [ ] Monitor database connectivity
- [ ] Track API response times

### Metrics to Track
- [ ] API response times (p50, p95, p99)
- [ ] Error rates
- [ ] Database query performance
- [ ] User signups/logins
- [ ] Card views (analytics)

---

## Performance Optimization

### Backend
- [ ] Enable query caching (Redis)
- [ ] Setup database connection pooling
- [ ] Enable gzip compression
- [ ] Use CDN for static files
- [ ] Monitor slow queries

### Frontend
- [ ] Enable Next.js ISR (Incremental Static Regeneration)
- [ ] Setup image optimization
- [ ] Enable code splitting
- [ ] Use CDN for assets
- [ ] Analyze bundle size

---

## Security Hardening

### Backend
- [ ] Rotate SECRET_KEY regularly
- [ ] Enable rate limiting on auth endpoints
- [ ] Setup CORS properly
- [ ] Use HTTPS only (force redirect)
- [ ] Keep dependencies updated
- [ ] Setup Web Application Firewall (WAF)
- [ ] Enable SQL injection protection

### Frontend
- [ ] Enable Content Security Policy (CSP)
- [ ] Remove sensitive data from localStorage
- [ ] Implement proper CORS in Next.js config
- [ ] Setup dependencies scanning
- [ ] Enable subresource integrity for CDN

### Database
- [ ] Enable SSL connections
- [ ] Setup backup encryption
- [ ] Enable audit logging
- [ ] Restrict access by IP
- [ ] Regular security updates

---

## Scaling Checklist

### For 1K-10K Users
- [ ] Single app server + PostgreSQL sufficient
- [ ] Enable horizontal scaling (Heroku dynos/AWS ECS)
- [ ] Setup Redis for caching
- [ ] Monitor database performance

### For 10K-100K Users
- [ ] Database read replicas
- [ ] Redis cluster for caching
- [ ] CDN for static assets
- [ ] Load balancer for backend
- [ ] API gateway (nginx, Kong)

### For 100K+ Users
- [ ] Microservices architecture
- [ ] Separate analytics processing (async jobs)
- [ ] Elasticsearch for search
- [ ] Message queue (RabbitMQ, Kafka)
- [ ] GraphQL API layer
- [ ] Multi-region deployment

---

## Disaster Recovery

### Backup Strategy
- [ ] Daily automated backups
- [ ] 30-day retention minimum
- [ ] Test restore monthly
- [ ] Document recovery procedures
- [ ] Store backups in different region

### Failover Plan
- [ ] Database replica/standby
- [ ] Load balancer with health checks
- [ ] Automated failover triggers
- [ ] Communication plan for downtime
- [ ] Runbook for manual recovery

---

## Launch Checklist (Final)

### 48 Hours Before
- [ ] All tests passing locally
- [ ] Staging environment tested
- [ ] Backup procedures tested
- [ ] Team trained on deployment

### 24 Hours Before
- [ ] Reserve time on calendar
- [ ] Notify team of launch
- [ ] Prepare rollback plan
- [ ] Brief runbook ready

### Launch Day
- [ ] Database migrations tested
- [ ] Environment variables verified
- [ ] SSL certificates valid
- [ ] DNS propagated
- [ ] Monitoring setup confirmed
- [ ] Deploy backend
- [ ] Deploy frontend
- [ ] Run smoke tests
- [ ] Monitor for errors (2 hours)

### Post-Launch
- [ ] Monitor error rates (24 hours)
- [ ] Check analytics data
- [ ] Verify all features working
- [ ] Get user feedback
- [ ] Document lessons learned

---

## Rollback Plan

```bash
# If something goes wrong:

# Revert to previous version
git revert <commit-hash>
git push

# Or redeploy stable image
docker run -d --name api-rollback \
  -e DATABASE_URL=... \
  yourname/digital-cards-backend:v1.0.0

# Update DNS/load balancer to point to stable version
```

---

## Post-Launch Monitoring (First Week)

Daily Review:
- [ ] Error rates normal
- [ ] Performance metrics stable
- [ ] User feedback positive
- [ ] Database size growing normally
- [ ] No unexpected costs

---

## Contact & Support

### Critical Issues
- Page down / API unresponsive
- Data loss / database corruption
- Security breach

**Action:** Activate incident response team

### Enhancement Requests
- Log in Issues tracking system
- Prioritize in next sprint
- Communicate timeline to users

---

**Ready to deploy! 🚀**

Remember: **Test in staging before production. Always have a rollback plan.**

