#!/bin/bash

################################################################################
# Digital Business Cards - Automated Deployment Script for DigitalOcean Ubuntu
# This script automates the deployment process
################################################################################

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions for logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root or with sudo
if [[ $EUID -ne 0 ]]; then
   log_error "This script must be run as root or with sudo"
   exit 1
fi

log_info "=========================================="
log_info "Digital Business Cards - Deployment Script"
log_info "=========================================="

# Step 1: Update System
log_info "Step 1: Updating system packages..."
apt update && apt upgrade -y
log_success "System packages updated"

# Step 2: Install Docker
log_info "Step 2: Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    usermod -aG docker $SUDO_USER
    log_success "Docker installed"
else
    log_warning "Docker already installed"
fi

# Step 3: Install Docker Compose
log_info "Step 3: Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    log_success "Docker Compose installed"
else
    log_warning "Docker Compose already installed"
fi

# Step 4: Install Git
log_info "Step 4: Installing Git..."
if ! command -v git &> /dev/null; then
    apt install -y git
    log_success "Git installed"
else
    log_warning "Git already installed"
fi

# Step 5: Install Nginx
log_info "Step 5: Installing Nginx..."
if ! command -v nginx &> /dev/null; then
    apt install -y nginx
    systemctl start nginx
    systemctl enable nginx
    log_success "Nginx installed and started"
else
    log_warning "Nginx already installed"
fi

# Step 6: Install Certbot for SSL
log_info "Step 6: Installing Certbot..."
if ! command -v certbot &> /dev/null; then
    apt install -y certbot python3-certbot-nginx
    log_success "Certbot installed"
else
    log_warning "Certbot already installed"
fi

# Step 7: Clone Repository
log_info "Step 7: Cloning repository..."
if [ ! -d "/opt/DigitalBusinessCard" ]; then
    mkdir -p /opt
    cd /opt
    git clone https://github.com/ebra-hazard/DigitalBusinessCard.git
    chown -R $SUDO_USER:$SUDO_USER /opt/DigitalBusinessCard
    log_success "Repository cloned"
else
    log_warning "Repository already exists"
fi

# Step 8: Create environment file
log_info "Step 8: Creating environment configuration..."

# Ask for domain/IP
read -p "Enter your domain or server IP (for CORS and API configuration): " DOMAIN_OR_IP
read -p "Enter your SMTP email address (for password reset, leave blank to skip): " SMTP_EMAIL
read -p "Enter your SMTP password/app password (leave blank to skip): " SMTP_PASSWORD

# Generate JWT Secret
JWT_SECRET=$(openssl rand -base64 32)

cd /opt/DigitalBusinessCard

# Create .env.production file
cat > .env.production << EOF
# Backend Configuration
API_HOST=$DOMAIN_OR_IP
API_PORT=8000
FRONTEND_HOST=$DOMAIN_OR_IP
FRONTEND_PORT=443
ENVIRONMENT=production

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/digital_cards
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=digital_cards

# CORS and Allowed Hosts
CORS_ORIGINS=https://$DOMAIN_OR_IP,https://www.$DOMAIN_OR_IP,http://localhost:3000
ALLOWED_HOSTS=$DOMAIN_OR_IP,www.$DOMAIN_OR_IP,localhost

# Frontend Public API Configuration
NEXT_PUBLIC_API_HOST=$DOMAIN_OR_IP
NEXT_PUBLIC_API_PORT=443

# JWT Secret
JWT_SECRET=$JWT_SECRET

# Email Configuration (optional for password reset)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=$SMTP_EMAIL
SMTP_PASSWORD=$SMTP_PASSWORD
SMTP_FROM=$SMTP_EMAIL
EOF

chmod 600 .env.production
log_success "Environment file created at /opt/DigitalBusinessCard/.env.production"

# Step 9: Configure Nginx
log_info "Step 9: Configuring Nginx..."

# Backup original nginx config
if [ -f /etc/nginx/sites-available/digital-cards ]; then
    cp /etc/nginx/sites-available/digital-cards /etc/nginx/sites-available/digital-cards.backup
fi

cat > /etc/nginx/sites-available/digital-cards << EOF
upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name $DOMAIN_OR_IP;
    
    # Redirect HTTP to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN_OR_IP;

    # SSL Configuration (temporary self-signed, will be replaced by Let's Encrypt)
    ssl_certificate /etc/nginx/ssl/self-signed.crt;
    ssl_certificate_key /etc/nginx/ssl/self-signed.key;
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
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }

    # API Backend
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
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

# Create self-signed certificate if it doesn't exist
if [ ! -d /etc/nginx/ssl ]; then
    mkdir -p /etc/nginx/ssl
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/ssl/self-signed.key \
        -out /etc/nginx/ssl/self-signed.crt \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN_OR_IP"
