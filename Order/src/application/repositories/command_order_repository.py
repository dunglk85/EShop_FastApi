from abc import ABC

class IcommandOrderRepository(ABC):
	async def create_order(self, order):
		"""Create a new order."""
		raise NotImplementedError("This method should be overridden by subclasses.")

	async def update_order(self, order_id, order_data):
		"""Update an existing order."""
		raise NotImplementedError("This method should be overridden by subclasses.")

	async def delete_order(self, order_id):
		"""Delete an existing order."""
		raise NotImplementedError("This method should be overridden by subclasses.")
	async def get_order_by_id(self, order_id):
		"""Retrieve an order by its ID."""
		raise NotImplementedError("This method should be overridden by subclasses.")