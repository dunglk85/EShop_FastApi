from abc import ABC
from datetime import datetime
from typing import Optional, TypeVar, Generic

T = TypeVar("T")

class IEntity(ABC):
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    last_modified: Optional[datetime] = None
    last_modified_by: Optional[str] = None


class IEntityWithId(IEntity, Generic[T], ABC):
    id: T

class Entity(IEntityWithId[T], ABC):
    def __init__(
        self,
        id: T,
        created_by: Optional[str] = None,
        last_modified_by: Optional[str] = None,
    ):
        self.id = id
        self.created_at = datetime.now(datetime.utc)
        self.created_by = created_by
        self.last_modified = datetime.now(datetime.utc)
        self.last_modified_by = last_modified_by
