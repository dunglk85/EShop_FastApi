import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base

from domain.abstraction.domain_event import IntegrationEvent
from utils.serialization import serialize_event  # shared with event store

Base = declarative_base()


class OutboxEventRecord(Base):
    __tablename__ = "outbox"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aggregate_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    aggregate_type = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    processed_at = Column(DateTime, nullable=True)
    event_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    @staticmethod
    def from_integration_event(event: IntegrationEvent, aggregate_id: uuid.UUID) -> "OutboxEventRecord":
        return OutboxEventRecord(
            aggregate_id=aggregate_id,
            aggregate_type=event.aggregate_type,
            event_type=event.__class__.__name__,
            payload=serialize_event(event)
        )