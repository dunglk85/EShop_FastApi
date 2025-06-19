from src.application.repositories.query_order_repository import IQueryOrderRepository
from bson import ObjectId
from src.infrastructure.db.read_db import DB_NAME, get_read_db

class QueryOrderRepository(IQueryOrderRepository):
    def __init__(self, db):
        client = db
        self.db = client[DB_NAME]
        self.collection = self.db["orders"]  # your read-model collection

    async def get_order_by_id(self, order_id: str):
        """Retrieve an order by its ID."""
        order = await self.collection.find_one({"_id": str(order_id)})
        return order

    async def get_orders_by_customer_id(self, customer_id: str):
        """Retrieve all orders for a specific user."""
        cursor = self.collection.find({"customer_id": customer_id})
        orders = []
        async for order in cursor:
            orders.append(order)
        return orders

    async def get_all_orders(self):
        """Retrieve all orders."""
        cursor = self.collection.find()
        orders = []
        async for order in cursor:
            orders.append(order)
        return orders
