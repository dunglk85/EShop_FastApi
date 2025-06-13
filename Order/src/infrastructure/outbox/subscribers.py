from domain.notifications import OutboxTriggered
from utils.mediator import mediator
from Order.src.infrastructure.outbox.tasks import process_outbox_task

def handle_outbox_triggered(_: OutboxTriggered):
    process_outbox_task.delay()

mediator.register(OutboxTriggered, handle_outbox_triggered)