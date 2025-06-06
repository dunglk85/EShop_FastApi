from src.domain.exception import DomainException
from dataclasses import dataclass
from typing import field, Any

@dataclass(frozen=True)
class OrderName:
    value: str
    _DEFAULT_LENGTH: int = field(default=5, init=False, repr=False)

    @staticmethod
    def of(value: str) -> "OrderName":
        if not value or not value.strip():
            raise DomainException("OrderName cannot be empty.")
        if not value.isalpha():
            raise DomainException("OrderName must contain only alphabetic characters.")
        return OrderName(value)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, OrderName) and self.value == other.value

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, OrderName):
            return NotImplemented
        return self.value < other.value

    def __hash__(self) -> int:
        return hash(self.value)