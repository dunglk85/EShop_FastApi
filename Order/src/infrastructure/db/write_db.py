# src/infrastructure/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from sqlmodel import SQLModel

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/orderdb")

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,          # number of persistent connections
    max_overflow=20,       # extra connections beyond pool_size
    pool_timeout=30,       # timeout for getting a connection
    pool_recycle=1800,     # close & reopen connections after 30 min
    echo=False             # set True to log SQL (for debugging)
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
Base = declarative_base()

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)