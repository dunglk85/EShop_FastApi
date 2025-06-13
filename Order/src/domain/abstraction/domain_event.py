from abc import ABC
from uuid import UUID, uuid4
from datetime import datetime


class IDomainEvent(ABC):
    @property
    def id(self) -> UUID:
        return uuid4()

    @property
    def occurred_on(self) -> datetime:
        return datetime.now()

    @property
    def event_type(self) -> str:
        return f"{self.__class__.__module__}.{self.__class__.__qualname__}"

class IntegrationEvent(IDomainEvent):
    is_integration_event = True