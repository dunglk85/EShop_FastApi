from typing import Optional
from src.domain.abstraction.entity import Entity
from src.domain.value_objects.ids import CustomerId

class Customer(Entity[CustomerId]):
	def __init__(self, id: CustomerId, name: str, email: str, phone: Optional[str] = None):
		if not name or not name.strip():
			raise ValueError("Customer name cannot be empty.")
		if not email or not email.strip():
			raise ValueError("Customer email cannot be empty.")
		super().__init__(id=id)
		self._name = name
		self._email = email
		self._phone = phone

	@property
	def name(self) -> str:
		return self._name

	@property
	def email(self) -> str:
		return self._email

	@property
	def phone(self) -> Optional[str]:
		return self._phone