from fastapi import APIRouter, HTTPException
from typing import List
from src.utils.mediator import mediator
from src.domain.value_objects.ids import OrderId, CustomerId
from src.application.requests import *
from src.application.dtos import OrderDTO

router = APIRouter()

@router.get("/orders/{order_id}", response_model=OrderDTO)
async def get_order(order_id: str):
    order = await mediator.send(QueryOrderById(OrderId.of(order_id)))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/orders", response_model=List[OrderDTO])
async def get_all_orders():
    orders = await mediator.send(QueryOrders())
    if not orders:
        return []
    return orders

@router.get("/orders/customer/{customer_id}", response_model=List[OrderDTO])
async def get_orders_by_customer(customer_id: str):
    orders = await mediator.send(QueryOrdersByCustomerId(CustomerId.of(customer_id)))
    if not orders:
        return []
    return orders

@router.post("/orders", response_model=OrderDTO)
async def create_order(order: OrderDTO_in):
    order_ = await mediator.send(CommandCreateOrder(order=order))
    return order_

@router.put("/orders/{order_id}", response_model=OrderDTO)
async def update_order(order_id: str, order: OrderDTO):
    order.order_id = order_id
    updated_order = await mediator.send(CommandUpdateOrder(order=order))
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    result = await mediator.send(CommandDeleteOrder(OrderId.of(order_id)))
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted"}