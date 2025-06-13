from fastapi import APIRouter, Depends
from src.models.basket import Basket
from src.dependencies import get_service
from src.services.service import BasketService
from src.config import message_bus
import uuid

router = APIRouter()

@router.post("/basket/add")
async def add_to_basket(req: Basket, service: BasketService = Depends(get_service)):
    await service.add_item(req)
    return {"message": "Item added to basket"}


@router.put("/basket/{user_id}/item/{product_id}")
async def update_basket_item(user_id: str, product_id: str, quantity: int, service: BasketService = Depends(get_service)):
    await service.update_item(user_id= user_id, product_id=product_id, quantity=quantity)
    return {"message": "Item updated"}


@router.get("/basket/{user_id}")
async def get_basket(user_id: str, service: BasketService = Depends(get_service)):
    return await service.get_items(user_id)

@router.delete("/basket/{user_id}/item/{product_id}")
async def delete_item(user_id: str, product_id: str, service: BasketService = Depends(get_service)):
    await service.delete_item(user_id, product_id)
    return {"message": "Item deleted"}


@router.delete("/basket/{user_id}")
async def clear_basket(user_id: str, service: BasketService = Depends(get_service)):
    await service.clear_basket(user_id)
    return {"message": "Basket cleared"}

@router.post("/basket/checkout/{user_id}")
async def checkout(user_id: str, service: BasketService = Depends(get_service)):
    items = await service.checkout(user_id)
    order_id = str(uuid.uuid4())
    payload = {
        "order_id": order_id,
        "user_id": user_id,
        "items": [item.dict() for item in items],
    }
    await message_bus.publish("Basket_checkouted", payload)
    return {"message": "Checkout successful", "order_id": order_id}