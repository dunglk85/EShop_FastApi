from pydantic import BaseModel, Field
from typing import List

class BasketItem(BaseModel):
    product_id: str = Field(..., description="Unique identifier for the product")
    name: str = Field(..., description="Name of the product")
    price: float =  Field(..., description="Price of the product")
    quantity: int = Field(..., ge=1, description="Quantity of the product in the basket")


class Basket(BaseModel):
    user_id: str
    items: List[BasketItem]  # changed from single item to list

#class AddBasketItemRequest(BaseModel):
#    user_id: str
#    items: List[BasketItem]


#class UpdateBasketItemRequest(BaseModel):
#    user_id: str
#    product_id: str
#    quantity: int
