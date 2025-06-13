from aiokafka import AIOKafkaConsumer
import motor.motor_asyncio
import json
import asyncio
from pymongo import UpdateOne
from tenacity import retry, stop_after_attempt, wait_exponential

class MongoProjectionConsumer:
    def __init__(self, topic: str, bootstrap_servers: str, mongo_uri: str):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.mongo_uri = mongo_uri
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            enable_auto_commit=True,
            auto_offset_reset="earliest",
            group_id="read_model_updater"
        )
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_uri)
        self.db = self.client.read_model
        
    
    async def start(self):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                try:
                    await self.project(msg.value)
                except Exception as e:
                    print(f"Projection error: {e}")
        finally:
            await self.consumer.stop()
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def project(self, event: dict):
        existing = await self.db.orders.find_one({"id": event.get("id")})
        if existing:
            return
        
        event_type = event.get("type")
        order_id = event.get("order_id")

        if event_type == "OrderCreated":
            await self.db.orders.insert_one(
                {"order_id": order_id},
                {
                    "$setOnInsert": {
                        "order_id": order_id,
                        "customer_id": event.get("customer_id"),
                        "total_price": event.get("total_price"),
                        "created_at": event.get("timestamp"),
                        "items": [],
                        "status": "created"
                    }
                },
                upsert=True
            )

        elif event_type == "OrderItemAdded":
            await self.db.orders.update_one(
                {"order_id": order_id},
                {
                    "$addToSet": {
                        "items": {
                            "product_id": event.get("product_id"),
                            "quantity": event.get("quantity"),
                            "price": event.get("price")
                        }
                    }
                }
            )

        elif event_type == "OrderCancelled":
            await self.db.orders.update_one(
                {"order_id": order_id},
                {"$set": {"status": "cancelled"}}
            )
