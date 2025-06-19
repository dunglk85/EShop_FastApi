from dataclasses import dataclass
from typing import List
from uuid import UUID
from src.domain.models.order import *


@dataclass
class AddressDTO:
    first_name: str
    last_name: str
    email_address: str
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
class OrderDTO_in:
    customer_id: UUID
    order_name: str
    shipping_address: AddressDTO
    billing_address: AddressDTO
    payment: PaymentDTO
    order_items: List[OrderItemDTO]
    status: OrderStatus


@dataclass
class OrderDTO(OrderDTO_in):
    id: UUID

def map_address_to_dto(address: Address) -> AddressDTO:
    return AddressDTO(
        first_name=address.first_name,
        last_name=address.last_name,
        email_address=address.email_address,
        address_line=address.address_line,
        country=address.country,
        state=address.state,
        zip_code=address.zip_code
    )

def map_payment_to_dto(payment: Payment) -> PaymentDTO:
    return PaymentDTO(
        card_name=payment.card_name,
        card_number=payment.card_number,
        expiration=payment.expiration,
        cvv=payment.cvv,
        payment_method=payment.payment_method
    )

def map_order_item_to_dto(item: OrderItem) -> OrderItemDTO:
    return OrderItemDTO(
        product_id=item.product_id.value,
        quantity=item.quantity,
        price=item.price
    )

def map_order_to_dto(order: Order) -> OrderDTO:
    return OrderDTO(
        id=order.id.value,
        customer_id=order.customer_id.value,
        order_name=order.order_name,
        shipping_address=map_address_to_dto(order.shipping_address),
        billing_address=map_address_to_dto(order.billing_address),
        payment=map_payment_to_dto(order.payment),
        order_items=[map_order_item_to_dto(item) for item in order.order_items],
        status=order.status
    )
