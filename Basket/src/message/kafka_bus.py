# src/message/kafka_bus.py

import json
from aiokafka import AIOKafkaProducer
from src.message.message_bus import MessageBus

class KafkaMessageBus(MessageBus):
    #_instance = None

    #def __new__(cls, *args, **kwargs):
    #    if not cls._instance:
    #        cls._instance = super(KafkaMessageBus, cls).__new__(cls)
    #    return cls._instance

    def __init__(self, bootstrap_servers="localhost:9092"):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.bootstrap_servers = bootstrap_servers
        #self.producer: AIOKafkaProducer | None = None
        #self._initialized = True
        self.producer = None

    async def start(self):
        if not self.producer:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode(),
            )
            await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            self.producer = None

    async def publish(self, event_type: str, payload: dict):
        event = {"type": event_type, **payload}
        await self.producer.send_and_wait("order-events", event)