fi

# Enable the site
ln -sf /etc/nginx/sites-available/digital-cards /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test and restart Nginx
nginx -t && systemctl restart nginx
log_success "Nginx configured"

# Step 10: Build and start Docker containers
log_info "Step 10: Building and starting Docker containers..."
cd /opt/DigitalBusinessCard
docker-compose -f docker-compose.yml down 2>/dev/null || true
docker-compose -f docker-compose.yml up -d
log_success "Docker containers started"

# Step 11: Wait for database initialization
log_info "Step 11: Waiting for database initialization..."
sleep 15

# Step 12: Initialize database
log_info "Step 12: Initializing database..."
docker-compose exec -T postgres psql -U postgres -c "CREATE DATABASE digital_cards;" 2>/dev/null || true
log_success "Database initialized"

# Step 13: Set up SSL with Let's Encrypt
log_info "Step 13: SSL Certificate Setup"
read -p "Do you have a domain name for SSL setup? (y/n): " HAS_DOMAIN

if [ "$HAS_DOMAIN" = "y" ] || [ "$HAS_DOMAIN" = "Y" ]; then
    read -p "Enter your domain name (e.g., example.com): " DOMAIN_NAME
    read -p "Enter your email for Let's Encrypt: " LE_EMAIL
    
    log_info "Setting up SSL certificate with Let's Encrypt..."
    certbot certonly --standalone -d $DOMAIN_NAME -d www.$DOMAIN_NAME -m $LE_EMAIL --agree-tos --non-interactive
    
    # Update Nginx config with real certificate
    sed -i "s|ssl_certificate /etc/nginx/ssl/self-signed.crt;|ssl_certificate /etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem;|g" /etc/nginx/sites-available/digital-cards
    sed -i "s|ssl_certificate_key /etc/nginx/ssl/self-signed.key;|ssl_certificate_key /etc/letsencrypt/live/$DOMAIN_NAME/privkey.pem;|g" /etc/nginx/sites-available/digital-cards
    
    nginx -t && systemctl restart nginx
    log_success "SSL certificate installed"
else
    log_warning "Skipping Let's Encrypt setup. Using self-signed certificate."
fi

# Step 14: Set up firewall
log_info "Step 14: Configuring firewall..."
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
log_success "Firewall configured"

# Step 15: Set up automatic backups
log_info "Step 15: Setting up automatic database backups..."
mkdir -p /opt/DigitalBusinessCard/backups

cat > /usr/local/bin/backup-digital-cards.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/DigitalBusinessCard/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

docker-compose -f /opt/DigitalBusinessCard/docker-compose.yml exec -T postgres pg_dump -U postgres digital_cards | gzip > $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz

# Keep only last 7 backups
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete

echo "Database backed up to $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz"
EOF

chmod +x /usr/local/bin/backup-digital-cards.sh

# Add to crontab for daily backups at 2 AM
(crontab -l 2>/dev/null | grep -v backup-digital-cards; echo "0 2 * * * /usr/local/bin/backup-digital-cards.sh") | crontab -
log_success "Automatic backups configured"

# Step 16: Final verification
log_info "Step 16: Verifying installation..."
log_info "Checking Docker containers..."
docker-compose -f /opt/DigitalBusinessCard/docker-compose.yml ps

log_info "Checking Nginx status..."
systemctl status nginx --no-pager | head -5

# Summary
log_success "=========================================="
log_success "Deployment completed successfully!"
log_success "=========================================="

echo ""
echo "Configuration Summary:"
echo "====================="
echo "Domain/IP: $DOMAIN_OR_IP"
echo "Application URL: https://$DOMAIN_OR_IP"
echo "API URL: https://$DOMAIN_OR_IP/api"
echo "Docker Compose Location: /opt/DigitalBusinessCard"
echo "Environment File: /opt/DigitalBusinessCard/.env.production"
echo "Nginx Config: /etc/nginx/sites-available/digital-cards"
echo "Backup Location: /opt/DigitalBusinessCard/backups"
echo ""
echo "Useful Commands:"
echo "================"
echo "View logs: docker-compose -f /opt/DigitalBusinessCard/docker-compose.yml logs -f"
echo "Restart services: docker-compose -f /opt/DigitalBusinessCard/docker-compose.yml restart"
echo "Check status: docker-compose -f /opt/DigitalBusinessCard/docker-compose.yml ps"
echo "Manual backup: /usr/local/bin/backup-digital-cards.sh"
echo ""

log_info "Next Steps:"
log_info "1. Update .env.production with your actual database password"
log_info "2. If using a domain, update the JWT_SECRET to something unique"
log_info "3. Configure email settings for password reset feature (optional)"
log_info "4. Monitor logs for any errors: docker-compose logs -f"
echo ""
