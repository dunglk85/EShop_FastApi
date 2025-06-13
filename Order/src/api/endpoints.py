from fastapi import APIRouter, HTTPException
from typing import List
from domain.models.order import Order
from utils.mediator import mediator
from domain.value_objects.ids import OrderId, CustomerId
from application.requests import *
from application.dtos import OrderDTO

router = APIRouter()

@router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    order = await mediator.publish(QueryOrderById(OrderId.of(order_id)))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/orders", response_model=List[Order])
async def get_all_orders():
    return await mediator.publish(QueryOrders())

@router.get("/orders/customer/{customer_id}", response_model=List[Order])
async def get_orders_by_customer(customer_id: str):
    return await mediator.publish(QueryOrdersByCustomerId(CustomerId.of(customer_id)))

@router.post("/orders", response_model=Order)
async def create_order(order: OrderDTO):
    created_order = await mediator.publish(CommandCreateOrder(order=order))
    return created_order

@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: str, order: OrderDTO):
    order.order_id = order_id
    updated_order = await mediator.publish(CommandUpdateOrder(order=order))
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    result = await mediator.publish(CommandDeleteOrder(OrderId.of(order_id)))
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted"}