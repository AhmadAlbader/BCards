#!/bin/bash
# ============================================
# Setup script for configuring environment for any IP/network
# ============================================

set -e

echo "🔧 Digital Business Cards - Environment Setup"
echo "============================================"
echo ""

# Function to get machine IP
get_machine_ip() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1
  elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    hostname -I | awk '{print $1}'
  else
    echo "localhost"
  fi
}

# Get current IP
CURRENT_IP=$(get_machine_ip)

echo "📍 Detected your machine IP: $CURRENT_IP"
echo ""

# Check if user wants to override
read -p "Press Enter to use this IP, or enter a different one: " USER_IP

if [ -z "$USER_IP" ]; then
  MACHINE_IP=$CURRENT_IP
else
  MACHINE_IP=$USER_IP
fi

echo "✓ Using IP: $MACHINE_IP"
echo ""

# Update .env (docker-compose reads this by default)
echo "📝 Updating .env file..."

if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS version of sed
  sed -i '' "s/CORS_ORIGINS=.*/CORS_ORIGINS=http:\/\/localhost:3000,http:\/\/localhost:8000,http:\/\/127.0.0.1:3000,http:\/\/127.0.0.1:8000,http:\/\/$MACHINE_IP:3000,http:\/\/$MACHINE_IP:8000/" .env
  sed -i '' "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=localhost,127.0.0.1,$MACHINE_IP/" .env
  sed -i '' "s/NEXT_PUBLIC_API_URL=.*/NEXT_PUBLIC_API_URL=http:\/\/$MACHINE_IP:8000\/api/" .env
  sed -i '' "s/NEXT_PUBLIC_APP_URL=.*/NEXT_PUBLIC_APP_URL=http:\/\/$MACHINE_IP:3000/" .env
  sed -i '' "s/API_HOST=.*/API_HOST=$MACHINE_IP/" .env
  sed -i '' "s/FRONTEND_HOST=.*/FRONTEND_HOST=$MACHINE_IP/" .env
else
  # Linux version of sed
  sed -i "s/CORS_ORIGINS=.*/CORS_ORIGINS=http:\/\/localhost:3000,http:\/\/localhost:8000,http:\/\/127.0.0.1:3000,http:\/\/127.0.0.1:8000,http:\/\/$MACHINE_IP:3000,http:\/\/$MACHINE_IP:8000/" .env
  sed -i "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=localhost,127.0.0.1,$MACHINE_IP/" .env
  sed -i "s/NEXT_PUBLIC_API_URL=.*/NEXT_PUBLIC_API_URL=http:\/\/$MACHINE_IP:8000\/api/" .env
  sed -i "s/NEXT_PUBLIC_APP_URL=.*/NEXT_PUBLIC_APP_URL=http:\/\/$MACHINE_IP:3000/" .env
  sed -i "s/API_HOST=.*/API_HOST=$MACHINE_IP/" .env
  sed -i "s/FRONTEND_HOST=.*/FRONTEND_HOST=$MACHINE_IP/" .env
fi

echo "✓ Updated .env with IP: $MACHINE_IP"
echo ""

echo "✅ Environment configuration complete!"
echo ""
echo "📋 Summary:"
echo "   • Machine IP: $MACHINE_IP"
echo "   • Frontend: http://$MACHINE_IP:3000"
echo "   • Backend API: http://$MACHINE_IP:8000/api"
echo "   • File updated: .env"
echo ""
echo "🚀 Next steps:"
echo "   1. If using Docker: docker-compose down && docker-compose up -d"
echo "   2. If running locally: npm run dev (frontend) & python -m uvicorn backend.main:app --reload (backend)"
echo ""
echo "⚠️  If changing networks:"
echo "   1. Run this script again with your new IP"
echo "   2. Restart your services"
echo ""
