# Digital Business Cards - DigitalOcean Deployment Guide

This guide provides step-by-step instructions to deploy the Digital Business Cards application on a DigitalOcean Ubuntu droplet.

## Prerequisites

- DigitalOcean account with an Ubuntu 22.04 LTS or 24.04 droplet (minimum 2GB RAM, 1 CPU)
- SSH access to your droplet
- Domain name (optional but recommended)
- GitHub account with your repository: `https://github.com/ebra-hazard/DigitalBusinessCard`

## Part 1: Initial Server Setup

### Step 1.1: Connect to Your Droplet

```bash
ssh root@YOUR_DROPLET_IP
```

Replace `YOUR_DROPLET_IP` with your actual droplet IP address.

### Step 1.2: Update System Packages

```bash
apt update && apt upgrade -y
```

### Step 1.3: Create a Non-Root User (Recommended)

```bash
adduser deploy
usermod -aG sudo deploy
su - deploy
```

### Step 1.4: Set Up SSH Key (Optional but Recommended)

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

On your local machine:
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub deploy@YOUR_DROPLET_IP
```

## Part 2: Install Required Dependencies

### Step 2.1: Install Docker and Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add current user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Step 2.2: Install Git

```bash
sudo apt install -y git
git --version
```

### Step 2.3: Install Additional Tools

```bash
sudo apt install -y curl wget nano htop
```

## Part 3: Deploy the Application

### Step 3.1: Clone the Repository

```bash
cd /opt
sudo git clone https://github.com/ebra-hazard/DigitalBusinessCard.git
sudo chown -R $USER:$USER DigitalBusinessCard
cd DigitalBusinessCard
```

### Step 3.2: Create Environment Configuration Files

**Copy the sample environment file:**

```bash
# Create .env for production
cat > .env.production << 'EOF'
# Backend Configuration
API_HOST=YOUR_DROPLET_IP_OR_DOMAIN
API_PORT=8000
FRONTEND_HOST=YOUR_DROPLET_IP_OR_DOMAIN
FRONTEND_PORT=3000
ENVIRONMENT=production

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/digital_cards
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=digital_cards

# CORS and Allowed Hosts (use your domain or IP)
CORS_ORIGINS=https://YOUR_DROPLET_IP_OR_DOMAIN,https://www.YOUR_DOMAIN
ALLOWED_HOSTS=YOUR_DROPLET_IP_OR_DOMAIN,www.YOUR_DOMAIN

# Frontend Public API Configuration
NEXT_PUBLIC_API_HOST=YOUR_DROPLET_IP_OR_DOMAIN
NEXT_PUBLIC_API_PORT=443

# JWT Secret (generate a strong secret)
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# Email Configuration (optional for password reset)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@your-domain.com
EOF
```

**Important:** Edit the `.env.production` file with your actual values:

```bash
nano .env.production
```

Replace these values:
- `YOUR_DROPLET_IP_OR_DOMAIN`: Your DigitalOcean droplet IP or domain name
- `your-super-secret-jwt-key-change-this-in-production`: Generate a strong JWT secret
- Email configuration (if you want password reset emails)

### Step 3.3: Set Up SSL Certificate (Using Let's Encrypt)

If you have a domain name, set up SSL:

```bash
sudo apt install -y certbot python3-certbot-nginx

# Generate SSL certificate
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com
```

Save the certificate paths. You'll need them for nginx.

### Step 3.4: Configure Nginx as Reverse Proxy

```bash
# Install Nginx
sudo apt install -y nginx

# Create nginx configuration
sudo tee /etc/nginx/sites-available/digital-cards << 'EOF'
upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name YOUR_DOMAIN_OR_IP;

    # SSL Configuration (if using Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Logging
    access_log /var/log/nginx/digital-cards-access.log;
    error_log /var/log/nginx/digital-cards-error.log;

    # Client upload size
    client_max_body_size 50M;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # API Backend
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://backend;
        access_log off;
    }
}
EOF
```

**Edit the configuration:**

```bash
sudo nano /etc/nginx/sites-available/digital-cards
```

Replace `YOUR_DOMAIN_OR_IP` with your domain or IP, and update SSL paths if using Let's Encrypt.

**Enable the site:**

```bash
sudo ln -s /etc/nginx/sites-available/digital-cards /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove default site
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

### Step 3.5: Start Docker Containers

```bash
cd /opt/DigitalBusinessCard

# Build and start containers
docker-compose -f docker-compose.yml up -d

# Verify containers are running
docker-compose ps
```

### Step 3.6: Initialize Database (First Time Only)

```bash
# Wait 10 seconds for database to start
sleep 10

# Run any migrations if needed
docker-compose exec backend python -m alembic upgrade head

# Create sample data (optional)
docker-compose exec backend python -c "
import asyncio
from database import get_db, AsyncSessionLocal
from services import create_user, create_company, get_user_by_email
from models import UserCreate, CompanyCreate
from security import hash_password

# Add setup code here if needed
"
```

## Part 4: Verify Deployment

### Step 4.1: Check Services Status

```bash
# Check Docker containers
docker-compose ps

# Check Nginx
sudo systemctl status nginx

# Check logs
docker-compose logs backend | tail -50
docker-compose logs frontend | tail -50
```

### Step 4.2: Test Endpoints

```bash
# Health check
curl http://localhost:8000/api/health

# Frontend
curl http://localhost:3000

# With your domain (if configured)
curl https://your-domain.com/api/health
```

### Step 4.3: Monitor Application

```bash
# View real-time logs
docker-compose logs -f

# Check resource usage
docker stats
```

## Part 5: Set Up Automatic Backups and Monitoring

