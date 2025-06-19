# src/infrastructure/db/mongo.py
import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = "order_read_db"
QUEUE_KEY = "projection_queue"

_mongo_client = None

def get_read_db():
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    return _mongo_client