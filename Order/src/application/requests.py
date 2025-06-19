from dataclasses import dataclass
from src.domain.value_objects.ids import *
from abc import ABC
from src.application.dtos import *

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
	order: OrderDTO_in

@dataclass
class CommandDeleteOrder(IRequest):
	order_id: OrderId

@dataclass
class CommandUpdateOrder(IRequest):
	order: OrderDTO

