from sqlmodel import SQLModel, Field
from src.core import AuditMixin

class ProductBase(SQLModel):
    name: str = Field(..., min_length=3, max_length=100, index=True)
    description: str = Field(None, max_length=500, index=True)
    price: float = Field(..., gt=0)

class Product(ProductBase, table=True, inherit=True, mixin=AuditMixin):
    id: int = Field(default=None, primary_key=True)

class ProductPublic(ProductBase):
    id: int

class ProductUpdate(SQLModel):
    name: str | None = Field(None, min_length=3, max_length=100, index=True)
    description: str | None = Field(None, max_length=500, index=True)
    price: float | None = Field(None, gt=0)
