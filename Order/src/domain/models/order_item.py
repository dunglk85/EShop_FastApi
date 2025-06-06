from typing import Optional
from src.domain.abstraction.entity import Entity
from src.domain.value_objects.ids import OrderId, ProductId, OrderItemId


class OrderItem(Entity[OrderItemId]):
    def __init__(self, order_id: OrderId, product_id: ProductId, quantity: int, price: float):
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if price <= 0:
            raise ValueError("Price must be positive.")

        super().__init__(id=OrderItemId.new())
        self._order_id = order_id
        self._product_id = product_id
        self._quantity = quantity
        self._price = price

    @property
    def order_id(self) -> OrderId:
        return self._order_id

    @property
    def product_id(self) -> ProductId:
        return self._product_id

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def price(self) -> float:
        return self._price
