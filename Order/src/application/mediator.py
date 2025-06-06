from typing import Any, Dict, Type, Callable, Awaitable, List
import asyncio

class IRequest:
    pass

class IEvent:
    pass

class IMediator:
    async def send(self, request: IRequest) -> Any:
        raise NotImplementedError

    async def publish(self, event: IEvent) -> None:
        raise NotImplementedError

class Mediator(IMediator):
    def __init__(self):
        self._request_handlers: Dict[Type[IRequest], Callable[[IRequest], Awaitable[Any]]] = {}
        self._event_handlers: Dict[Type[IEvent], List[Callable[[IEvent], Awaitable[None]]]] = {}

    def register_request_handler(self, request_type: Type[IRequest], handler: Callable[[IRequest], Awaitable[Any]]):
        self._request_handlers[request_type] = handler

    def register_event_handler(self, event_type: Type[IEvent], handler: Callable[[IEvent], Awaitable[None]]):
        self._event_handlers.setdefault(event_type, []).append(handler)

    async def send(self, request: IRequest, **kwargs) -> Any:
        handler = self._request_handlers.get(type(request))
        if not handler:
            raise Exception(f"No handler registered for {type(request)}")
        return await handler(request, **kwargs)

    async def publish(self, event: IEvent) -> None:
        handlers = self._event_handlers.get(type(event), [])
        await asyncio.gather(*(handler(event) for handler in handlers))

_mediator = Mediator()
def get_mediator() -> IMediator:
	return _mediator