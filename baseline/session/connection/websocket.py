import os
from typing import Any, Final, Callable
import socketio
from loguru import logger

from baseline.tools.constants import IS_DEBUG, SESSION_WS_PROTOCOL_VERSION
from baseline.session.connection.connection import ConnectionAbstract


class Websocket(ConnectionAbstract):
    _client: 'socketio.AsyncClient'

    __host: str = 'https://aimdoc-back.172.16.10.154.nip.io'
    __token: str
    __version: int = 2

    __namespace: Final[str] = '/baseline'

    __client_params = {
        'reconnection': True,
        'reconnection_attempts': 3000,
        'reconnection_delay': 1,  # how long to initially wait before attempting a new reconnection
        'reconnection_delay_max': 3000,
        'randomization_factor': 0.5,
        'ssl_verify': False,
    }

    def __init__(self):
        self.__prepare_init_properties()

        self._client = socketio.AsyncClient(**self.__client_params)

        self._register_default_handlers()

    def is_connected(self) -> bool:
        return self._client.connected

    def on(self, event, fn: Callable) -> 'Websocket':
        self._client.on(event, fn, namespace=self.__namespace)
        return self

    async def connect(self):
        logger.debug('self.__namespace')
        logger.debug(self.__namespace)
        logger.debug(self.__version)
        await self._client.connect(
            f'{self.__host}?token={self.__token}&version={self.__version}',
            transports=['websocket'],
            namespaces=[self.__namespace],
        )

    async def disconnect(self):
        await self._client.disconnect()

    async def wait(self):
        logger.debug('Wait socketio loop')
        await self._client.wait()

    async def emit(self, event, data: Any = None, callback: Callable = None) -> 'Websocket':
        logger.debug(f'Emit {event}', data=data)
        await self._client.emit(event=event, data=data, namespace=self.__namespace, callback=callback)
        return self

    def __prepare_init_properties(self):
        if IS_DEBUG:
            self.__client_params['logger'] = logger
            self.__client_params['engineio_logger'] = logger

        if 'HOST' not in os.environ:
            raise EnvironmentError('HOST is not defined, check your .env file')

        if 'TOKEN' not in os.environ:
            raise EnvironmentError('TOKEN is not defined, check your .env file')

        self.__host = os.environ['HOST']
        self.__token = os.environ['TOKEN']
        self.__version = SESSION_WS_PROTOCOL_VERSION

    async def __connect(self):
        logger.info(f'Connected on default [/] namespace. sid={self._client.sid}')

    async def __disconnect(self):
        logger.info(f'Disconnected on default [/] namespace. sid={self._client.sid}')

    async def __connect_error(self, message):
        logger.info(f'Connect_error on default [/] namespace. sid={self._client.sid}. Message: {message}')

    def _register_default_handlers(self):
        self._client.on('connect', self.__connect)
        self._client.on('disconnect', self.__disconnect)
        self._client.on('connect_error', self.__connect_error)

