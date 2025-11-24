# Environment Configuration Guide

## Environment Files Overview

This project uses environment-based configuration to work seamlessly across development, staging, and production environments.

### File Structure

```
.env.local              # Local overrides (NOT committed - personal machine)
.env.development        # Development defaults (committed)
.env.production.template # Production template (committed as reference)
.env.production         # Actual production values (NOT committed - server only)
```

### Priority Order (loaded in this order, later overrides earlier)

1. Default values in code
2. `.env.development`
3. `.env.production` (on production server)
4. `.env.local` (on your local machine)

## Environment Variables

### Frontend Variables (NEXT_PUBLIC_*)

```
NEXT_PUBLIC_API_URL     # Backend API base URL (e.g., https://api.yourdomain.com)
NEXT_PUBLIC_APP_URL     # Frontend app URL (e.g., https://yourdomain.com)
```

### Backend Variables

```
API_HOST                # IP or domain where backend runs
API_PORT                # Port number (3000 for frontend, 8000 for backend)
FRONTEND_HOST           # Where frontend is hosted
FRONTEND_PORT           # Frontend port
DATABASE_URL            # PostgreSQL connection string
SECRET_KEY              # JWT secret (use strong random string)
DEBUG                   # Set to false in production
ENVIRONMENT             # 'development', 'staging', or 'production'
```

### Security Variables

```
CORS_ORIGINS            # Allowed origins for CORS (comma-separated)
ALLOWED_HOSTS           # Allowed hostnames
SSL_ENABLED             # Enable HTTPS
SSL_CERT_PATH           # Path to SSL certificate
SSL_KEY_PATH            # Path to SSL key
```

## Setup Instructions

### 1. Local Development

```bash
# File already created: .env.local
# Update with your machine's IP if different
NEXT_PUBLIC_API_URL=http://192.168.1.123:8000/api
NEXT_PUBLIC_APP_URL=http://192.168.1.123:3000
```

### 2. Production (DigitalOcean)

On your DigitalOcean Droplet:

```bash
# Create production env file
cd /app/digital-business-cards
cp .env.production.template .env.production

# Edit with your values
nano .env.production

# Update these with your domain:
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
NEXT_PUBLIC_APP_URL=https://yourdomain.com
API_HOST=yourdomain.com
...
```

### 3. Docker-Compose with Environment Files

The `docker-compose.yml` reads from `.env` by default.

To use different environments:

```bash
# Development (default)
docker-compose up -d

# Production (on server with .env.production)
docker-compose up -d
```

## Important Notes

⚠️ **NEVER commit to git:**
- `.env.local`
- `.env.production`
- Any file with actual secrets

✅ **Safe to commit:**
- `.env.development`
- `.env.production.template` (as reference only)
- `.gitignore` (ensures .env files are not committed)

## Generating Secret Keys

```bash
# For SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Or using OpenSSL
openssl rand -base64 32
```

## Development Workflow

1. **Local development**: Uses `.env.local` + `.env.development`
2. **Push to GitHub**: Code only, no .env files
3. **Pull on server**: Uses `.env.production` (created manually on server)
4. **Deploy**: Docker uses the environment file automatically

## Testing Your Configuration

```bash
# Check which environment is active
echo $ENVIRONMENT

# Test database connection
python3 -c "from backend.database import engine; print('Database connection OK')"

# Test frontend can reach API
curl $NEXT_PUBLIC_API_URL/docs
```

## Troubleshooting

If the app uses old URLs:
1. Verify `.env.local` or `.env.production` exists
2. Restart Docker: `docker-compose down && docker-compose up -d`
3. Check logs: `docker logs digital-cards-backend`
4. Confirm env vars in container: `docker exec digital-cards-backend printenv | grep API`
