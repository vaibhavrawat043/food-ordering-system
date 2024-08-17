import asyncio
from app.database import async_engine as engine, Base
from app.models import Restaurant, MenuItem, Order, OrderItem  # Import all models

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())