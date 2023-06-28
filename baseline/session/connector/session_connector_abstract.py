from __future__ import annotations
from abc import ABC, abstractmethod

from baseline.session.connection.connection import ConnectionAbstract
from baseline.epicrisis.epicrisis import Epicrisis, EpicrisisFactory
import baseline.session.session as m_session


class SessionConnectorAbstract(ABC):
    _platform_connection: ConnectionAbstract
    _session: m_session.Session

    def __init__(self, session: m_session.Session) -> None:
        self._session = session

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def abort(self):
        pass

    @abstractmethod
    async def reconnect(self):
        pass

    @abstractmethod
    async def send_file(self, epicrisis: Epicrisis, answer: str) -> None:
        pass

    @abstractmethod
    async def get_file(self) -> None:
        pass
