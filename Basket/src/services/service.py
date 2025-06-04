from fastapi import HTTPException
from src.models.basket import Basket
from src.repository.IRepository import IBasketRepository

class BasketService:
    def __init__(self, repository: IBasketRepository):
        self.repository = repository

    async def add_item(self, req: Basket):
        await self.repository.add_items(req.user_id, req.items)

    async def update_item(self, user_id: str, product_id: str, quantity: int):
        success = await self.repository.update_quantity(user_id, product_id, quantity)
        if not success:
            raise HTTPException(status_code=404, detail="Item not found")

    async def get_items(self, user_id: str):
        return await self.repository.get_items(user_id)

    async def delete_item(self, user_id: str, product_id: str):
        await self.repository.delete_item(user_id, product_id)

    async def clear_basket(self, user_id: str):
        await self.repository.clear_basket(user_id)

    async def checkout(self, user_id: str):
        items = await self.repository.get_and_clear_basket(user_id)
        if not items:
            raise HTTPException(status_code=404, detail="Basket is empty")
        return items

