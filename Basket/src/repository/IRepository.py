from abc import ABC, abstractmethod
from src.models.basket import BasketItem
from typing import List

class IBasketRepository(ABC):
    @abstractmethod
    async def get_basket_key(user_id: str) -> str:
        pass
    

    @abstractmethod
    async def add_items(user_id: str, items: List[BasketItem]) -> None:
        pass

    @abstractmethod
    async def get_items(user_id: str) -> List[BasketItem]:
        """
        Retrieve all items in the user's basket.
        """
        pass

    @abstractmethod
    async def update_quantity(user_id: str, product_id: str, quantity: int) -> bool:
        """
        Update the quantity of a specific item in the user's basket.
        """
        pass

    @abstractmethod
    async def delete_item(user_id: str, product_id: str) -> None:
        """
        Delete a specific item from the user's basket.
        """
        pass

    @abstractmethod
    async def clear_basket(user_id: str) -> None:
        """
        Clear all items from the user's basket.
        """
        pass
    
    @abstractmethod
    async def get_and_clear_basket(user_id: str) -> List[BasketItem]:
        """
        Retrieve and clear all items from the user's basket.
        """
        pass