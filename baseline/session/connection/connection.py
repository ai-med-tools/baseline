from abc import ABC, abstractmethod
from typing import NoReturn, Any, Coroutine, Callable


class Connect(ABC):
    @abstractmethod
    async def on(self, event: str, fn: Callable) -> NoReturn:
        pass

    @abstractmethod
    async def emit(self, event: str, data: Any) -> NoReturn:
        pass


class ConnectionAbstract(ABC):
    _client: Connect

    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def on(self, event, fn: Callable) -> 'ConnectionAbstract':
        pass

    @abstractmethod
    async def connect(self) -> Coroutine:
        pass

    @abstractmethod
    async def disconnect(self) -> Coroutine:
        pass

    @abstractmethod
    async def wait(self) -> Coroutine:
        pass

    @abstractmethod
    async def emit(self, event, data: Any = None, callback: Callable = None) -> 'ConnectionAbstract':
        pass

