from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Type, cast
import datetime

from src.domain.abstraction.entity import IEntityWithId
from src.domain.abstraction.domain_event import IDomainEvent

T = TypeVar("T")  # ID type
TAggregate = TypeVar("TAggregate", bound="Aggregate")

class IAggregateId(IEntityWithId[T], ABC):
    pass

class Aggregate(IAggregateId[T], ABC):

    def __init__(
        self,
        id: T,
        created_by: Optional[str] = None,
        last_modified_by: Optional[str] = None,
    ):
        self._id: T = id
        self.created_at: datetime.datetime = datetime.datetime.now()
        self.created_by: Optional[str] = created_by
        self.last_modified: datetime.datetime = datetime.datetime.now()
        self.last_modified_by: Optional[str] = last_modified_by
        self._domain_events: List[IDomainEvent] = []

    @property
    def id(self) -> T:
        return self._id

    @property
    def domain_events(self) -> List[IDomainEvent]:
        return list(self._domain_events)

    def add_domain_event(self, event: IDomainEvent) -> None:
        self._domain_events.append(event)

    def clear_domain_events(self) -> List[IDomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events

    def apply(self, event: IDomainEvent):
        """Dynamically call the corresponding _apply_<EventName> method."""
        method = f"_apply_{type(event).__name__}"
        if hasattr(self, method):
            getattr(self, method)(event)

    def raise_event(self, event: IDomainEvent):
        self.apply(event)
        self.add_domain_event(event)

    @classmethod
    def rehydrate(cls: Type[TAggregate], id: T , events: List[object]) -> TAggregate:
        """Factory-safe rehydration method for any Aggregate subclass."""
        instance = cls.__new__(cls)
        cls.__allow_init = True
        instance.__init__(id)
        cls.__allow_init = False

        for event in events:
            instance.apply(event)

        return instance
