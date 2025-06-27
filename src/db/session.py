# app/db/session.py

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings

# Create async engine for PostgreSQL
# echo=True is good for development to see SQL, set to False in production for performance
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, pool_pre_ping=True)

# Create an async session maker
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,  # Don't auto-commit transactions
    autoflush=False,  # Don't auto-flush changes
    bind=engine,  # Bind to the engine
    class_=AsyncSession,  # Use the async session class
    expire_on_commit=False,  # Important: prevents ORM objects from expiring after commit
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides an asynchronous database session.
    The session is automatically created, yielded, and then closed/rolled back
    after the request is processed, ensuring proper resource management.
    """
    async with AsyncSessionLocal() as session:
        yield session
