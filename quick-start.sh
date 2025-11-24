#!/bin/bash
set -e

echo "🚀 Digital Business Cards SaaS - Quick Start Script"
echo "=================================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✅ Docker found"
echo ""

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env created (update with your settings)"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🐳 Starting Docker Compose services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "✅ Services are running!"
echo ""
echo "📚 Access points:"
echo "   - Frontend:    http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs:    http://localhost:8000/docs"
echo "   - Database:    postgres://localhost:5432/digital_cards"
echo ""
echo "🔑 Next steps:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Sign up with your email"
echo "   3. Add employees from the admin dashboard"
echo "   4. View public card at http://localhost:3000/card/{company_slug}/{employee_slug}"
echo ""
echo "💡 Useful commands:"
echo "   - View logs:           docker-compose logs -f"
echo "   - Stop services:       docker-compose down"
echo "   - Database shell:      docker-compose exec postgres psql -U postgres -d digital_cards"
echo "   - Backend shell:       docker-compose exec backend bash"
echo ""
echo "🎉 Happy carding!"
