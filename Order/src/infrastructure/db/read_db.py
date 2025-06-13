# src/infrastructure/db/mongo.py
import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
DB_NAME = "order_read_db"
QUEUE_KEY = "projection_queue"