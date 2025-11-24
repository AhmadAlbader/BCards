# Complete Setup Guide: Local Development → GitHub → DigitalOcean Production

This guide walks you through the complete workflow for your Digital Business Cards application.

---

## 📋 Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Push to GitHub](#push-to-github)
3. [Deploy to DigitalOcean](#deploy-to-digitalocean)
4. [Development Workflow](#development-workflow)
5. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites

- Docker and Docker Compose installed
- Git installed
- Node.js 18+ (for frontend development)
- Python 3.9+ (for backend development)

### 1. Verify Local Configuration

```bash
cd /Users/mac/New\ AI\ Projects/Digital\ Business\ Cards

# Check environment files
ls -la | grep .env
# Should show: .env.local, .env.development

# Verify Docker setup
docker --version
docker-compose --version
```

### 2. Start Local Services

```bash
# Start all services
docker-compose up -d

# Verify containers are running
docker-compose ps

# Check logs
docker logs digital-cards-backend
docker logs digital-cards-frontend

# Access services
# Frontend: http://192.168.1.123:3000
# Backend API: http://192.168.1.123:8000
# API Docs: http://192.168.1.123:8000/docs
```

### 3. Test All Features

```bash
# Test card display
curl http://192.168.1.123:3000/card/test-admin-s-company-8f8d7331/alice-johnson-1e569e00

# Test vCard download
curl http://192.168.1.123:3000/api/vcard?company_slug=test-admin-s-company-8f8d7331&employee_slug=alice-johnson-1e569e00

# Test QR code
curl http://192.168.1.123:3000/api/qrcode?company_slug=test-admin-s-company-8f8d7331&employee_slug=alice-johnson-1e569e00

# Test backend API
curl http://192.168.1.123:8000/api/card/test-admin-s-company-8f8d7331/alice-johnson-1e569e00
```

✅ Local development is ready!

---

## Push to GitHub

### 1. Create Private Repository

See: `GITHUB_PUSH_GUIDE.md` section "Step 1"

### 2. Add GitHub Remote

```bash
cd /Users/mac/New\ AI\ Projects/Digital\ Business\ Cards

# Replace YOUR_USERNAME
git remote add origin https://github.com/YOUR_USERNAME/digital-business-cards.git
git branch -M main
git push -u origin main
```

### 3. Verify on GitHub

Visit: `https://github.com/YOUR_USERNAME/digital-business-cards`

✅ Code is now backed up on GitHub!

---

## Deploy to DigitalOcean

### 1. Create & Configure Droplet

See: `DEPLOYMENT_GUIDE.md` section "Part 2: DigitalOcean Droplet Setup"

**Quick summary:**
```bash
# On your local machine, SSH into droplet
ssh root@YOUR_DROPLET_IP

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Clone Repository

```bash
# SSH into droplet
ssh root@YOUR_DROPLET_IP

# Clone repository
cd ~
git clone https://github.com/YOUR_USERNAME/digital-business-cards.git
cd digital-business-cards
```

### 3. Create Production Environment

```bash
# Copy template to production env
cp .env.production.template .env.production

# Edit with your values
nano .env.production
```

**Update these values:**
```
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
NEXT_PUBLIC_APP_URL=https://yourdomain.com
API_HOST=yourdomain.com
FRONTEND_HOST=yourdomain.com
SECRET_KEY=<generate: openssl rand -base64 32>
DATABASE_URL=postgresql+asyncpg://postgres:STRONG_PASSWORD@localhost:5432/digital_cards
DEBUG=false
ENVIRONMENT=production
SSL_ENABLED=true
```

### 4. Configure SSL Certificate

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificates (replace with your domain)
sudo certbot certonly --standalone -d yourdomain.com -d api.yourdomain.com

# Update .env.production with cert paths
SSL_CERT_PATH=/etc/letsencrypt/live/yourdomain.com/fullchain.pem
SSL_KEY_PATH=/etc/letsencrypt/live/yourdomain.com/privkey.pem
```

### 5. Start Services

```bash
cd ~/digital-business-cards

# Start all services
docker-compose up -d

# Verify
docker-compose ps

# Check logs
docker logs digital-cards-backend
docker logs digital-cards-frontend

# Test
curl https://yourdomain.com
curl https://api.yourdomain.com/docs
```

✅ Production deployment complete!

---

## Development Workflow

### Local Development → GitHub → Production

#### 1. Local Development

```bash
cd /Users/mac/New\ AI\ Projects/Digital\ Business\ Cards

# Create feature branch
git checkout -b feature/new-feature

# Make changes
# Edit files...

# Test locally
docker-compose down
docker-compose up -d
# Visit http://192.168.1.123:3000
# Test features...

# Commit changes
git add .
git commit -m "Add new feature"
```

#### 2. Push to GitHub

```bash
# Push feature branch
git push origin feature/new-feature

# On GitHub: Create Pull Request and review
# Merge to main when approved

# Pull latest on local
git checkout main
git pull origin main
```

#### 3. Deploy to Production

```bash
# SSH into DigitalOcean droplet
ssh root@YOUR_DROPLET_IP

cd ~/digital-business-cards

# Pull latest changes
git pull origin main

# Restart services (new code is loaded)
docker-compose down
docker-compose up -d

# Verify deployment
docker logs digital-cards-backend
curl https://yourdomain.com
```

---

## Project Structure

```
digital-business-cards/
├── backend/                      # FastAPI backend
│   ├── main.py                   # App entry point
│   ├── routes.py                 # API endpoints
│   ├── services.py               # Business logic
│   ├── database.py               # Database setup
│   ├── database_models.py        # SQLAlchemy models
│   ├── vcard_utils.py            # vCard generation
│   ├── security.py               # JWT & auth
│   └── Dockerfile                # Backend container
│
├── frontend/                     # Next.js frontend
│   ├── src/app/                  # Pages and routes
│   │   ├── api/                  # API proxy routes
│   │   ├── card/                 # Card display page
│   │   ├── auth/                 # Login/signup
│   │   └── company-admin/        # Admin panel
│   ├── package.json              # Dependencies
│   ├── tailwind.config.js        # Styling
│   └── Dockerfile                # Frontend container
│
├── docker-compose.yml            # Container orchestration
├── .env.development              # Development config (committed)
├── .env.production.template      # Production template (committed)
├── .env.local                    # Local overrides (not committed)
├── .gitignore                    # Git ignore rules
│
├── DEPLOYMENT_GUIDE.md           # Detailed deployment steps
├── ENV_CONFIGURATION.md          # Environment setup guide
├── GITHUB_PUSH_GUIDE.md          # GitHub push instructions
├── README.md                     # Project overview
└── ... (other docs)
```

---

## Environment Variables

### Development (.env.development)
```
Used for: Local machine
IP: 192.168.1.123
Protocol: http://
Debug: true
```

### Production (.env.production)
```
Used for: DigitalOcean server
Domain: yourdomain.com
Protocol: https://
Debug: false
SSL: enabled
```

### Local Override (.env.local)
```
Used for: Personal machine settings
Not committed to git
Overrides .env.development
```

---

## Commands Reference

### Git Commands
```bash
git clone <url>                  # Clone repository
git checkout -b <branch>        # Create feature branch
git add .                        # Stage changes
git commit -m "message"         # Commit changes
git push origin <branch>        # Push to GitHub
git pull origin main            # Pull latest
git merge <branch>              # Merge branch
```

### Docker Commands
```bash
docker-compose up -d            # Start services
docker-compose down             # Stop services
docker-compose ps               # View running containers
docker logs <container>         # View logs
docker-compose restart          # Restart services
docker-compose build --no-cache # Rebuild images
```

### Server Commands
```bash
ssh root@IP                     # Connect to server
scp file root@IP:/path          # Copy file to server
curl https://domain.com         # Test endpoint
systemctl restart docker        # Restart Docker
```

---

## Troubleshooting

### Local Issues

**Services won't start:**
```bash
docker-compose down
docker-compose up -d
docker logs digital-cards-backend
```

**Port already in use:**
```bash
# Kill process on port
lsof -i :8000  # Find what's using port
kill -9 <PID>  # Kill process
```

**Git push fails:**
```bash
# Ensure remote is set correctly
git remote -v
# Should show: origin https://github.com/USERNAME/repo.git

# If wrong, fix it:
git remote remove origin
git remote add origin <correct-url>
```

### Production Issues

**SSH connection fails:**
```bash
ssh -i /path/to/key root@IP
# Or use password authentication
```

**Domain not resolving:**
```bash
# Wait 5-15 minutes for DNS to propagate
nslookup yourdomain.com
```

**Services not running on server:**
```bash
cd ~/digital-business-cards
docker-compose ps
docker logs digital-cards-backend
```

**SSL certificate issues:**
```bash
# Check certificate status
sudo certbot certificates

# Renew certificate
sudo certbot renew
```

---

## Support

For detailed information, see:
- **Deployment**: `DEPLOYMENT_GUIDE.md`
- **Environment Setup**: `ENV_CONFIGURATION.md`
- **GitHub**: `GITHUB_PUSH_GUIDE.md`
- **README**: `README.md`

---

## Checklist

### Before Pushing to GitHub
- [ ] All features tested locally
- [ ] No hardcoded IPs (using env vars)
- [ ] `.env.local` not committed
- [ ] `.env.production` not committed
- [ ] Docker services running smoothly
- [ ] No sensitive data in code

### Before Deploying to Production
- [ ] GitHub repository created and code pushed
- [ ] DigitalOcean Droplet created
- [ ] Docker and Docker Compose installed
- [ ] `.env.production` created with correct values
- [ ] SSL certificate obtained
- [ ] DNS configured
- [ ] Firewall rules configured

### After Deployment
- [ ] Frontend accessible via domain
- [ ] Backend API responding
- [ ] Card display working
- [ ] QR codes generating
- [ ] vCard downloads working
- [ ] Analytics tracking
- [ ] Admin panel accessible
- [ ] SSL working (https)

---

🎉 You're all set! Your Digital Business Cards application is ready for production!
