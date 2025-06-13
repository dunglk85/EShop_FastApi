from dataclasses import dataclass
from src.application.repositories.command_order_repository import IcommandOrderRepository
from src.domain.value_objects.ids import OrderId
from src.application.dtos import OrderDTO
from application.requests import *


class UpdateOrderHandler:
    def __init__(self, repository: IcommandOrderRepository):
        self.repository = repository

    async def handle(self, command: CommandUpdateOrder) -> bool:
        order = await self.repository.get_order_by_id(OrderId.of(command.order.order_id))

        if not order:
            raise ValueError(f"Order with ID {command.order.order_id} does not exist.")
        # Clear any existing domain events before updating
        order.clear_domain_events()

        for key, value in command.order.new_details.items():
            if key == "order_name":
                order.change_order_name(value)
            elif key == "shipping_address":
                order.change_shipping_address(value)
            elif key == "billing_address":
                order.change_billing_address(value)
            elif key == "payment":
                order.change_payment_method(value)
            elif key == "order_items":
                for item in order.order_items:
                    if item.product_id in value:
                        # If the item exists in the new details, update it
                        new_item = value[item.product_id]
                        order.change_item(
							product_id=item.product_id,
							new_quantity=new_item.quantity,
							new_price=new_item.price
						)
                        value.pop(item.product_id, None)
                    else:
                        # If the item is not in the new details, remove it
                        order.remove_item(item.product_id)
                for item in value:
                    order.add_item(
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.price
                    )
                    
        # Save the updated aggregate
        await self.repository.forward(order)
        return order
