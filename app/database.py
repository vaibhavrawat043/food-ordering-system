from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from app.config import settings

# Async database setup
async_engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# Sync database setup (for testing)
sync_engine = create_engine(settings.DATABASE_URL.replace("+asyncpg", ""), echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

Base = declarative_base()

async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session

# Synchronous version for testing
def get_sync_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()