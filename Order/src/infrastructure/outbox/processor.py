from infrastructure.kafka.kafka_producer import KafkaProducer
from infrastructure.db.write_db import async_get_session
from celery_app import celery
from infrastructure.db.redis import REDIS_BROKER, get_redis_pool, QUEUE_KEY
import json

@celery.task
async def process_outbox_messages():
    redis = await get_redis_pool(REDIS_BROKER)
    async for db in async_get_session():
        
        try:
            # Fetch unpublished outbox events
            result = await db.execute(
                "SELECT * FROM outbox WHERE published = false"
            )
            outbox_events = result.scalars().all()

            if not outbox_events:
                return

            producer = KafkaProducer()

            for event in outbox_events:
                # Publish to Redis (all events)
                await redis.rpush(QUEUE_KEY, json.dumps(event.payload))

                # Publish to Kafka if integration event
                if getattr(event, "is_integration_event", False):
                    await producer.send(topic=event.topic, value=event.payload)

                # Mark as published
                event.published = True

            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e
        finally:
            await db.close()