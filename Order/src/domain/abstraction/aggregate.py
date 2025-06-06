from abc import ABC, abstractmethod
from typing import Optional, TypeVar, List
from domain.abstraction.entity import IEntity, IEntityWithId
from domain.abstraction.domain_event import IDomainEvent
import datetime

T = TypeVar("T")

class IAggregate(IEntity, ABC):
    @property
    @abstractmethod
    def domain_events(self) -> List[IDomainEvent]:
        """Returns the list of domain events."""
        pass

    @abstractmethod
    def clear_domain_events(self) -> List[IDomainEvent]:
        pass
    
class IAggregateId(IAggregate, IEntityWithId[T], ABC):
    pass

class Aggregate(IAggregateId[T], ABC):
    def __init__(
        self,
        id: T,
        created_by: Optional[str] = None,
        last_modified_by: Optional[str] = None,
    ):
        self.id: T = id
        self.created_at: datetime = datetime.now(datetime.utc)
        self.created_by: Optional[str] = created_by
        self.last_modified: datetime = datetime.now(datetime.utc)
        self.last_modified_by: Optional[str] = last_modified_by
        self._domain_events: List[IDomainEvent] = []

    @property
    def domain_events(self) -> List[IDomainEvent]:
        return list(self._domain_events)

    def add_domain_event(self, event: IDomainEvent) -> None:
        self._domain_events.append(event)

    def clear_domain_events(self) -> List[IDomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events