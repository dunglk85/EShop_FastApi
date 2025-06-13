from dataclasses import dataclass
from domain.value_objects.ids import *
from abc import ABC
from application.dtos import *

class IRequest(ABC):
	pass

@dataclass
class QueryOrderById(IRequest):
	order_id: OrderId

@dataclass
class QueryOrders(IRequest):
	pass

@dataclass
class QueryOrdersByCustomerId(IRequest):
	customer_id: CustomerId

@dataclass
class CommandCreateOrder(IRequest):
	order: OrderDTO

@dataclass
class CommandDeleteOrder(IRequest):
	order_id: OrderId

@dataclass
class CommandUpdateOrder(IRequest):
	order: OrderDTO

