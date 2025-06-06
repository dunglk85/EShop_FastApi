from enum import Enum

class OrderStatus(Enum):
    DRAFT = 1
    PENDING = 2
    COMPLETED = 3
    CANCELLED = 4

    def __str__(self) -> str:
        return self.name.capitalize()
