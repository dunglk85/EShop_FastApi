# infrastructure/event_store/models.py
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base

from domain.abstraction.domain_event import IDomainEvent  # You should define a base class
from utils.serialization import serialize_event, deserialize_event  # custom helpers

Base = declarative_base()


class EventStoreRecord(Base):
    __tablename__ = "event_store"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aggregate_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    aggregate_type = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    version = Column(int, nullable=False)

    @staticmethod
    def from_domain_event(event: IDomainEvent, aggregate_id: uuid.UUID) -> "EventStoreRecord":
        return EventStoreRecord(
            aggregate_id=aggregate_id,
            aggregate_type=event.aggregate_type,
            event_type=event.__class__.__name__,
            payload=serialize_event(event)
        )

    @staticmethod
    def to_domain_event(record: "EventStoreRecord") -> IDomainEvent:
        return deserialize_event(record.event_type, record.payload)
