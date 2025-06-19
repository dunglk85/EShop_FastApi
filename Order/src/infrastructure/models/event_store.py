import uuid
from datetime import datetime
from typing import Optional, Type
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy import Column, Integer, String, UniqueConstraint

from src.domain.event_map import EVENT_TYPE_MAPPING
from src.domain.abstraction.domain_event import IDomainEvent
from src.utils.serialization import convert_uuids

class EventStoreRecord(SQLModel, table=True):
    __tablename__ = "event_store"
    __table_args__ = (UniqueConstraint("aggregate_id", "version", name="uix_aggregate_version"),)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    aggregate_id: uuid.UUID = Field(index=True)
    aggregate_type: str
    event_type: str
    payload: dict = Field(sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.now)
    version: int

    @staticmethod
    def from_domain_event(event: BaseModel, aggregate_id: uuid.UUID, version: int) -> "EventStoreRecord":
        payload = event.model_dump() if hasattr(event, "model_dump") else event.dict()
        payload = convert_uuids(payload)
        return EventStoreRecord(
            aggregate_id=aggregate_id,
            aggregate_type=getattr(event, "aggregate_type", type(event).__name__),
            event_type=type(event).__name__,
            payload=payload,
            version=version
        )

    @staticmethod
    def to_domain_event(record: "EventStoreRecord") -> BaseModel:
        event_cls: Type[BaseModel] = EVENT_TYPE_MAPPING.get(record.event_type)
        if not event_cls:
            raise ValueError(f"Unknown event type: {record.event_type}")
        return event_cls(**record.payload)
