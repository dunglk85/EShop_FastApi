from src.application.repositories.query_order_repository import IQueryOrderRepository
from application.requests import *

class GetOrdersHandler:
	def __init__(self, order_repository: IQueryOrderRepository):
		self.order_repository = order_repository

	async def handle(self, query: QueryOrders):
		"""
		Retrieves orders for a specific customer.

		:param customer_id: The ID of the customer whose orders are to be retrieved.
		:return: A list of orders associated with the given customer ID.
		"""
		return self.order_repository.get_all_orders()