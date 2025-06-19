from src.domain.events import *

EVENT_TYPE_MAPPING = {
    "OrderCreated": OrderCreated,
    "OrderCanceled": OrderCanceled,
    "OrderConfirmed": OrderConfirmed,
    "OrderShipped": OrderShipped,
    "OrderFulfilled": OrderFulfilled,
    "OrderDeleted": OrderDeleted,
    "OrderItemAdded": OrderItemAdded,
    "OrderItemRemoved": OrderItemRemoved,
    "OrderItemChanged": OrderItemChanged,
    "OrderBillingAddressChanged": OrderBillingAddressChanged,
    "OrderShippingAddressChanged": OrderShippingAddressChanged,
    "OrderPaymentMethodChanged": OrderPaymentMethodChanged,
    "OrderNameChanged": OrderNameChanged,
}
