from src.domain.exception import DomainException
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Payment:
    card_name: Optional[str]
    card_number: str
    expiration: str
    cvv: str
    payment_method: int

    @staticmethod
    def of(card_name: Optional[str], card_number: str, expiration: str, cvv: str, payment_method: int) -> "Payment":
        if not card_name or not card_name.strip():
            raise DomainException("Card name cannot be empty.")
        if not card_number or not card_number.strip():
            raise DomainException("Card number cannot be empty.")
        if not cvv or not cvv.strip():
            raise DomainException("CVV cannot be empty.")
        if len(cvv) > 3:
            raise DomainException("CVV must not be longer than 3 characters.")

        return Payment(
            card_name=card_name,
            card_number=card_number,
            expiration=expiration,
            cvv=cvv,
            payment_method=payment_method,
        )