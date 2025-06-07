from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class AddressDTO:
    first_name: str
    last_name: str
    email: str
    address_line: str
    country: str
    state: str
    zip_code: str


@dataclass
class PaymentDTO:
    card_name: str
    card_number: str
    expiration: str
    cvv: str
    payment_method: str


@dataclass
class OrderItemDTO:
    product_id: UUID
    quantity: int
    price: float


@dataclass
class OrderDTO:
    order_id: UUID
    customer_id: UUID
    order_name: str
    shipping_address: AddressDTO
    billing_address: AddressDTO
    payment: PaymentDTO
    order_items: List[OrderItemDTO]