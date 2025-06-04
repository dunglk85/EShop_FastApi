# rabbitmq_bus.py
import json
import aio_pika
from .message_bus import MessageBus
import os


class RabbitMQMessageBus(MessageBus):
    def __init__(self, url="amqp://guest:guest@localhost/"):
        self.url = url
        self.connection = None
        self.channel = None

    async def start(self):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()

    async def stop(self):
        if self.connection:
            await self.connection.close()

    async def publish(self, event_type: str, payload: dict):
        message = aio_pika.Message(
            body=json.dumps({"type": event_type, **payload}).encode()
        )
        await self.channel.default_exchange.publish(
            message, routing_key="order-events"
        )
