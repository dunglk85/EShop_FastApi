from sqlmodel import SQLModel, Field
from src.core import AuditMixin

class ProductBase(SQLModel):
    name: str
    description: str = None
    price: float

class Product(ProductBase, table=True, inherit=True, mixin=AuditMixin):
    id: int = Field(default=None, primary_key=True)

class ProductPublic(ProductBase):
    id: int
