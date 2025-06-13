from utils.mediator import mediator
from application.queries.get_order_by_id import GetOrderByIdHandler
from application.queries.get_orders import GetOrdersHandler
from application.queries.get_order_by_custormer import GetOrderByCustomerHandler
from application.commands.create_order import CreateOrderHandler
from application.commands.delete_order import DeleteOrderHandler
from application.commands.update_order import UpdateOrderHandler
from infrastructure.repositories.query_order_repository import QueryOrderRepository
from infrastructure.repositories.command_order_repository import CommandOrderRepository
from application.requests import *

mediator.register(QueryOrderById, GetOrderByIdHandler(QueryOrderRepository()).handle)

mediator.register(QueryOrders, GetOrdersHandler(QueryOrderRepository()).handle)

mediator.register(QueryOrdersByCustomerId, GetOrderByCustomerHandler(QueryOrderRepository()).handle)

mediator.register(CommandCreateOrder, CreateOrderHandler(CommandOrderRepository()).handle)

mediator.register(CommandDeleteOrder, DeleteOrderHandler(CommandOrderRepository()).handle)

mediator.register(CommandUpdateOrder, UpdateOrderHandler(CommandOrderRepository()).handle)
