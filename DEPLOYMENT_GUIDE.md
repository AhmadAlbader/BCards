# Deployment Guide: Local Development → DigitalOcean Production

## Overview

This guide covers the complete workflow for:
1. Developing locally on your machine
2. Pushing code to GitHub
3. Deploying to DigitalOcean Droplet
4. Updating production with new changes

---

## Part 1: Initial GitHub Setup

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Create a **private** repository named `digital-business-cards`
3. Do NOT initialize with README (we have one)
4. Copy the repository URL (e.g., `https://github.com/YOUR_USERNAME/digital-business-cards.git`)

### Step 2: Initialize Git Locally

```bash
cd /Users/mac/New\ AI\ Projects/Digital\ Business\ Cards

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/digital-business-cards.git

# Rename branch to main (if needed)
git branch -M main

# Add all files (respects .gitignore)
git add .

# Verify what's being added (should NOT include .env files)
git status

# Create initial commit
git commit -m "Initial commit: Digital Business Cards project"

# Push to GitHub
git push -u origin main
```

### Step 3: Verify on GitHub

Visit https://github.com/YOUR_USERNAME/digital-business-cards
- ✅ Code is there
- ✅ .env.local is NOT there
- ✅ .env.production is NOT there
- ✅ .env.development IS there

---

## Part 2: DigitalOcean Droplet Setup

### Step 1: Create Droplet

1. Login to DigitalOcean
2. Create new Droplet:
   - **Image**: Ubuntu 22.04 LTS
   - **Size**: Minimum 2GB RAM (recommended 4GB for smooth operation)
   - **Region**: Choose closest to your location
   - **Add SSH Key**: (recommended) or use password
3. Copy the droplet IP address

### Step 2: Initial SSH Setup

```bash
# SSH into your droplet
ssh root@YOUR_DROPLET_IP

# Update system
apt update && apt upgrade -y

# Create non-root user (optional but recommended)
adduser appuser
usermod -aG sudo appuser
su - appuser
```

### Step 3: Install Docker & Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group (so you don't need sudo)
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Step 4: Clone Repository

```bash
# Navigate to home directory
cd ~

# Clone your repository
git clone https://github.com/YOUR_USERNAME/digital-business-cards.git
cd digital-business-cards

# Verify .env files are NOT cloned (only templates)
ls -la | grep env
# Should show: .env.development, .env.production.template
# Should NOT show: .env.local, .env.production
```

### Step 5: Create Production .env File

```bash
# Copy template to production file
cp .env.production.template .env.production

# Edit it
sudo nano .env.production
```

Fill in with your actual values:

```
# Replace YOURDOMAIN.COM with your actual domain
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
NEXT_PUBLIC_APP_URL=https://yourdomain.com
API_HOST=yourdomain.com
FRONTEND_HOST=yourdomain.com

# Generate a strong secret key
SECRET_KEY=<use: openssl rand -base64 32>

# Database (if using managed DB)
DATABASE_URL=postgresql+asyncpg://postgres:STRONG_PASSWORD@db.yourdomain.com:5432/digital_cards

DEBUG=false
ENVIRONMENT=production
SSL_ENABLED=true
```

### Step 6: Configure DNS (if using domain)

```bash
# Point your domain to droplet IP
# In your domain registrar:
# A record: yourdomain.com → YOUR_DROPLET_IP
# A record: api.yourdomain.com → YOUR_DROPLET_IP
# or CNAME: api.yourdomain.com → yourdomain.com

# Verify DNS (may take 5-15 minutes to propagate)
nslookup yourdomain.com
```

### Step 7: Setup SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificates (adjust domain)
sudo certbot certonly --standalone -d yourdomain.com -d api.yourdomain.com

# Certificate paths will be:
# /etc/letsencrypt/live/yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/yourdomain.com/privkey.pem

# Auto-renew certificates
sudo systemctl enable certbot.timer
```

---

## Part 3: Initial Deployment

```bash
cd ~/digital-business-cards

# Start services
docker-compose up -d

# Verify containers are running
docker-compose ps

# Check logs
docker logs digital-cards-backend
docker logs digital-cards-frontend