### Step 5.1: Database Backups

Create a backup script:

```bash
cat > ~/backup-database.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/DigitalBusinessCard/backups"
mkdir -p $BACKUP_DIR
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

docker-compose -f /opt/DigitalBusinessCard/docker-compose.yml exec -T postgres pg_dump -U postgres digital_cards | gzip > $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz

# Keep only last 7 backups
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete

echo "Database backed up to $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz"
EOF

chmod +x ~/backup-database.sh
```

Schedule daily backups:

```bash
# Add to crontab
(crontab -l 2>/dev/null; echo "0 2 * * * ~/backup-database.sh") | crontab -
```

### Step 5.2: Set Up Log Rotation

```bash
sudo tee /etc/logrotate.d/digital-cards << 'EOF'
/var/log/nginx/digital-cards-*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload nginx > /dev/null 2>&1 || true
    endscript
}
EOF
```

## Part 6: Maintenance and Troubleshooting

### Restart Services

```bash
# Restart all containers
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart frontend

# Full restart
docker-compose down && docker-compose up -d
```

### View Logs

```bash
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# Database logs
docker-compose logs postgres

# Real-time logs
docker-compose logs -f
```

### Update Application

```bash
cd /opt/DigitalBusinessCard
git pull origin main
docker-compose restart
```

### Backup and Restore Database

**Backup:**
```bash
docker-compose exec postgres pg_dump -U postgres digital_cards > backup.sql
```

**Restore:**
```bash
docker-compose exec -T postgres psql -U postgres digital_cards < backup.sql
```

### Check Disk Space

```bash
df -h
du -sh /opt/DigitalBusinessCard
```

### Monitor Resources

```bash
# CPU and Memory usage
docker stats

# Top processes
htop
```

## Part 7: Security Hardening

### Step 7.1: Configure Firewall

```bash
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw status
```

### Step 7.2: Fail2Ban for SSH Protection

```bash
sudo apt install -y fail2ban

# Start and enable service
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

### Step 7.3: Enable Automatic Security Updates

```bash
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### Step 7.4: Secure Environment Variables

```bash
# Make .env files accessible only by owner
chmod 600 .env.production
chmod 600 .env

# Use secrets manager for sensitive data in production
# Consider using DigitalOcean App Platform or similar
```

## Part 8: Troubleshooting Common Issues

### Issue: Port Already in Use

```bash
# Find process using port
sudo lsof -i :8000
sudo lsof -i :3000
sudo lsof -i :5432

# Kill process
kill -9 <PID>
```

### Issue: Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Rebuild images
docker-compose build --no-cache

# Start fresh
docker-compose down -v
docker-compose up -d
```

### Issue: Database Connection Error

```bash
# Check if postgres is running
docker-compose ps postgres

# Test connection
docker-compose exec postgres psql -U postgres -d digital_cards -c "SELECT 1"
```

### Issue: SSL Certificate Issues

```bash
# Verify certificate
sudo certbot certificates

# Renew certificate
sudo certbot renew

# Force renewal
sudo certbot renew --force-renewal
```

## Part 9: Performance Optimization

### Step 9.1: Enable Gzip Compression

Already configured in Nginx template above.

### Step 9.2: Configure Docker Resource Limits

Edit `docker-compose.yml`:

```yaml
services:
  backend:
    # ... other config
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M

  frontend:
    # ... other config
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### Step 9.3: Database Optimization

```bash
# Connect to database
docker-compose exec postgres psql -U postgres -d digital_cards

# Run optimization
VACUUM ANALYZE;
```

## Part 10: Monitoring and Alerts

### Step 10.1: Set Up Basic Monitoring

```bash
cat > ~/monitor.sh << 'EOF'
#!/bin/bash

# Check if services are running
services=("backend" "frontend" "postgres")

for service in "${services[@]}"; do
    if ! docker-compose ps | grep -q "$service.*Up"; then
        echo "WARNING: $service is not running!"
        # Optionally send email alert
    fi
done

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "WARNING: Disk usage is at $DISK_USAGE%"
fi
EOF

chmod +x ~/monitor.sh
(crontab -l 2>/dev/null; echo "*/5 * * * * ~/monitor.sh") | crontab -
```

## Accessing Your Application

Once deployed, access your application at:

- **Frontend:** `https://your-domain.com` or `https://YOUR_DROPLET_IP`
- **API:** `https://your-domain.com/api` or `https://YOUR_DROPLET_IP:8000/api`
- **Admin Dashboard:** `https://your-domain.com/company-admin/dashboard`

## Quick Reference Commands

```bash
# View all containers
docker-compose ps

# View logs
docker-compose logs -f

# Restart application
docker-compose restart

# Stop application
docker-compose down

# Start application
docker-compose up -d

# Update application
cd /opt/DigitalBusinessCard && git pull && docker-compose restart

# Database backup
docker-compose exec postgres pg_dump -U postgres digital_cards > backup.sql

# SSH into container
docker-compose exec backend bash
docker-compose exec frontend sh
docker-compose exec postgres bash
```

## Support and Further Reading

- Docker Documentation: https://docs.docker.com
- Docker Compose: https://docs.docker.com/compose/
- Nginx Documentation: https://nginx.org/en/docs/
- Let's Encrypt: https://letsencrypt.org/
- DigitalOcean Docs: https://docs.digitalocean.com/

## Notes

- Change all default passwords and secrets in `.env.production`
- Use strong JWT secret (minimum 32 characters)
- Regularly backup your database
- Monitor disk space and resource usage
- Keep system and packages updated
- Consider using DigitalOcean's managed database for production
- Set up CDN (DigitalOcean Spaces) for file storage
