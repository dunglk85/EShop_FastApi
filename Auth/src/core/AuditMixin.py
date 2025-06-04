from datetime import datetime, timezone
from sqlmodel import Field
from typing import Optional

class AuditMixin:
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)
