from src.models.product import Product, ProductPublic
from src.core.mediator import IRequest, mediator
from src.db.session import get_session
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Query
from typing import Annotated
from fastapi import APIRouter
from dataclasses import dataclass

router = APIRouter()

@dataclass
class GetProductListRequest(IRequest):
	"""
	CreateProduct is a subclass of Product that can be used to create new product instances.
	It inherits all fields from Product and can be extended with additional fields if needed.
	"""
	offset: int = 0
	limit: int = 100


async def get_product_list_request_handler(
		request: GetProductListRequest,
		session: Annotated[AsyncSession, Depends(get_session)]
		) -> list[ProductPublic]:
	"""
	Handle the creation of a new product.
	:param request: The request containing product data.
	:return: The created product response.
	"""
	products = await session.execute(select(Product).offset(offset=request.offset).limit(limit=request.limit))
	return products.scalars().all()

mediator.register_request_handler(GetProductListRequest, get_product_list_request_handler)


@router.get("/products", response_model=list[ProductPublic], summary="Get Products", description="Retrieve a list of products with pagination support.")
async def get_product_list_endpoint(offset: int = 0, limit: int = Query(default=100, le=100), session: AsyncSession = Depends(get_session)) -> list[ProductPublic]:
	"""
	Endpoint to create a new product.
	:param request: The request containing product data.
	:param session: The database session.
	:return: The created product response.
	"""
	request = GetProductListRequest(offset=offset, limit=limit)
	products = await mediator.send(request, session=session)
	return products
