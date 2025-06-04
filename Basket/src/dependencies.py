# src/dependencies.py
from fastapi import Depends
from src.repository.IRepository import IBasketRepository
from src.services.service import BasketService
from src.db.factory import create_repository

async def get_service(repository: IBasketRepository = Depends(create_repository)) -> BasketService:
    return BasketService(repository)
