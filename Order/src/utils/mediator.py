from typing import Type, Callable, Dict, List

class Mediator:
    def __init__(self):
        self._handlers: Dict[Type, List[Callable]] = {}

    def register(self, event_type: Type, handler: Callable):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event):
        for handler in self._handlers.get(type(event), []):
            handler(event)

mediator = Mediator()