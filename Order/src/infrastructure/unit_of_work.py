from sqlalchemy.ext.asyncio import AsyncSession
from Order.src.domain.repositories.unit_of_work import IUnitOfWork
from src.infrastructure.repositories.sqlalchemy_event_store import SqlAlchemyEventStoreRepository

class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.event_store = SqlAlchemyEventStoreRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        await self.event_store.flush_outbox()  # if using an OutboxPublisher
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()