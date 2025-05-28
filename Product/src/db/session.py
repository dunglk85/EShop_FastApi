from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy import event
from datetime import datetime, timezone
import os

DATABASE_URL = os.getenv("DATABASE_URL")  # Change this to your database URL
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

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