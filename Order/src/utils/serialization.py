from src.domain.events import (
	OrderCreated,
	OrderCanceled,
	OrderConfirmed,
	OrderShipped,
	OrderFulfilled,
	OrderDeleted,
	OrderItemAdded,
	OrderItemRemoved,
	OrderItemChanged,
	OrderBillingAddressChanged,
	OrderShippingAddressChanged,
	OrderPaymentMethodChanged,
	OrderNameChanged
)

all_events = {
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
	"OrderNameChanged": OrderNameChanged
}

def serialize_event(event) -> dict:
    return event.dict()

def deserialize_event(event_type: str, payload: dict):
    event_cls = all_events.get(event_type)
    if not event_cls:
        raise ValueError(f"Unknown event type: {event_type}")
    return event_cls(**payload)

def convert_uuids(obj):
    import uuid
    if isinstance(obj, dict):
        return {k: convert_uuids(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_uuids(i) for i in obj]
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    else:
        return obj