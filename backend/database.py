import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator

# Get DATABASE_URL from environment and convert to asyncpg format
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost:5432/digital_cards"
)

# Railway provides postgres:// but we need postgresql+asyncpg://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

print(f"🔗 Connecting to database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'localhost'}")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to False in production to reduce logs
    future=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_db() -> AsyncGenerator:
    """Dependency injection for database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Create all database tables with retry logic."""
    max_retries = 30  # Increased retries for Railway startup
    retry_delay = 3  # seconds
    
    print("🚀 Starting up... initializing database")
    
    for attempt in range(max_retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ Database initialized successfully")
            return
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⏳ Database connection attempt {attempt + 1}/{max_retries} failed: {e}")
                print(f"   Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                print(f"❌ Failed to initialize database after {max_retries} attempts")
                print(f"   Last error: {e}")
                raise


async def drop_db():
    """Drop all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
