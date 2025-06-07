from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
import json


class EventRecord(SQLModel, table=True):
    __tablename__ = "event_store"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    aggregate_id: str = Field(index=True)
    aggregate_type: str
    event_type: str
    event_data: dict
    occurred_on: datetime = Field(default_factory=datetime.now)
