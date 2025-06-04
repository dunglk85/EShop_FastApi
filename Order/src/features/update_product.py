from src.models.product import ProductUpdate, Product, ProductPublic
from src.core.mediator import IRequest, IEvent, mediator
from src.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

class UpdateProductRequest(ProductUpdate, IRequest):
	"""
	CreateProduct is a subclass of Product that can be used to create new product instances.
	It inherits all fields from Product and can be extended with additional fields if needed.
	"""
	pass

class UpdateProductResponse(ProductPublic):
	"""
	CreateProductResponse is a subclass of Product that can be used to return the created product instance.
	It inherits all fields from Product and can be used to return additional information if needed.
	"""
	pass

class UpdatedProductEvent(IEvent):
	"""
	CreatedProductEvent is an event that is triggered when a new product is created.
	It can be used to notify other parts of the system about the creation of a new product.
	"""
	def __init__(self, product: ProductUpdate):
		self.product = product

async def update_product_request_handler(
		request: UpdateProductRequest,
		session: Annotated[AsyncSession, Depends(get_session)],
		product_id: int
		) -> ProductPublic:
	"""
	Handle the creation of a new product.
	:param request: The request containing product data.
	:return: The created product response.
	"""
	product = await session.get(Product, product_id)  # Fetch the product by ID
	if not product:
		raise ValueError(f"Product with ID {product_id} not found")
	product_data = request.model_dump(exclude_unset=True)
	product.sqlmodel_update(product_data)  # Update the product with new data
	session.add(product)
	await session.commit()
	await mediator.publish(UpdatedProductEvent(product=product))  # Publish the event after creation
	return product  # Simulating ID assignment

mediator.register_request_handler(UpdateProductRequest, update_product_request_handler)

async def updated_product_event_1_handler(
		event: UpdatedProductEvent,
	) -> None:
	"""
	Handle the creation of a new product.
	:param request: The request containing product data.
	:param session: The database session.
	:return: The created product response.
	"""
	print(f"Product created with ID: {event.product.id}, Name: {event.product.name}")
mediator.register_event_handler(UpdatedProductEvent, updated_product_event_1_handler)

async def updated_product_event_2_handler(
		event: UpdatedProductEvent,
	) -> None:
	"""
	Handle the creation of a new product.
	:param request: The request containing product data.
	:param session: The database session.
	:return: The created product response.
	"""
	print(f"Another handler for product creation with ID: {event.product.id}, Name: {event.product.name}")
	
mediator.register_event_handler(UpdatedProductEvent, updated_product_event_2_handler)

@router.patch("/products/{product_id}", summary="Update Product", description="Update product with the provided details.")
async def update_product_endpoint(product_id: int, request: UpdateProductRequest, session: AsyncSession = Depends(get_session)):
	"""
	Endpoint to create a new product.
	:param request: The request containing product data.
	:param session: The database session.
	:return: The created product response.
	"""
	product = await mediator.send(request, session=session, product_id=product_id)
	return JSONResponse(content=product.dict(), status_code=200)
