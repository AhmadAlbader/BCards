# Digital Business Cards - DigitalOcean Deployment Quick Reference

## One-Command Deployment (Automated)

```bash
# 1. Connect to your droplet
ssh root@YOUR_DROPLET_IP

# 2. Run automated deployment
curl -fsSL https://raw.githubusercontent.com/ebra-hazard/DigitalBusinessCard/main/deploy.sh | sudo bash
```

The script handles everything automatically.

---

## Manual Step-by-Step Deployment

### Prerequisites
- DigitalOcean Ubuntu 22.04+ droplet
- SSH access
- Domain name (optional, IP works too)

### Step 1: Connect to Droplet
```bash
ssh root@YOUR_DROPLET_IP
```

### Step 2: Install Docker & Dependencies
```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx and SSL tools
sudo apt install -y git nginx certbot python3-certbot-nginx
```

### Step 3: Clone Repository
```bash
cd /opt
sudo git clone https://github.com/ebra-hazard/DigitalBusinessCard.git
sudo chown -R $USER:$USER DigitalBusinessCard
cd DigitalBusinessCard
```

### Step 4: Configure Environment
```bash
# Generate JWT secret
JWT_SECRET=$(openssl rand -base64 32)

# Create .env.production
cat > .env.production << EOF
API_HOST=YOUR_IP_OR_DOMAIN
API_PORT=8000
FRONTEND_HOST=YOUR_IP_OR_DOMAIN
FRONTEND_PORT=443
ENVIRONMENT=production
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/digital_cards
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=digital_cards
CORS_ORIGINS=https://YOUR_IP_OR_DOMAIN
ALLOWED_HOSTS=YOUR_IP_OR_DOMAIN
NEXT_PUBLIC_API_HOST=YOUR_IP_OR_DOMAIN
NEXT_PUBLIC_API_PORT=443
JWT_SECRET=$JWT_SECRET
EOF

chmod 600 .env.production
```

### Step 5: Configure Nginx
```bash
# Backup
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# Create config
sudo tee /etc/nginx/sites-available/digital-cards > /dev/null << 'EOF'
upstream backend { server localhost:8000; }
upstream frontend { server localhost:3000; }

server {
    listen 80;
    server_name _;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name _;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    access_log /var/log/nginx/digital-cards-access.log;
    error_log /var/log/nginx/digital-cards-error.log;
    client_max_body_size 50M;

    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/digital-cards /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Create self-signed cert
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/key.pem \
    -out /etc/nginx/ssl/cert.pem \
    -subj "/CN=localhost"

# Test and restart
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Start Application
```bash
cd /opt/DigitalBusinessCard
docker-compose up -d
sleep 10
docker-compose ps
```

### Step 7: Set Up SSL (If Using Domain)
```bash
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Update Nginx config with real certificates
sudo sed -i 's|/etc/nginx/ssl/cert.pem|/etc/letsencrypt/live/your-domain.com/fullchain.pem|g' /etc/nginx/sites-available/digital-cards
sudo sed -i 's|/etc/nginx/ssl/key.pem|/etc/letsencrypt/live/your-domain.com/privkey.pem|g' /etc/nginx/sites-available/digital-cards
sudo nginx -t
sudo systemctl restart nginx
```

### Step 8: Configure Firewall
```bash
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw status
```

### Step 9: Verify Deployment
```bash
# Check containers
docker-compose ps

# Test API
curl https://YOUR_IP_OR_DOMAIN/api/health

# View logs
docker-compose logs -f
```

---

## Access Your Application

- **Frontend:** `https://YOUR_IP_OR_DOMAIN`
- **API:** `https://YOUR_IP_OR_DOMAIN/api`
- **Admin Dashboard:** `https://YOUR_IP_OR_DOMAIN/company-admin/dashboard`

### Default Test Account
- Email: `testuser@example.com`
- Password: `testpass123`

---

## Essential Commands

