from src.models.product import Product
from src.core.mediator import IRequest, mediator
from src.db.session import get_session
from sqlmodel import delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated
from fastapi import APIRouter
from dataclasses import dataclass

router = APIRouter()

@dataclass
class DeleteProducRequest(IRequest):
	"""
	CreateProduct is a subclass of Product that can be used to create new product instances.
	It inherits all fields from Product and can be extended with additional fields if needed.
	"""
	id: int


async def delete_product_request_handler(
		request: DeleteProducRequest,
		session: Annotated[AsyncSession, Depends(get_session)]
		) -> bool:
	
	await session.execute(delete(Product).where(Product.id == request.id))
	return True

mediator.register_request_handler(DeleteProducRequest, delete_product_request_handler)


@router.delete("/products/{product_id}", response_model=bool, summary="Get Products", description="Retrieve a list of products with pagination support.")
async def get_product_endpoint(product_id: int, session: AsyncSession = Depends(get_session)) -> bool:
	"""
	Endpoint to create a new product.
	:param request: The request containing product data.
	:param session: The database session.
	:return: The created product response.
	"""
	request = DeleteProducRequest(id=product_id)
	return await mediator.send(request, session=session)
