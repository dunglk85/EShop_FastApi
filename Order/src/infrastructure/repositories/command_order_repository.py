from application.repositories.command_order_repository import IcommandOrderRepository
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.order import Order
from infrastructure.models.event_store import EventStoreRecord
from infrastructure.models.out_box import OutboxEventRecord
from utils.mediator import mediator
from infrastructure.models.outbox_trigger import OutboxTriggered
from infrastructure.db.write_db import get_session

class CommandOrderRepository(IcommandOrderRepository):
	def __init__(self):
		pass

	async def forward(self, order):
		session = await get_session()
		try:
			for event in order.domain_events:
				# Process domain events if needed
				event_store = self._get_event_store(event, aggregate_id=order.id)
				session.add(event_store)
				outbox = self._get_outbox_event(event, aggregate_id=order.id)
				outbox.event_id = event_store.id
				session.add(outbox)
			await session.commit()
			mediator.publish(OutboxTriggered(aggregate_id=order.id))
		except Exception as e:
			await session.rollback()
			raise e
		finally:
			await session.close()
		
	async def get_order_by_id(self, order_id):
		"""Retrieve an order by its ID."""
		session = await get_session()
		try:
			event_stores = await session.execute(
				"SELECT * FROM event_store WHERE order_id = :order_id",
				{"order_id": order_id})
			event_records = event_stores.scalars().all()
			if event_records:
				domain_events = [EventStoreRecord.to_domain_event(record) for record in event_records]
				order = Order.rehydrate(domain_events)
				return order
		finally:
			await session.close()
		
	def _get_event_store(self, event, aggregate_id=None):
		# Convert the domain event to an event store entity
		# This is a placeholder implementation; actual implementation will depend on your event store design
		return EventStoreRecord.from_domain_event(event, aggregate_id)
	
	def _get_outbox_event(self, event, aggregate_id=None):
		# Convert the integration event to an outbox event entity
		# This is a placeholder implementation; actual implementation will depend on your outbox design
		return OutboxEventRecord.from_domain_event(event, aggregate_id)