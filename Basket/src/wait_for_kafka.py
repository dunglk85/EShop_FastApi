from src.config import message_bus
import logging
import asyncio
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError

logger = logging.getLogger(__name__)

async def wait_for_kafka(host="kafka", port=9092, timeout=30):
    deadline = asyncio.get_event_loop().time() + timeout
    bootstrap_servers = f"{host}:{port}"
    while True:
        try:
            temp_producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
            await temp_producer.start()
            await temp_producer.stop()
            logger.info("✅ Kafka is available.")
            return
        except KafkaConnectionError:
            if asyncio.get_event_loop().time() > deadline:
                raise RuntimeError("❌ Kafka did not become available in time.")
            logger.info("⏳ Waiting for Kafka to be ready...")
            await asyncio.sleep(2)
        finally:
            if not temp_producer._closed:
                await temp_producer.stop()