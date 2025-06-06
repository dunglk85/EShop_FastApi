from abc import ABC
from uuid import UUID, uuid4
from datetime import datetime


class IDomainEvent(ABC):
    @property
    def event_id(self) -> UUID:
        return uuid4()

    @property
    def occurred_on(self) -> datetime:
        return datetime.utcnow()

    @property
    def event_type(self) -> str:
        return f"{self.__class__.__module__}.{self.__class__.__qualname__}"
