from dataclasses import dataclass
from typing import Optional

class OutboxTriggered:
    """Notification to trigger outbox processing."""
    def __init__(self, aggregate_id=None):
        self.aggregate_id = aggregate_id