# Test backend API
curl https://api.yourdomain.com/docs

# Test frontend
curl https://yourdomain.com
```

---

## Part 4: Development Workflow

### Local Development

```bash
# On your local machine
cd /Users/mac/New\ AI\ Projects/Digital\ Business\ Cards

# Make changes
# Edit files as needed

# Test locally
docker-compose up -d
# Visit http://192.168.1.123:3000

# When ready to deploy
git add .
git commit -m "Description of changes"
git push origin main
```

### Update Production

```bash
# SSH into droplet
ssh appuser@YOUR_DROPLET_IP

# Navigate to project
cd ~/digital-business-cards

# Pull latest changes
git pull origin main

# Restart services (new code is loaded)
docker-compose down
docker-compose up -d

# Verify deployment
docker logs digital-cards-backend

# Test the site
curl https://yourdomain.com
```

---

## Part 5: Branching Strategy (Recommended)

For safer development:

```bash
# On local machine - create feature branch
git checkout -b feature/new-feature

# Make changes
git add .
git commit -m "Add new feature"

# Push branch
git push origin feature/new-feature

# On GitHub: Create Pull Request
# Review changes
# Merge to main

# Pull production update
git pull origin main

# Deploy to DigitalOcean
# (steps from "Update Production" above)
```

---

## Part 6: Keeping Secrets Safe

### Files to NEVER commit:

```bash
# Remove if accidentally added
git rm --cached .env.production
git rm --cached .env.local

# Commit the removal
git commit -m "Remove env files from tracking"
git push origin main
```

### Secure environment variables on server:

```bash
# On DigitalOcean, .env.production should be:
# - Readable by docker user only
sudo chmod 600 .env.production
sudo chown appuser:appuser .env.production

# Never push secrets to GitHub
cat .env.production | grep SECRET
# This file should NEVER be in git
```

---

## Part 7: Automated Deployment (Optional - Advanced)

Create a deployment script on your server:

```bash
# ~/deploy.sh
#!/bin/bash
cd ~/digital-business-cards
git pull origin main
docker-compose down
docker-compose up -d
docker logs digital-cards-backend
```

Make executable:

```bash
chmod +x ~/deploy.sh
```

Then deploy with:

```bash
./deploy.sh
```

Or set up GitHub Actions for automated deployment on push to main.

---

## Part 8: Monitoring & Logs

```bash
# Check if services are running
docker-compose ps

# View backend logs
docker logs digital-cards-backend -f

# View frontend logs
docker logs digital-cards-frontend -f

# Check database
docker logs digital-cards-db

# View last 50 lines
docker logs -n 50 digital-cards-backend

# Access backend shell
docker exec -it digital-cards-backend /bin/bash

# Access frontend shell
docker exec -it digital-cards-frontend /bin/sh
```

---

## Part 9: Troubleshooting

### Services won't start

```bash
# Check .env.production exists
ls -la .env.production

# Check Docker daemon is running
docker ps

# View detailed logs
docker-compose logs

# Rebuild images
docker-compose build --no-cache
docker-compose up -d
```

### API not reachable

```bash
# Check firewall
sudo ufw status

# Allow ports
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
sudo ufw allow 3000/tcp

# Check DNS
nslookup yourdomain.com
```

### Database connection failed

```bash
# Check DATABASE_URL in .env.production
cat .env.production | grep DATABASE_URL

# Test connection
docker exec digital-cards-backend \
  python3 -c "from backend.database import engine; print('OK')"
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Clone repo | `git clone https://github.com/USERNAME/digital-business-cards.git` |
| Create env | `cp .env.production.template .env.production && nano .env.production` |
| Deploy | `docker-compose down && docker-compose up -d` |
| Check status | `docker-compose ps` |
| View logs | `docker logs digital-cards-backend -f` |
| Pull updates | `git pull origin main && docker-compose restart` |

---

## Support & Next Steps

1. ✅ GitHub repo created
2. ✅ DigitalOcean droplet configured
3. ✅ DNS pointing to droplet
4. ✅ SSL certificate installed
5. ✅ Services running
6. 📍 Ready for development → deployment workflow
