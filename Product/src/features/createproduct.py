from src.models.product import ProductBase, Product
from src.core.mediator import IRequest, IEvent, mediator
#from endpoints import router
from src.db.session import get_session
from sqlmodel import Session
from fastapi import Depends
from typing import Annotated
from fastapi import APIRouter

router = APIRouter()

class CreateProductRequest(ProductBase, IRequest):
	"""
	CreateProduct is a subclass of Product that can be used to create new product instances.
	It inherits all fields from Product and can be extended with additional fields if needed.
	"""
	pass

class CreateProductResponse(ProductBase):
	"""
	CreateProductResponse is a subclass of Product that can be used to return the created product instance.
	It inherits all fields from Product and can be used to return additional information if needed.
	"""
	id: int

class CreatedProductEvent(IEvent):
	"""
	CreatedProductEvent is an event that is triggered when a new product is created.
	It can be used to notify other parts of the system about the creation of a new product.
	"""
	def __init__(self, product: ProductBase):
		self.product = product

async def create_product_request_handler(
		request: CreateProductRequest,
		session: Annotated[Session, Depends(get_session)]
		) -> CreateProductResponse:
	"""
	Handle the creation of a new product.
	:param request: The request containing product data.
	:return: The created product response.
	"""
	product = Product(**request.dict())
	session.add(product)
	session.commit()
	session.refresh(product)
	await mediator.publish(CreatedProductEvent(product=product))  # Publish the event after creation
	return CreateProductResponse(**product.dict())  # Simulating ID assignment

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

@router.post("/products/", response_model=CreateProductResponse)
async def create_product_endpoint(request: CreateProductRequest, session: Session = Depends(get_session)) -> CreateProductResponse:
	"""
	Endpoint to create a new product.
	:param request: The request containing product data.
	:param session: The database session.
	:return: The created product response.
	"""
	product = await mediator.send(request, session=session)
	return product
