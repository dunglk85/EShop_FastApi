from src.application.repositories.command_order_repository import IcommandOrderRepository
from src.domain.models.order import Order
from src.infrastructure.models.event_store import EventStoreRecord
from src.infrastructure.models.out_box import OutboxEventRecord
from src.infrastructure.models.outbox_trigger import OutboxTriggered
from src.infrastructure.db.write_db import get_session
from src.utils.mediator import mediator

from sqlalchemy import text


class CommandOrderRepository(IcommandOrderRepository):
    def __init__(self):
        pass

    async def forward(self, order: Order):
        async for session in get_session():
            try:
                # Get latest version from event store
                result = await session.execute(
                    text(
                        "SELECT MAX(version) FROM event_store WHERE aggregate_id = :aggregate_id"
                    ),
                    {"aggregate_id": str(order.id)},
                )
                latest_version_in_store = result.scalar() or 0
                for i, event in enumerate(order.domain_events):
                    event_version = latest_version_in_store + i + 1
                    event_store = self._get_event_store(event, aggregate_id=order.id.value, version=event_version)
                    session.add(event_store)

                    outbox_event = self._get_outbox_event(event, aggregate_id=order.id.value)
                    # Link outbox event to event store
                    outbox_event.event_id = event_store.id
                    session.add(outbox_event)

                await session.commit()

                # After commit, trigger outbox processor (via mediator)
                await mediator.publish(OutboxTriggered(aggregate_id=order.id.value))

            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    async def get_order_by_id(self, order_id: str) -> Order | None:
        session = await get_session()
        try:
            result = await session.execute(
                text("SELECT * FROM event_store WHERE aggregate_id = :order_id ORDER BY occurred_at"),
                {"order_id": order_id}
            )
            records = result.scalars().all()
            if not records:
                return None

            domain_events = [EventStoreRecord.to_domain_event(record) for record in records]
            return Order.rehydrate(domain_events)
        finally:
            await session.close()

    def _get_event_store(self, event, aggregate_id, version=0) -> EventStoreRecord:
        return EventStoreRecord.from_domain_event(event, aggregate_id, version=version)

    def _get_outbox_event(self, event, aggregate_id=None) -> OutboxEventRecord:
        return OutboxEventRecord.from_domain_event(event, aggregate_id)
