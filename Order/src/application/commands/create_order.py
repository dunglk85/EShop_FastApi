from dataclasses import dataclass
from typing import List
from uuid import UUID
from src.application.dtos import OrderDTO
from src.domain.models.order import Order
from src.domain.value_objects.ids import CustomerId, ProductId
from src.domain.value_objects.order_name import OrderName
from src.domain.value_objects.address import Address
from src.domain.value_objects.payment import Payment
from src.application.repositories.command_order_repository import IcommandOrderRepository

    

class CreateOrderHandler:
    def __init__(self, repository: IcommandOrderRepository):
        self.repository = repository

    async def handle(self, command: OrderDTO) -> UUID:
        shipping_address = Address(
            first_name=command.shipping_address.first_name,
            last_name=command.shipping_address.last_name,
            email=command.shipping_address.email,
            address_line=command.shipping_address.address_line,
            country=command.shipping_address.country,
            state=command.shipping_address.state,
            zip_code=command.shipping_address.zip_code,
        )

        billing_address = Address(
            first_name=command.billing_address.first_name,
            last_name=command.billing_address.last_name,
            email=command.billing_address.email,
            address_line=command.billing_address.address_line,
            country=command.billing_address.country,
            state=command.billing_address.state,
            zip_code=command.billing_address.zip_code,
        )

        payment = Payment(
            card_name=command.payment.card_name,
            card_number=command.payment.card_number,
            expiration=command.payment.expiration,
            cvv=command.payment.cvv,
            method=command.payment.payment_method,
        )

        order = Order.create(
            customer_id=CustomerId.of(command.customer_id),
            order_name=OrderName.of(command.order_name),
            shipping_address=shipping_address,
            billing_address=billing_address,
            payment=payment
        )

        for item in command.order_items:
            order.add_item(
                product_id=ProductId.of(item.product_id),
                quantity=item.quantity,
                price=item.price
            )
        await self.repository.create_order(order)
        return order.id.value
