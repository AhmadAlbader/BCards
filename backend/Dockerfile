FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/pyproject.toml* ./

# Install Python dependencies
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

# Copy application code
COPY backend/ ./

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/api/health')"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
