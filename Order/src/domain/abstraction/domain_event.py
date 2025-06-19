from abc import ABC
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field
from typing import ClassVar


class IDomainEvent(BaseModel, ABC):
    id: UUID = Field(default_factory=uuid4)
    occurred_on: datetime = Field(default_factory=datetime.now())

    @property
    def aggregate_type(self) -> str:
        return self.__class__.__module__.split('.')[2]  # e.g. from `src.domain.order.events`

    @property
    def event_type(self) -> str:
        return f"{self.__class__.__module__}.{self.__class__.__qualname__}"

class IntegrationEvent(IDomainEvent):
    is_integration_event: ClassVar[bool] = True