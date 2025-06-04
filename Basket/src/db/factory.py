from src.repository.IRepository import IBasketRepository
from src.repository.redis_repository import RedisBasketRepository
from src.db.redis_client import redis_client

def create_repository() -> IBasketRepository:
    """
    Creates the appropriate repository based on configuration.
    For PostgreSQL: Uses the provided database session
    For DynamoDB: Uses the provided database client
    """
    return RedisBasketRepository(redis_client=redis_client)
