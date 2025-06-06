from src.domain.exception import DomainException
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Address:
    first_name: str
    last_name: str
    email_address: Optional[str]
    address_line: str
    country: str
    state: str
    zip_code: str

    @staticmethod
    def of(
        first_name: str,
        last_name: str,
        email_address: Optional[str],
        address_line: str,
        country: str,
        state: str,
        zip_code: str,
    ) -> "Address":
        if not email_address or not email_address.strip():
            raise DomainException("Email address cannot be empty.")
        if not address_line or not address_line.strip():
            raise DomainException("Address line cannot be empty.")

        return Address(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            address_line=address_line,
            country=country,
            state=state,
            zip_code=zip_code,
        )