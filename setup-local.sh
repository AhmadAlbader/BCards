#!/bin/bash

# 🚀 BCards - Quick Local Setup Script
# يقوم بتجهيز وتشغيل المشروع بالكامل

set -e

echo "🎯 BCards - Local Development Setup"
echo "===================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker
echo "📦 Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker found${NC}"

# Check .env
echo ""
echo "🔧 Checking .env file..."
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "Creating from example..."
    
    cat > .env << 'EOF'
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@postgres:5432/digital_cards
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=digital_cards

# Security
SECRET_KEY=dev_f8k2m9p4n7q1s6t3v8w2x5y9z4a7b2c6d1e4f8g3h7j2k6m1n5p9r4s8t3u7v2w6x1
ENVIRONMENT=development

# Stripe (Test Mode)
STRIPE_SECRET_KEY=sk_test_your_test_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_test_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Frontend
FRONTEND_URL=http://localhost:3000

# Subscription Configuration
FREE_PLAN_EMPLOYEE_LIMIT=2
DEFAULT_TRIAL_DAYS=3
SUPPORTED_CURRENCIES=USD,KWD

# CORS
CORS_ORIGINS=http://localhost:3000,http://192.168.0.229:3000

# Network
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=3000
EOF
    
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Remember to add your Stripe keys!${NC}"
else
    echo -e "${GREEN}✅ .env file exists${NC}"
fi

# Check frontend .env.local
echo ""
echo "🔧 Checking frontend .env.local..."
if [ ! -f frontend/.env.local ]; then
    echo "Creating frontend/.env.local..."
    
    cat > frontend/.env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_test_publishable_key_here
EOF
    
    echo -e "${GREEN}✅ frontend/.env.local created${NC}"
else
    echo -e "${GREEN}✅ frontend/.env.local exists${NC}"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."

# Backend
echo "Installing backend dependencies..."
cd backend
if command -v poetry &> /dev/null; then
    poetry install
else
    echo -e "${YELLOW}Poetry not found, using pip...${NC}"
    pip install -r requirements.txt || pip install -e .
fi
cd ..
echo -e "${GREEN}✅ Backend dependencies installed${NC}"

# Frontend
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..
echo -e "${GREEN}✅ Frontend dependencies installed${NC}"

# Build and start containers
echo ""
echo "🐳 Starting Docker containers..."
docker-compose up -d

# Wait for database
echo ""
echo "⏳ Waiting for database..."
sleep 5

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
python migrate_subscriptions.py

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "🌐 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Next steps:"
echo "   1. Add your Stripe API keys to .env and frontend/.env.local"
echo "   2. Create Products in Stripe Dashboard"
echo "   3. Update Price IDs in backend/subscription_config.py"
echo "   4. Test with: http://localhost:3000/pricing"
echo ""
echo "🛑 To stop: docker-compose down"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
