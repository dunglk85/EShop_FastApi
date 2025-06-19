import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column
from src.domain.abstraction.domain_event import IDomainEvent
from src.utils.serialization import serialize_event, convert_uuids


class OutboxEventRecord(SQLModel, table=True):
    __tablename__ = "outbox"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    aggregate_id: uuid.UUID = Field(index=True)
    aggregate_type: str
    event_type: str
    payload: Dict[str, Any] = Field(sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4, index=True)
    published: bool = Field(default=False, nullable=False)

    @staticmethod
    def from_domain_event(event: IDomainEvent, aggregate_id: uuid.UUID) -> "OutboxEventRecord":
        payload = event.model_dump() if hasattr(event, "model_dump") else event.dict()
        payload = convert_uuids(payload)
        return OutboxEventRecord(
            aggregate_id=aggregate_id,
            aggregate_type=event.aggregate_type,
            event_type=event.__class__.__name__,
            payload=payload,
            event_id=getattr(event, "event_id", uuid.uuid4())
        )
