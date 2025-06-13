from abc import ABC

class IcommandOrderRepository(ABC):
	async def forward(self, order):
		"""Create a new order."""
		raise NotImplementedError("This method should be overridden by subclasses.")

	async def get_order_by_id(self, order_id):
		"""Retrieve an order by its ID."""
		raise NotImplementedError("This method should be overridden by subclasses.")