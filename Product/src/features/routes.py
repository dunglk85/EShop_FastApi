from fastapi import APIRouter
from .create_product import router as create_product_router
from .get_products import router as get_product_router
from .get_product_byid import router as get_product_by_id_router
from .delete_product import router as delete_product_router

product_router = APIRouter()
product_router.include_router(create_product_router)
product_router.include_router(get_product_router)
product_router.include_router(get_product_by_id_router)
product_router.include_router(delete_product_router)