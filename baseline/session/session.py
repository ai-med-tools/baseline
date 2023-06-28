from typing import NoReturn, Optional
from loguru import logger

import baseline.session.connector.session_connector_abstract as connector_abstract
from baseline.session.connector.session_connector_factory import SessionConnectorFactory
from baseline.session.dto import SessionStarterOptions
from baseline.tools.singleton import MetaSingleton
from baseline.epicrisis.epicrisis import Epicrisis, EpicrisisFactory


class Session(metaclass=MetaSingleton):
    _id: Optional[int] = None
    _options: Optional[SessionStarterOptions] = None

    _session_connector: connector_abstract.SessionConnectorAbstract

    def __init__(self):
        self._session_connector = SessionConnectorFactory.get(self)

    async def start(self, options: SessionStarterOptions):
        logger.info('Init start session')
        self._options = options
        await self._session_connector.start()

    async def abort(self):
        await self._session_connector.abort()

    async def reconnect(self):
        await self._session_connector.reconnect()

    async def send_file(self, epicrisis: Epicrisis, answer: str) -> NoReturn:
        await self._session_connector.send_file(epicrisis, answer)

    async def get_file(self) -> NoReturn:
        pass

    @property
    def options(self) -> Optional[SessionStarterOptions]:
        return self._options

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if self._id is None:
            self._id = value
        else:
            raise ValueError('Session id is exist, ')

    def reset(self):
        self._id = None
        self._options = None
