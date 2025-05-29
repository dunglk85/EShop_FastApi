from src.models.product import ProductBase, Product, ProductPublic
from src.core.mediator import IRequest, IEvent, mediator
from src.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

class CreateProductRequest(ProductBase, IRequest):
	"""
	CreateProduct is a subclass of Product that can be used to create new product instances.
	It inherits all fields from Product and can be extended with additional fields if needed.
	"""
	pass

class CreateProductResponse(ProductPublic):
	"""
	CreateProductResponse is a subclass of Product that can be used to return the created product instance.
	It inherits all fields from Product and can be used to return additional information if needed.
	"""
	pass

class CreatedProductEvent(IEvent):
	"""
	CreatedProductEvent is an event that is triggered when a new product is created.
	It can be used to notify other parts of the system about the creation of a new product.
	"""
	def __init__(self, product: ProductBase):
		self.product = product

async def create_product_request_handler(
		request: CreateProductRequest,
		session: Annotated[AsyncSession, Depends(get_session)]
		) -> ProductPublic:
	"""
	Handle the creation of a new product.
	:param request: The request containing product data.
	:return: The created product response.
	"""
	product = Product(**request.dict())
	session.add(product)
	await session.commit()
	await session.refresh(product)
	await mediator.publish(CreatedProductEvent(product=product))  # Publish the event after creation
	return product  # Simulating ID assignment

async def created_product_event_1_handler(
		event: CreatedProductEvent,
	) -> None:
	"""
	Handle the creation of a new product.
	:param request: The request containing product data.
	:param session: The database session.
	:return: The created product response.
	"""
	print(f"Product created with ID: {event.product.id}, Name: {event.product.name}")
mediator.register_event_handler(CreatedProductEvent, created_product_event_1_handler)

async def created_product_event_2_handler(
		event: CreatedProductEvent,
	) -> None:
	"""
	Handle the creation of a new product.
	:param request: The request containing product data.
	:param session: The database session.
	:return: The created product response.
	"""
	print(f"Another handler for product creation with ID: {event.product.id}, Name: {event.product.name}")
	
mediator.register_event_handler(CreatedProductEvent, created_product_event_2_handler)

mediator.register_request_handler(CreateProductRequest, create_product_request_handler)

@router.post("/products", summary="Create Product", description="Create a new product with the provided details.")
async def create_product_endpoint(request: CreateProductRequest, session: AsyncSession = Depends(get_session)):
	"""
	Endpoint to create a new product.
	:param request: The request containing product data.
	:param session: The database session.
	:return: The created product response.
	"""
	product = await mediator.send(request, session=session)
	return JSONResponse(content=product.dict(), status_code=201)
