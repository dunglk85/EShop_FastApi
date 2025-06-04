from abc import ABC, abstractmethod

class MessageBus(ABC):
    @abstractmethod
    async def publish(self, event_type: str, payload: dict):
        """
		Publish an event to the message bus.
		
		:param event_type: The type of the event to publish.
		:param payload: The data associated with the event.
		"""
        pass
    
    @abstractmethod
    async def start(self):
        pass
    @abstractmethod
    async def stop(self):
        pass
