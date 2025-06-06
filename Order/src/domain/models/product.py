from typing import Optional
from src.domain.abstraction.entity import Entity
from src.domain.value_objects.ids import ProductId

class Product(Entity[ProductId]):
	def __init__(self, id: ProductId, name: str, description: Optional[str] = None, price: float = 0.0):
		if not name or not name.strip():
			raise ValueError("Product name cannot be empty.")
		if price < 0:
			raise ValueError("Product price cannot be negative.")
		
		super().__init__(id=id)
		self._name = name
		self._description = description
		self._price = price

	@property
	def name(self) -> str:
		return self._name

	@property
	def description(self) -> Optional[str]:
		return self._description

	@property
	def price(self) -> float:
		return self._price