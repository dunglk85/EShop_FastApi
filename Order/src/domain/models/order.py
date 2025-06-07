from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from src.domain.events import (
    OrderCreated,
    OrderCanceled,
    OrderConfirmed,
    OrderShipped,
    OrderFulfilled,
    OrderDeleted,
    OrderItemAdded,
    OrderItemRemoved,
    OrderBillingAddressChanged,
    OrderShippingAddressChanged,
    OrderPaymentMethodChanged,
    OrderItemChanged,
    OrderNameChanged
)
from value_objects.address import Address
from value_objects.payment import Payment
from value_objects.order_name import OrderName
from value_objects.ids import ProductId, CustomerId, OrderId
from domain.enum import OrderStatus
from domain.abstraction.aggregate import Aggregate
from domain.models.order_item import OrderItem


class Order(Aggregate[OrderId]):
    def __init__(self):
        if not getattr(self.__class__, "__allow_init", False):
            raise Exception("Use the create method to instantiate an Order.")
        super().__init__(OrderId(uuid4()))

    @property
    def customer_id(self) -> Optional[CustomerId]:
        return self._customer_id
    
    @property
    def order_name(self) -> Optional[OrderName]:
        return self._order_name
    
    @property
    def shipping_address(self) -> Optional[Address]:
        return self._shipping_address
    
    @property
    def billing_address(self) -> Optional[Address]:
        return self._billing_address
    
    
    @property
    def payment(self) -> Optional[Payment]:
        return self._payment
    
    @property
    def id(self) -> OrderId:
        return self._id
    
    @property
    def status(self) -> OrderStatus:
        return self._status
    
    @property
    def order_items(self) -> List[OrderItem]:
        return list(self._order_items)

    # --- Command Handlers that Raise Events ---
    @classmethod
    def create(cls, customer_id: CustomerId, order_name: OrderName, shipping_address: Address, billing_address: Address, payment: Payment):
        Order.__allow_init = True
        order = cls()
        Order.__allow_init = False
        order.raise_event(OrderCreated(order.id, customer_id, order_name, shipping_address, billing_address, payment))
        return order
    
    def confirm(self):
        self.raise_event(OrderConfirmed(self.id))

    def ship(self, tracking_number: str):
        self.raise_event(OrderShipped(self.id, tracking_number))

    def fulfill(self, tracking_number: str):
        self.raise_event(OrderFulfilled(self.id, tracking_number))

    def delete(self):
        self.raise_event(OrderDeleted(self.id))

    def cancel(self):
        self.raise_event(OrderCanceled(self.id))

    def add_item(self, product_id: ProductId, quantity: int, price: float):
        self.raise_event(OrderItemAdded(self.id, product_id, quantity, price))

    def remove_item(self, product_id: ProductId):
        self.raise_event(OrderItemRemoved(self.id, product_id))

    def change_item(self, product_id: ProductId, new_quantity: int, new_price: float):
        self.raise_event(OrderItemChanged(self.id, product_id, new_quantity, new_price))

    def change_billing_address(self, address: Address):
        self.raise_event(OrderBillingAddressChanged(self.id, address))

    def change_shipping_address(self, address: Address):
        self.raise_event(OrderShippingAddressChanged(self.id, address))

    def change_payment_method(self, payment: Payment):
        self.raise_event(OrderPaymentMethodChanged(self.id, payment))

    def change_order_name(self, order_name: OrderName):
        self.raise_event(OrderNameChanged(self.id, order_name))

    # --- Apply Methods ---

    def _apply_OrderCreated(self, event: OrderCreated):
        self._customer_id = event.customer_id
        self._order_name = event.order_name
        self._shipping_address = event.shipping_address
        self._billing_address = event.billing_address
        self._payment = event.payment
        self._status = OrderStatus.PENDING
        self._order_items = []
    
    def _apply_OrderConfirmed(self, event: OrderConfirmed):
        self._status = OrderStatus.CONFIRMED
    
    def _apply_OrderShipped(self, event: OrderShipped):
        self._status = OrderStatus.SHIPPED

    def _apply_OrderFulfilled(self, event: OrderFulfilled):
        self._status = OrderStatus.FULFILLED
    
    def _apply_OrderDeleted(self, event: OrderDeleted):
        self._status = OrderStatus.DELETED
        self._order_items.clear()

    def _apply_OrderCanceled(self, event: OrderCanceled):
        self._status = OrderStatus.CANCELLED

    def _apply_OrderItemAdded(self, event: OrderItemAdded):
        item = OrderItem(order_id=self.id, product_id=event.product_id, quantity=event.quantity, price=event.price)
        self._order_items.append(item)

    def _apply_OrderItemRemoved(self, event: OrderItemRemoved):
        self._order_items = [i for i in self._order_items if i.product_id != event.product_id]

    def _apply_OrderItemChanged(self, event: OrderItemChanged):
        for item in self._order_items:
            if item.product_id == event.product_id:
                item.quantity = event.new_quantity
                item.price = event.new_price
                break

    def _apply_OrderBillingAddressChanged(self, event: OrderBillingAddressChanged):
        self._billing_address = event.billing_address

    def _apply_OrderShippingAddressChanged(self, event: OrderShippingAddressChanged):
        self._shipping_address = event.shipping_address

    def _apply_OrderPaymentMethodChanged(self, event: OrderPaymentMethodChanged):
        self._payment = event.payment
    
    def _apply_OrderNameChanged(self, event: OrderNameChanged):
        self._order_name = event.new_order_name
