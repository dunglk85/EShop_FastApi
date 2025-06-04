import json
from typing import List
from src.db.redis_client import redis_client as r
from src.models.basket import BasketItem
from src.repository.IRepository import IBasketRepository

class RedisBasketRepository(IBasketRepository):
	"""
	Repository for managing user baskets in Redis.
	"""
	def __init__(self, redis_client):
		self.r = redis_client

	def get_basket_key(self, user_id: str) -> str:
		return f"basket:{user_id}:items"

	async def add_items(self, user_id: str, items: List[BasketItem]):
		key = self.get_basket_key(user_id)
		pipe = r.pipeline()
		for item in items:
			pipe.hset(key, item.product_id, item.json())
		await pipe.execute()

	async def get_items(self, user_id: str) -> List[BasketItem]:
		key = self.get_basket_key(user_id)
		raw_items = await r.hgetall(key)
		return [BasketItem(**json.loads(value)) for value in raw_items.values()]

	async def update_quantity(self, user_id: str, product_id: str, quantity: int) -> bool:
		key = self.get_basket_key(user_id)
		val = await r.hget(key, product_id)
		if not val:
			return False
		item = json.loads(val)
		item["quantity"] = quantity
		await r.hset(key, product_id, json.dumps(item))
		return True

	async def delete_item(self, user_id: str, product_id: str):
		key = self.get_basket_key(user_id)
		await r.hdel(key, product_id)

	async def clear_basket(self, user_id: str):
		key = self.get_basket_key(user_id)
		await r.delete(key)
	
	async def get_and_clear_basket(self, user_id: str) -> List[BasketItem]:
		key = self.get_basket_key(user_id)
		raw_items = await r.hgetall(key)
		await r.delete(key)
		return [BasketItem(**json.loads(val)) for val in raw_items.values()]
