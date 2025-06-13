from infrastructure.outbox.processor import process_outbox_messages
from celery import shared_task
import asyncio

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def process_outbox_task(self):
    try:
        asyncio.run(process_outbox_messages())
    except Exception as e:
        raise self.retry(exc=e)
