from dataclasses import dataclass
from datetime import datetime
from value_objects.address import Address
from value_objects.payment import Payment
from value_objects.order_name import OrderName
from value_objects.ids import ProductId, CustomerId, OrderId
from domain.abstraction.domain_event import IDomainEvent, IntegrationEvent


@dataclass(frozen=True)
class OrderCreated(IDomainEvent):
    order_id: OrderId
    customer_id: CustomerId
    order_name: OrderName
    shipping_address: Address
    billing_address: Address
    payment: Payment

@dataclass(frozen=True)
class OrderCanceled(IntegrationEvent):
    order_id: OrderId
    
@dataclass(frozen=True)
class OrderConfirmed(IntegrationEvent):
	order_id: OrderId

@dataclass(frozen=True)
class OrderShipped(IntegrationEvent):
	order_id: OrderId
	tracking_number: str
     
@dataclass(frozen=True)
class OrderFulfilled(IntegrationEvent):
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
class OrderItemChanged(IDomainEvent):
    order_id: OrderId
    product_id: ProductId
    quantity: int
    price: float
    
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
class OrderNameChanged(IDomainEvent):
	order_id: OrderId
	new_order_name: OrderName