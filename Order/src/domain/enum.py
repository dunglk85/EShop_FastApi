from enum import Enum

class OrderStatus(Enum):
    DRAFT = 1
    PENDING = 2
    CONFIRMED = 3
    SHIPPED = 4
    FULFILLED = 5
    CANCELLED = 6
    DELETED = 7

    def __str__(self) -> str:
        return self.name.capitalize()