```bash
# View all containers
docker-compose ps

# View logs (real-time)
docker-compose logs -f

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend

# Stop services
docker-compose down

# Start services
docker-compose up -d

# Backup database
docker-compose exec postgres pg_dump -U postgres digital_cards > backup.sql

# Restore database
docker-compose exec -T postgres psql -U postgres digital_cards < backup.sql

# SSH into container
docker-compose exec backend bash
docker-compose exec frontend sh

# Check resource usage
docker stats

# View disk usage
df -h
du -sh /opt/DigitalBusinessCard
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
sudo lsof -i :80,443,3000,8000,5432

# Kill process
kill -9 <PID>
```

### Container Won't Start
```bash
# Check logs
docker-compose logs backend

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Database Connection Error
```bash
# Restart database
docker-compose restart postgres
sleep 10
docker-compose restart backend

# Check database
docker-compose exec postgres psql -U postgres -d digital_cards -c "SELECT 1"
```

### Nginx 502 Bad Gateway
```bash
# Check if backend is running
docker-compose ps backend

# Restart Nginx
sudo systemctl restart nginx

# Check Nginx error log
sudo tail -50 /var/log/nginx/digital-cards-error.log
```

### SSL Certificate Error
```bash
# Check certificate
sudo certbot certificates

# Renew certificate
sudo certbot renew

# Force renewal
sudo certbot renew --force-renewal
```

---

## Maintenance

### Set Up Auto-Backups
```bash
# Create backup script
cat > ~/backup.sh << 'EOF'
#!/bin/bash
docker-compose -f /opt/DigitalBusinessCard/docker-compose.yml exec -T postgres pg_dump -U postgres digital_cards | gzip > /opt/DigitalBusinessCard/backups/db_$(date +%Y%m%d_%H%M%S).sql.gz
EOF

chmod +x ~/backup.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * ~/backup.sh") | crontab -
```

### Update Application
```bash
cd /opt/DigitalBusinessCard
git pull origin main
docker-compose restart
```

### Monitor Resources
```bash
# Real-time monitoring
watch -n 1 'docker stats --no-stream'

# Disk usage
df -h

# Check processes
htop
```

### SSL Auto-Renewal
```bash
# Already configured in Certbot
# Check renewal
sudo certbot renew --dry-run

# View renewal status
sudo systemctl status certbot.timer
```

---

## File Locations

| Path | Purpose |
|------|---------|
| `/opt/DigitalBusinessCard` | Application root |
| `.env.production` | Production config |
| `/etc/nginx/sites-available/digital-cards` | Nginx config |
| `/var/log/nginx/` | Nginx logs |
| `/opt/DigitalBusinessCard/backups/` | Database backups |
| `docker-compose.yml` | Docker configuration |
| `/etc/letsencrypt/live/` | SSL certificates |

---

## Performance Tips

1. **Enable Gzip in Nginx** - Already configured
2. **Use CDN** - Consider DigitalOcean Spaces
3. **Database Optimization** - Run `VACUUM ANALYZE;` regularly
4. **Monitor Disk** - Keep >20% free space
5. **Update Regularly** - Run `apt update && apt upgrade -y` monthly
6. **Backup Frequently** - Automate daily backups
7. **Review Logs** - Check error logs weekly

---

## Security Checklist

- [ ] Change default database password
- [ ] Update JWT_SECRET to unique strong value
- [ ] Enable firewall
- [ ] Disable root SSH login
- [ ] Configure SSH keys
- [ ] Set up SSL/HTTPS
- [ ] Keep system updated
- [ ] Review access logs regularly
- [ ] Enable automatic security updates

```bash
# Enable auto-security updates
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## Support Resources

- **Detailed Guide:** Read `DIGITALOCEAN_DEPLOYMENT.md`
- **GitHub Repo:** https://github.com/ebra-hazard/DigitalBusinessCard
- **Docker Docs:** https://docs.docker.com
- **Nginx Docs:** https://nginx.org/en/docs/
- **Let's Encrypt:** https://letsencrypt.org/

---

**Notes:**
- All commands assume you're in `/opt/DigitalBusinessCard` directory
- Replace `YOUR_IP_OR_DOMAIN` with actual IP or domain
- Keep `.env.production` secure (don't commit to git)
- Backup database before making major changes
- Monitor logs regularly for errors
