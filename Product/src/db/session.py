from sqlmodel import SQLModel
from sqlalchemy import event
from datetime import datetime, timezone
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")  # Change this to your database URL
engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@event.listens_for(SQLModel, "before_insert", propagate=True)
def set_created_updated_timestamps(mapper, connection, target):
    now = datetime.now(timezone.utc)
    if hasattr(target, "created_at") and not target.created_at:
        target.created_at = now
    if hasattr(target, "updated_at"):
        target.updated_at = now

@event.listens_for(SQLModel, "before_update", propagate=True)
def set_updated_timestamp(mapper, connection, target):
    if hasattr(target, "updated_at"):
        target.updated_at = datetime.now(timezone.utc)