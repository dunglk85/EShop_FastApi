from aiokafka import AIOKafkaConsumer
import json
import os

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")

class KafkaConsumer:
    def __init__(self, topic: str, group_id: str = "default_group", bootstrap_servers: str = KAFKA_BOOTSTRAP):
        self.topic = topic
        self.group_id = group_id
        self.bootstrap_servers = bootstrap_servers
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            enable_auto_commit=True,
            auto_offset_reset="earliest",
            group_id=self.group_id
        )

    async def start(self, handler):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                try:
                    await handler(msg.value)
                except Exception as e:
                    print(f"Handler error: {e}")
        finally:
            await self.consumer.stop()

    async def stop(self):
        await self.consumer.stop()

async def get_kafka_consumer(topic: str):
    return KafkaConsumer(topic=topic)
