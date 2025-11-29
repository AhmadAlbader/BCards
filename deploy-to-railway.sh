#!/bin/bash

# ================================
# BCards - Railway Deployment Script
# ================================
# هذا السكريبت ينشر المشروع على Railway بشكل آمن
# لن يؤثر على المشاريع الأخرى

set -e  # Exit on error

echo "🚀 بدء نشر BCards على Railway..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo -e "${YELLOW}⚠️  Railway CLI غير مثبت${NC}"
    echo ""
    echo "تثبيت Railway CLI..."
    echo ""
    
    # Install Railway CLI
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install railway
    else
        # Linux or other
        npm i -g @railway/cli
    fi
    
    echo -e "${GREEN}✅ تم تثبيت Railway CLI${NC}"
    echo ""
fi

# Login to Railway
echo -e "${BLUE}🔐 تسجيل الدخول إلى Railway...${NC}"
echo ""
railway login

echo ""
echo -e "${GREEN}✅ تم تسجيل الدخول بنجاح${NC}"
echo ""

# Create new project
echo -e "${BLUE}📦 إنشاء مشروع جديد: BCards SaaS${NC}"
echo ""
echo "⚠️  هذا سينشئ مشروع جديد منفصل تماماً عن المشاريع الأخرى"
echo ""
read -p "هل تريد المتابعة؟ (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ تم الإلغاء${NC}"
    exit 1
fi

# Initialize Railway project
railway init

echo ""
echo -e "${GREEN}✅ تم إنشاء المشروع${NC}"
echo ""

# Link to GitHub repo
echo -e "${BLUE}🔗 ربط بـ GitHub Repository...${NC}"
echo ""
railway link

echo ""
echo -e "${GREEN}✅ تم الربط بـ GitHub${NC}"
echo ""

# Add PostgreSQL database
echo -e "${BLUE}🗄️  إضافة PostgreSQL Database...${NC}"
echo ""
railway add postgresql

echo ""
echo -e "${GREEN}✅ تم إضافة Database${NC}"
echo ""

# Generate SECRET_KEY
echo -e "${BLUE}🔑 توليد SECRET_KEY...${NC}"
SECRET_KEY=$(openssl rand -base64 64 | tr -d '\n')
echo -e "${GREEN}✅ تم توليد SECRET_KEY${NC}"
echo ""

# Prompt for Stripe keys
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📝 الآن، أدخل معلومات Stripe:${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "يمكنك استخدام Test Keys أو Live Keys"
echo "احصل عليها من: https://dashboard.stripe.com/apikeys"
echo ""

read -p "Stripe Secret Key (sk_test_... أو sk_live_...): " STRIPE_SECRET_KEY
read -p "Stripe Publishable Key (pk_test_... أو pk_live_...): " STRIPE_PUBLISHABLE_KEY

echo ""
echo -e "${BLUE}📋 إضافة Environment Variables...${NC}"
echo ""

# Set backend environment variables
railway variables set \
  SECRET_KEY="$SECRET_KEY" \
  STRIPE_SECRET_KEY="$STRIPE_SECRET_KEY" \
  STRIPE_PUBLISHABLE_KEY="$STRIPE_PUBLISHABLE_KEY" \
  FRONTEND_URL="https://digitalbc.sword-academy.net" \
  CORS_ORIGINS="https://digitalbc.sword-academy.net" \
  ALLOWED_HOSTS="digitalbc.sword-academy.net,api.digitalbc.sword-academy.net" \
  ENVIRONMENT="production" \
  DEBUG="false" \
  DEFAULT_TRIAL_DAYS="3" \
  FREE_PLAN_EMPLOYEE_LIMIT="2" \
  PRO_PLAN_EMPLOYEE_LIMIT="50" \
  ENTERPRISE_PLAN_EMPLOYEE_LIMIT="999999" \
  PRO_PLAN_PRICE_USD="29.00" \
  ENTERPRISE_PLAN_PRICE_USD="99.00" \
  PRO_PLAN_PRICE_KWD="8.90" \
  ENTERPRISE_PLAN_PRICE_KWD="30.50" \
  DEFAULT_CURRENCY="USD" \
  SUPPORTED_CURRENCIES="USD,KWD"

echo ""
echo -e "${GREEN}✅ تم إضافة Environment Variables${NC}"
echo ""

# Deploy
echo -e "${BLUE}🚀 بدء النشر...${NC}"
echo ""
echo "سيتم نشر Backend و Frontend..."
echo ""

railway up

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ تم النشر بنجاح!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Get the deployment URL
echo -e "${BLUE}🌐 الحصول على URLs...${NC}"
echo ""
BACKEND_URL=$(railway status | grep -o 'https://[^ ]*' | head -1)

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}📊 معلومات النشر:${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Backend URL (مؤقت): $BACKEND_URL"
echo ""
echo -e "${YELLOW}الخطوات التالية:${NC}"
echo ""
echo "1️⃣  إضافة Custom Domain للـ Backend:"
echo "   - اذهب لـ Railway Dashboard"
echo "   - Backend Service → Settings → Domains"
echo "   - أضف: api.digitalbc.sword-academy.net"
echo ""
echo "2️⃣  إضافة Custom Domain للـ Frontend:"
echo "   - Frontend Service → Settings → Domains"
echo "   - أضف: digitalbc.sword-academy.net"
echo ""
echo "3️⃣  تحديث DNS في Hostinger (راجع HOSTINGER_DNS_GUIDE.md)"
echo ""
echo "4️⃣  إضافة Stripe Webhook (راجع STRIPE_WEBHOOK_SETUP.md)"
echo "   URL: https://api.digitalbc.sword-academy.net/api/webhooks/stripe"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "للمتابعة، افتح: RAILWAY_QUICK_DEPLOY.md"
echo ""
