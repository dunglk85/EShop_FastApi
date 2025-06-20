import asyncio
import json
import datetime
from src.infrastructure.db.redis import REDIS_BROKER, get_redis_client
from src.infrastructure.db.read_db import DB_NAME, QUEUE_KEY, get_read_db

async def handle_event(event):
    client = get_read_db()
    db = client[DB_NAME]
    projection_log = client["projection_log"]
    # Idempotency check
    if await projection_log.projection_log.find_one({"event_id": event["id"]}):
        return

    event_type = event.get("type")
    payload = event.get("payload", {})

    if event_type == "OrderCreated":
        await db.orders.insert_one(payload)
    else:
        await db.orders.update_one({"id": payload.get("order_id")}, {"$set": payload})

    await projection_log.projection_log.insert_one({
        "event_id": event["id"],
        "projection": event_type,
        "timestamp": datetime.datetime.now()
    })

async def projection_worker():
    redis = await get_redis_client(REDIS_BROKER)
    while True:
        try:
            _, raw_event = await redis.blpop(QUEUE_KEY)
            event = json.loads(raw_event)
            await handle_event(event)
        except Exception as e:
            print(f"Error processing event: {e}")

if __name__ == "__main__":
    asyncio.run(projection_worker())