# src/infrastructure/db/redis_client.py
import aioredis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

# Database numbers for different purposes
REDIS_BROKER = 0
REDIS_BACKEND = 1
REDIS_CACHE = 2
REDIS_OTHER = 3  # Add more as needed

# Factory to create a Redis pool for a given DB number
async def get_redis_pool(db_number: int):
    return await aioredis.create_redis_pool(f"{REDIS_URL}/{db_number}")