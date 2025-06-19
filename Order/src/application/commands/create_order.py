from dataclasses import dataclass
from typing import List
from uuid import UUID
from src.application.dtos import *
from src.domain.models.order import Order
from src.domain.value_objects.ids import CustomerId, ProductId
from src.domain.value_objects.order_name import OrderName
from src.domain.value_objects.address import Address
from src.domain.value_objects.payment import Payment
from src.application.repositories.command_order_repository import IcommandOrderRepository
from src.application.requests import *

    

class CreateOrderHandler:
    def __init__(self, repository: IcommandOrderRepository):
        self.repository = repository

    async def handle(self, command: CommandCreateOrder) -> OrderDTO:
        shipping_address = Address(
            first_name=command.order.shipping_address.first_name,
            last_name=command.order.shipping_address.last_name,
            address_line=command.order.shipping_address.address_line,
            country=command.order.shipping_address.country,
            state=command.order.shipping_address.state,
            zip_code=command.order.shipping_address.zip_code,
            email_address = command.order.shipping_address.email_address
        )

        billing_address = Address(
            first_name=command.order.billing_address.first_name,
            last_name=command.order.billing_address.last_name,
            address_line=command.order.billing_address.address_line,
            country=command.order.billing_address.country,
            state=command.order.billing_address.state,
            zip_code=command.order.billing_address.zip_code,
            email_address = command.order.billing_address.email_address
        )

        payment = Payment(
            card_name=command.order.payment.card_name,
            card_number=command.order.payment.card_number,
            expiration=command.order.payment.expiration,
            cvv=command.order.payment.cvv,
            payment_method=command.order.payment.payment_method,
        )

        order = Order.create(
            customer_id=CustomerId.of(command.order.customer_id),
            order_name=OrderName.of(command.order.order_name),
            shipping_address=shipping_address,
            billing_address=billing_address,
            payment=payment
        )

        for item in command.order.order_items:
            order.add_item(
                product_id=ProductId.of(item.product_id),
                quantity=item.quantity,
                price=item.price
            )
        await self.repository.forward(order)
        return map_order_to_dto(order=order)
