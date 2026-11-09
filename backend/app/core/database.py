"""Database session management"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import logging
import os

logger = logging.getLogger(__name__)

# Use SQLite for simplicity
if settings.database_url.startswith("sqlite"):
    # SQLite configuration
    async_database_url = settings.database_url.replace("sqlite:///", "sqlite+aiosqlite:///")
    sync_database_url = settings.database_url
    
    async_engine = create_async_engine(
        async_database_url,
        echo=settings.debug,
        future=True,
        connect_args={"check_same_thread": False}
    )
    
    sync_engine = create_engine(
        sync_database_url,
        echo=settings.debug,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL configuration (fallback)
    async_database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
    sync_database_url = settings.database_url.replace("postgresql://", "postgresql+psycopg2://")
    
    async_engine = create_async_engine(
        async_database_url,
        echo=settings.debug,
        future=True,
        pool_pre_ping=True,
        pool_recycle=300,
    )
    
    sync_engine = create_engine(
        sync_database_url,
        echo=settings.debug,
        pool_pre_ping=True,
    )

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create sync session factory
SessionLocal = sessionmaker(bind=sync_engine)


async def get_db_session() -> AsyncSession:
    """Dependency to get a database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db_session():
    """Get a synchronous database session"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()