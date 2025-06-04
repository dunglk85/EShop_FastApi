from src.models.product import Product, ProductPublic
from src.core.mediator import IRequest, mediator
from src.db.session import get_session
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Query
from typing import Annotated
from fastapi import APIRouter
from dataclasses import dataclass
from src.core.exception import ResourceNotFoundException

router = APIRouter()

@dataclass
class GetProducRequest(IRequest):
	"""
	CreateProduct is a subclass of Product that can be used to create new product instances.
	It inherits all fields from Product and can be extended with additional fields if needed.
	"""
	id: int


async def get_product_request_handler(
		request: GetProducRequest,
		session: Annotated[AsyncSession, Depends(get_session)]
		) -> ProductPublic:
	
	result = await session.execute(select(Product).where(Product.id == request.id))
	product = result.scalar_one_or_none()
	if product is None:
		raise ResourceNotFoundException(f"Product with ID {request.id} not found.")
	return product

mediator.register_request_handler(GetProducRequest, get_product_request_handler)


@router.get("/products/{product_id}", response_model=ProductPublic, summary="Get Products", description="Retrieve a list of products with pagination support.")
async def get_product_endpoint(product_id: int, session: AsyncSession = Depends(get_session)) -> ProductPublic:
	"""
	Endpoint to create a new product.
	:param request: The request containing product data.
	:param session: The database session.
	:return: The created product response.
	"""
	request = GetProducRequest(id=product_id)
	product = await mediator.send(request, session=session)
	return product
