from typing import Any, Dict, Type, Callable, Awaitable, List
import asyncio

class Mediator:
    def __init__(self):
        self._request_handlers: Dict[Type, Callable[..., Awaitable[Any]]] = {}
        self._event_handlers: Dict[Type, List[Callable[..., Awaitable[None]]]] = {}

    def register_request_handler(self, request_type: Type, handler: Callable[..., Awaitable[Any]]):
        self._request_handlers[request_type] = handler

    def register_event_handler(self, event_type: Type, handler: Callable[..., Awaitable[None]]):
        self._event_handlers.setdefault(event_type, []).append(handler)

    async def send(self, request: Any, **kwargs) -> Any:
        handler = self._request_handlers.get(type(request))
        if not handler:
            raise Exception(f"No handler registered for {type(request)}")
        return await handler(request, **kwargs)

    async def publish(self, event: Any) -> None:
        handlers = self._event_handlers.get(type(event), [])
        await asyncio.gather(*(handler(event) for handler in handlers))

# Global mediator instance
mediator = Mediator()