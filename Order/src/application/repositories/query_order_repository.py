from abc import ABC

class IQueryOrderRepository(ABC):
	async def get_order_by_id(self, order_id):
		"""Retrieve an order by its ID."""
		raise NotImplementedError("This method should be overridden by subclasses.")

	async def get_orders_by_user_id(self, user_id):
		"""Retrieve all orders for a specific user."""
		raise NotImplementedError("This method should be overridden by subclasses.")

	async def get_all_orders(self):
		"""Retrieve all orders."""
		raise NotImplementedError("This method should be overridden by subclasses.")