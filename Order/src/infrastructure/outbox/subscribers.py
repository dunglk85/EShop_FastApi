from src.infrastructure.models.outbox_trigger import OutboxTriggered
from src.utils.mediator import mediator
from src.infrastructure.outbox.tasks import process_outbox_task

async def handle_outbox_triggered(_: OutboxTriggered):
    process_outbox_task.delay()

mediator.register_event_handler(OutboxTriggered, handle_outbox_triggered)
   