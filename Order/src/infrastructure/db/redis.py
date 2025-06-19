import os
import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

# Database numbers for different purposes
REDIS_BROKER = 0
REDIS_BACKEND = 1
REDIS_CACHE = 2
REDIS_OTHER = 3  # Add more as needed
QUEUE_KEY = "projection_queue"

# Factory to create a Redis client for a given DB number
async def get_redis_client(db_number: int) -> redis.Redis:
    return redis.Redis.from_url(f"{REDIS_URL}/{db_number}")
