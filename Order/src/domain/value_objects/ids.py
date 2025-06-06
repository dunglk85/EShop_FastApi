from src.domain.exception import DomainException
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Any, TypeVar, Type, Optional
from abc import ABC

T = TypeVar("T", bound="UUIDIdentifier")

@dataclass(frozen=True)
class UUIDIdentifier(ABC):
    value: UUID

    @classmethod
    def of(cls: Type[T], value: UUID) -> T:
        if value is None:
            raise ValueError(f"{cls.__name__} cannot be None.")
        if value.int == 0:
            raise DomainException(f"{cls.__name__} cannot be empty.")
        return cls(value)

    @classmethod
    def new(cls: Type[T]) -> T:
        return cls(uuid4())

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
    
@dataclass(frozen=True)
class OrderId(UUIDIdentifier):
    pass

@dataclass(frozen=True)
class CustomerId(UUIDIdentifier):
    pass

@dataclass(frozen=True)
class ProductId(UUIDIdentifier):
	pass

@dataclass(frozen=True)
class OrderItemId(UUIDIdentifier):
	pass