from dataclasses import dataclass
from typing import List
from uuid import UUID
from src.application.dtos import AddressDTO, PaymentDTO, OrderItemDTO
from src.domain.models.order import Order
from src.domain.value_objects.ids import OrderId, CustomerId, ProductId
from src.domain.value_objects.order_name import OrderName
from src.domain.value_objects.address import Address
from src.domain.value_objects.payment import Payment
from src.application.repositories.command_order_repository import IcommandOrderRepository
from application.requests import *

class DeleteOrderHandler:
    def __init__(self, repository: IcommandOrderRepository):
        self.repository = repository

    async def handle(self, command: CommandDeleteOrder) -> bool:
        order = await self.repository.get_order_by_id(OrderId.of(command.order_id))
        if not order:
            raise ValueError(f"Order with ID {command.order_id} does not exist.")
        order.clear_domain_events()  # Clear any existing domain events before deletion
        order.delete()
        
        await self.repository.forward(order)
        return True
