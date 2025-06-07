from dataclasses import dataclass
from datetime import datetime
from value_objects.address import Address
from value_objects.payment import Payment
from value_objects.order_name import OrderName
from value_objects.ids import ProductId, CustomerId, OrderId
from domain.abstraction.domain_event import IDomainEvent


@dataclass(frozen=True)
class OrderCreated(IDomainEvent):
    order_id: OrderId
    customer_id: CustomerId
    order_name: OrderName
    shipping_address: Address
    billing_address: Address
    payment: Payment

@dataclass(frozen=True)
class OrderCanceled(IDomainEvent):
    order_id: OrderId
    
@dataclass(frozen=True)
class OrderConfirmed(IDomainEvent):
	order_id: OrderId

@dataclass(frozen=True)
class OrderShipped(IDomainEvent):
	order_id: OrderId
	tracking_number: str
     
@dataclass(frozen=True)
class OrderFulfilled(IDomainEvent):
	order_id: OrderId
	tracking_number: str

@dataclass(frozen=True)
class OrderDeleted(IDomainEvent):
	order_id: OrderId

@dataclass(frozen=True)
class OrderItemAdded(IDomainEvent):
    order_id: OrderId
    product_id: ProductId
    quantity: int
    price: float
    

@dataclass(frozen=True)
class OrderItemRemoved(IDomainEvent):
    order_id: OrderId
    product_id: ProductId
    
@dataclass(frozen=True)
class OrderItemQuantityChanged(IDomainEvent):
    order_id: OrderId
    product_id: ProductId
    new_quantity: int
    
@dataclass(frozen=True)
class OrderBillingAddressChanged(IDomainEvent):
    order_id: OrderId
    billing_address: Address
    

@dataclass(frozen=True)
class OrderShippingAddressChanged(IDomainEvent):
    order_id: OrderId
    shipping_address: Address
    
@dataclass(frozen=True)
class OrderPaymentMethodChanged(IDomainEvent):
    order_id: OrderId
    payment: Payment
@dataclass(frozen=True)
class OrderChangeName(IDomainEvent):
	order_id: OrderId
	new_order_name: OrderName