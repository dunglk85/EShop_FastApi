from src.infrastructure.kafka.kafka_producer import get_kafka_producer
from src.infrastructure.db.write_db import get_session
from src.infrastructure.outbox.celery_worker import celery_app as celery
from src.infrastructure.db.redis import REDIS_BROKER, get_redis_client, QUEUE_KEY
import json
from sqlalchemy import text

@celery.task
async def process_outbox_messages():
    redis = await get_redis_client(REDIS_BROKER)
    async for db in get_session():
        
        try:
            # Fetch unpublished outbox events
            result = await db.execute(
                text("SELECT * FROM outbox WHERE published = false")
            )
            outbox_events = result.scalars().all()

            if not outbox_events:
                return

            producer = await get_kafka_producer()

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
            if producer:
                await producer.stop()