from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from src.api.endpoints import router
from src.infrastructure.db.read_db import get_read_db
from src.infrastructure.db.write_db import create_db_and_tables
from src.infrastructure.db.redis import get_redis_client, REDIS_BROKER
from src.infrastructure.kafka.kafka_consumer import get_kafka_consumer
from src.infrastructure.kafka.kafka_producer import get_kafka_producer
from src.infrastructure.repositories.query_order_repository import QueryOrderRepository
from src.infrastructure.repositories.command_order_repository import CommandOrderRepository

from src.application.queries.get_order_by_id import GetOrderByIdHandler
from src.application.queries.get_orders import GetOrdersHandler
from src.application.queries.get_order_by_custormer import GetOrderByCustomerHandler
from src.application.commands.create_order import CreateOrderHandler
from src.application.commands.delete_order import DeleteOrderHandler
from src.application.commands.update_order import UpdateOrderHandler
from src.application.requests import *
from src.utils.mediator import mediator
from src.infrastructure.models.outbox_trigger import OutboxTriggered
from src.infrastructure.outbox.subscribers import handle_outbox_triggered

KAFKA_TOPIC = "your_topic"

async def consume_messages(consumer, handler):
    await consumer.consumer.start()
    try:
        async for msg in consumer.consumer:
            await handler(msg.value)
    finally:
        await consumer.consumer.stop()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- MongoDB ---
    for _ in range(60):
        try:
            mongo_client = get_read_db()
            await mongo_client.admin.command("ping")
            break
        except Exception:
            await asyncio.sleep(1)
    else:
        raise RuntimeError("MongoDB not available")

    # --- PostgreSQL ---
    for _ in range(60):
        try:
            await create_db_and_tables()
            break
        except Exception:
            await asyncio.sleep(1)
    else:
        raise RuntimeError("PostgreSQL not available")

    # --- Redis ---
    for _ in range(60):
        try:
            redis_client = await get_redis_client(REDIS_BROKER)
            await redis_client.ping()
            break
        except Exception:
            await asyncio.sleep(1)
    else:
        raise RuntimeError("Redis not available")

    # --- Kafka Producer ---
    for _ in range(60):
        try:
            kafka_producer = await get_kafka_producer()
            await kafka_producer.start()
            break
        except Exception:
            await asyncio.sleep(1)
    else:
        raise RuntimeError("Kafka Producer not available")

    # --- Kafka Consumer ---
    for _ in range(60):
        try:
            kafka_consumer = await get_kafka_consumer(KAFKA_TOPIC)

            async def handler(event):
                print(event)  # Replace with your real projection handler

            consumer_task = asyncio.create_task(consume_messages(kafka_consumer, handler))
            break
        except Exception:
            await asyncio.sleep(1)
    else:
        await kafka_producer.stop()
        raise RuntimeError("Kafka Consumer not available")

    # --- Store Clients ---
    app.state.mongo_client = mongo_client
    app.state.redis_client = redis_client
    app.state.kafka_producer = kafka_producer
    app.state.kafka_consumer = kafka_consumer
    app.state.consumer_task = consumer_task

    # --- Register Mediator Handlers ---
    query_repo = QueryOrderRepository(mongo_client)
    command_repo = CommandOrderRepository()

    mediator.register_request_handler(QueryOrderById, GetOrderByIdHandler(query_repo).handle)
    mediator.register_request_handler(QueryOrders, GetOrdersHandler(query_repo).handle)
    mediator.register_request_handler(QueryOrdersByCustomerId, GetOrderByCustomerHandler(query_repo).handle)

    mediator.register_request_handler(CommandCreateOrder, CreateOrderHandler(command_repo).handle)
    mediator.register_request_handler(CommandDeleteOrder, DeleteOrderHandler(command_repo).handle)
    mediator.register_request_handler(CommandUpdateOrder, UpdateOrderHandler(command_repo).handle)
    #mediator.register_event_handler(OutboxTriggered, handle_outbox_triggered)

    yield

    # --- Graceful Shutdown ---
    await kafka_producer.stop()
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api/v1", tags=["orders"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, loop="uvloop", http="h11", reload=True)
