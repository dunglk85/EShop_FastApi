from celery import Celery
from infrastructure.db.redis import REDIS_URL, REDIS_BROKER, REDIS_BACKEND

celery_app = Celery(
    "order_service",
    broker=f"{REDIS_URL}/{REDIS_BROKER}",
    backend=f"{REDIS_URL}/{REDIS_BACKEND}",
)

celery_app.autodiscover_tasks(['src.infrastructure.outbox'])
