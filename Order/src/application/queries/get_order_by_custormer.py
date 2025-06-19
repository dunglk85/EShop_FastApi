from src.application.repositories.query_order_repository import IQueryOrderRepository
from src.application.requests import *
from src.application.dtos import *

class GetOrderByCustomerHandler:
	def __init__(self, order_repository: IQueryOrderRepository):
		self.order_repository = order_repository

	async def handle(self, query: QueryOrdersByCustomerId):
		"""
		Retrieves orders for a specific customer.

		:param customer_id: The ID of the customer whose orders are to be retrieved.
		:return: A list of orders associated with the given customer ID.
		"""
		order = await self.order_repository.get_orders_by_customer(query.customer_id)
		return map_order_to_dto(order=order)