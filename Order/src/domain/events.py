from src.domain.abstraction.domain_event import IDomainEvent

class OrderCreatedEvent(IDomainEvent):
	def __init__(self, order_id: str, customer_id: str, items: list):
		self.order_id = order_id
		self.customer_id = customer_id
		self.items = items

class OrderUpdatedEvent(IDomainEvent):
	def __init__(self, order_id: str, items: list):
		self.order_id = order_id
		self.items = items