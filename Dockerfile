# ========================================
# Multi-stage Dockerfile: Backend + Frontend
# ========================================

# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ ./
RUN npm run build

# Stage 2: Backend with Node.js for Frontend
FROM python:3.11-slim

# Install Node.js and system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    postgresql-client \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies (Backend)
COPY backend/pyproject.toml* ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-dev 2>/dev/null || \
    pip install --no-cache-dir \
        fastapi==0.104.0 \
        uvicorn[standard]==0.24.0 \
        sqlalchemy==2.0.23 \
        asyncpg==0.29.0 \
        pydantic==2.5.0 \
        pydantic-settings==2.1.0 \
        python-dotenv==1.0.0 \
        python-jose[cryptography]==3.3.0 \
        passlib[bcrypt]==1.7.4 \
        python-multipart==0.0.6 \
        email-validator==2.1.0 \
        python-slugify==8.0.1 \
        httpx==0.25.2 \
        stripe==7.8.0

# Copy Backend files
COPY backend/ ./backend/

# Copy Frontend build from stage 1
COPY --from=frontend-builder /frontend/.next ./frontend/.next
COPY --from=frontend-builder /frontend/public ./frontend/public
COPY --from=frontend-builder /frontend/node_modules ./frontend/node_modules
COPY --from=frontend-builder /frontend/package.json ./frontend/package.json
COPY --from=frontend-builder /frontend/next.config.js ./frontend/next.config.js

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "🚀 Starting Backend..."\n\
cd /app/backend && uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
echo "🎨 Starting Frontend..."\n\
cd /app/frontend && npm start -- -p 3000 &\n\
wait -n\n\
exit $?\n\
' > /start.sh && chmod +x /start.sh

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

USER appuser

# Railway will use PORT environment variable
EXPOSE 8000 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

CMD ["/start.sh"]
