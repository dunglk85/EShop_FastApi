from dataclasses import dataclass
from typing import List, Tuple
from src.domain.value_objects.ids import OrderId, CustomerId, ProductId
from src.domain.value_objects.order_name import OrderName
from src.domain.value_objects.address import Address
from src.domain.value_objects.payment import Payment
from src.domain.events import OrderCreatedEvent, OrderUpdatedEvent
from src.domain.abstraction.aggregate import Aggregate
from src.domain.enum import OrderStatus
from src.domain.models.order_item import OrderItem


class Order(Aggregate[OrderId]):
    def __init__(self, id: OrderId, customer_id: CustomerId, order_name: OrderName,
                 shipping_address: Address, billing_address: Address, payment: Payment):
        super().__init__(id)
        self._customer_id = customer_id
        self._order_name = order_name
        self._shipping_address = shipping_address
        self._billing_address = billing_address
        self._payment = payment
        self._status = OrderStatus.PENDING
        self._order_items: List[OrderItem] = []

        self.add_domain_event(OrderCreatedEvent(self))

    @property
    def customer_id(self) -> CustomerId:
        return self._customer_id

    @property
    def order_name(self) -> OrderName:
        return self._order_name

    @property
    def shipping_address(self) -> Address:
        return self._shipping_address

    @property
    def billing_address(self) -> Address:
        return self._billing_address

    @property
    def payment(self) -> Payment:
        return self._payment

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def order_items(self) -> Tuple[OrderItem, ...]:
        return tuple(self._order_items)

    @property
    def total_price(self) -> float:
        return sum(item.price * item.quantity for item in self._order_items)

    def update(self, order_name: OrderName, shipping_address: Address,
               billing_address: Address, payment: Payment, status: OrderStatus):
        self._order_name = order_name
        self._shipping_address = shipping_address
        self._billing_address = billing_address
        self._payment = payment
        self._status = status
        self.add_domain_event(OrderUpdatedEvent(self))

    def add(self, product_id: ProductId, quantity: int, price: float):
        if quantity <= 0 or price <= 0:
            raise ValueError("Quantity and price must be positive")
        item = OrderItem(self.id, product_id, quantity, price)
        self._order_items.append(item)

    def remove(self, product_id: ProductId):
        self._order_items = [item for item in self._order_items if item.product_id != product_id]
