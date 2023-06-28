from __future__ import annotations
from pathlib import Path
from typing import NoReturn, Optional, Callable, Union
import json
from loguru import logger
from baseline.epicrisis.file import FileFactory
from baseline.epicrisis.epicrisis import Epicrisis, EpicrisisFactory
from baseline.tools.constants import SESSION_IS_ONLY_SAVE_FILES
import baseline.session.session as m_session
from baseline.session.connection.connection import ConnectionAbstract
from baseline.session.connection.websocket import Websocket
from baseline.session.connector import exceptions
from baseline.session.connector.session_connector_abstract import SessionConnectorAbstract
from baseline.session.dto import input as dto_input
from baseline.session import exception

from baseline.solution import Marker


class SessionWebsocketConnector(SessionConnectorAbstract):
    _platform_connection: ConnectionAbstract
    _session: m_session.Session

    __callback_after_connect: Optional[Callable] = None

    # can reinit in start and reconnect event
    _logger = logger

    def __init__(self, session: m_session.Session):
        super().__init__(session)

        self._platform_connection = Websocket()

        self._subscribe()

    async def start(self) -> NoReturn:
        if self._session and self._session.id:
            self._logger.error('Previous session is still active. Try to use "reconnect" command')
            raise exceptions.StartSessionError(
                f'Session is exists, id={self._session.id}. Try to use reconnect command')

        async def emit_start():
            # @todo need detect if use start 2 times, because connect can reconnect active session
            self._logger.debug('Emitting session-start after namespace connection')
            await self._platform_connection.emit(
                'session-start',
                options.prepare_to_command()
            )

        options = self._session.options
        self.__callback_after_connect = emit_start

        await self._platform_connection.connect()
        self._logger.info('Start command init')

        self._logger.debug('Start session options', data=options)
        if self._platform_connection.is_connected() and options:
            self._logger.debug('Baseline was connected and run loop')
            await self._platform_connection.wait()
        else:
            self._logger.error(
                'Baseline was not connected or start options are empty', data={
                    'connect': self._platform_connection.is_connected(),
                    'options': options
                }
            )
            raise exceptions.StartSessionError('Baseline was not connected or start options are empty')

    async def abort(self):
        async def emit_abort():
            await self._platform_connection.emit('session-client-abort')

        self.__callback_after_connect = emit_abort

        await self._platform_connection.connect()
        self._logger.info('Abort command init')
        await self._platform_connection.wait()

    async def reconnect(self):
        await self._platform_connection.connect()
        self._logger.info('Reconnect command init')

        async def emit_reconnect():
            await self._platform_connection.emit('session-reconnect')

        self.__callback_after_connect = emit_reconnect

        await self._platform_connection.wait()

    async def send_file(self, epicrisis: Epicrisis, solution: list[dict[str, Union[int, str]]]) -> None:
        self._logger.debug('Emit session-file-send', self._platform_connection.is_connected())
        if self._platform_connection.is_connected():
            self._logger.info(f'Sending epicrisis id={epicrisis.epicrisis_id} during session id={self._session.id}')
            await self._platform_connection.emit(
                'session-send-file-result',
                {
                    'sessionId': self._session.id,
                    'epicrisisId': epicrisis.epicrisis_id,
                    'taskId': epicrisis.task_id,
                    # @todo сделать передачу словаря, а не json-строки
                    'answer': solution
                }
            )
        else:
            self._logger.error('An error occured during sending of epicrisis due to connection lost.')
            raise exceptions.NotConnectedError('WS is not connected')

    async def get_file(self) -> None:
        # not implement on platform
        # here emit event for get active file in session
        pass

    def _subscribe(self):
        self._logger.debug('Subscribing on events')
        self.__subscribe_handlers_default()
        self.__subscribe_handlers_session()
        self.__subscribe_handlers_file()

    def __subscribe_handlers_default(self):
        self._platform_connection.on('connect', self.__handler_connect)
        self._platform_connection.on('disconnect', self.__handler_disconnect)

    def __subscribe_handlers_session(self):
        self._platform_connection.on('connection-auth-error', self.__handler_connection_auth_error)

        self._platform_connection.on('session-start-success', self.__handler_session_start_success)
        self._platform_connection.on('session-start-error', self.__handler_session_start_error)

        self._platform_connection.on('session-reconnect-success', self.__handler_session_reconnect_success)
        self._platform_connection.on('session-reconnect-error', self.__handler_session_reconnect_error)
        self._platform_connection.on('session-auto-reconnect-error', self.__handler_session_auto_reconnect_error)

        self._platform_connection.on('session-close', self.__handler_session_close)

        self._platform_connection.on('session-client-abort-success', self.__handler_session_abort_success)
        self._platform_connection.on('session-client-abort-error', self.__handler_session_abort_error)

    def __subscribe_handlers_file(self):
        self._platform_connection.on('session-send-next-file', self.__handler_file_available)
        self._platform_connection.on('session-file-send-success', self.__handler_file_send_success)
        self._platform_connection.on('session-file-send-error', self.__handler_file_send_error)

    """
        Handlers for a websocket event
    """

    async def __handler_connect(self):
        self._logger.info(f'Connected on [/pku] namespace.')
        await self.__call_after_connect()

    async def __call_after_connect(self):
        """
        Хак! для старой (4.6) версии пакета python-socketio
        Проблема заключается в том, что нет ожидания подключения к неймспейсу /pku
        В результате чего emit в неймспейс не проходят, т.к. выполняются раньше коннекта
        Сделал отложенный вызов функции с замыканием, чтобы он сработал при подключении в неймспейс
        С v5.0.4 проблема решена в пакете

        @todo обновить пакет python-socketio до последней версии после выхода поддержки 3го протокола socketio в платформе
        @link: https://github.com/nestjs/nest/issues/5676
        @todo добавить после обновления пакета в вызов self._client.connect параметр wait=True
        @https://python-socketio.readthedocs.io/en/latest/api.html#socketio.Client.connect

        :return: None
        """
        if self.__callback_after_connect is not None:
            self._logger.debug(f'There is callback with emit, name={self.__callback_after_connect.__name__}')
            try:
                self._logger.info(f'Call {self.__callback_after_connect.__name__}')
                await self.__callback_after_connect()
            except Exception:
                # @todo catch correct errors
                self._logger.exception('Error after connect callback')
            finally:
                self.__callback_after_connect = None

    async def __handler_disconnect(self):
        self._logger.info(f'Disconnected on [/pku] namespace.')

    async def __handler_connection_auth_error(self, data: dict):
        self._logger.debug('__handler_connection_auth_error', data=data)
        message_dto = dto_input.MessageDto(**data)
        self._logger.info(f'Handle auth error. Message: {message_dto.message}')
        self._logger.error('Authotization failed. Please check your token. Disconnect!')
        await self._platform_connection.disconnect()

    def __handler_session_start_success(self, data: dict) -> NoReturn:
        self._logger.debug('__handler_session_start_success', data=data)
        session = dto_input.SessionStartSuccessDto(session_id=data.get('sessionId'))

        if self._session is None:
            self._logger.error('Session does not exist. Correction of init session entity needed.')
            raise exception.SessionNotExistError('Event: session-start-success. Session is None')

        self._logger.success(f'Session id={session.session_id} was started successfuly.')
        self._session.id = session.session_id
        # add context on log message
        self._logger = self._logger.bind(session=self._session.id)

    async def __handler_session_start_error(self, data: dict) -> NoReturn:
        self._logger.debug('__handler_session_start_error', data=data)
        message_dto = dto_input.MessageDto(**data)

        self._logger.error(f'Session was not started. Message: {message_dto.message}')
        self._logger.info(f'Session was not started, check init params. Disconnect!')
        await self._platform_connection.disconnect()

    def __handler_session_reconnect_success(self, data: dict):
        self._logger.debug('__handler_session_reconnect_success', data=data)
        session = dto_input.SessionStartSuccessDto(session_id=data.get('sessionId'))

        self._logger.success(f'Reconnect to session id={session.session_id}')
        if self._session.id is None:
            self._session.id = session.session_id
        # add context on log message
        self._logger = self._logger.bind(session=self._session.id)
        # todo add confirm connection

    async def __handler_session_reconnect_error(self, data: dict):
        self._logger.debug('__handler_session_reconnect_error', data=data)
        message_dto = dto_input.MessageDto(**data)
        self._logger.error('Attempt to reconnect to the active session was failed. '
                           + f'Reason: {message_dto.message}. '
                           + 'Disconnect.')
        await self._platform_connection.disconnect()

    async def __handler_session_auto_reconnect_error(self, data: dict):
        """
        When try reconnect in connect event
        :param data: data sent by the platform
        """
        self._logger.debug('__handler_session_auto_reconnect_error', data=data)
        message_dto = dto_input.MessageDto(**data)
        self._logger.info('Attempt to auto reconnect to the active session was failed. '
                          + f'Reason: {message_dto.message}. '
                          + 'Wait reconnect or stop the application (press Ctrl+C to interrupt.)')

    async def __handler_session_abort_success(self, data: dict):
        self._logger.debug('__handler_session_abort_success', data=data)
        message_dto = dto_input.MessageDto(**data)

        self._logger.success(f'Session {self._session.id} aborted. Message: {message_dto.message}.')
        self._logger.info('Reset connect params and disconnect')
        self._session.reset()
        await self._platform_connection.disconnect()

    async def __handler_session_abort_error(self, data: dict):
        self._logger.debug('__handler_session_abort_error', data=data)
        message_dto = dto_input.MessageDto(**data)
        self._logger.error(f'An error was occurred during the session abort. Message: {message_dto.message}.')
        self._logger.info(f'Abort command returned an error, try again. Disconnect.')
        await self._platform_connection.disconnect()

    async def __handler_session_close(self, data: dict):
        self._logger.debug('__handler_session_close', data=data)
        self._logger.success(f'Session id={self._session.id} is finished!')
        self._session.reset()
        await self._platform_connection.disconnect()

    async def __handler_file_available(self, data: dict) -> NoReturn:
        """
        When the platform send available epicrisis in current session
        :param data: data with epicrisis id and content
        """
        self._logger.debug('__handler_file_available', data=data)

        if not (data.get('sessionId') and data.get('epicrisisId') and data.get('awsLink') and data.get('timeoutFile')):
            raise ValueError('In available epicrisis absent "epicrisisId" '
                             'or "sessionId" or "awsLink" fields or "timeoutFile"')

        session_file = dto_input.SessionFileDto(
            session_id=data.get('sessionId'),
            epicrisis_id=data.get('epicrisisId'),
            version_id=data.get('versionId'),
            team_id=data.get('teamId'),
            task_id=data.get('taskId'),
            session_type_code=data.get('sessionTypeCode'),
            aws_link=data.get('awsLink'),
        )
        self._logger.info(
            f'Epicrisis id={session_file.task_id} is available during session id={self._session.id}'
        )

        epicrisis = await self.__create_epicrisis(session_file)

        self._logger.info(
            f'SESSION_IS_ONLY_SAVE_FILES id={SESSION_IS_ONLY_SAVE_FILES}'
        )

        if not SESSION_IS_ONLY_SAVE_FILES:
            solution = await self.__create_solution(epicrisis, data.get('timeoutFile'))
            if solution:
                self._logger.info(f'Solution find. Try to send this to platform.')
                await self.send_file(epicrisis, solution)

    async def __handler_file_send_success(self, data: dict) -> NoReturn:
        self._logger.debug('__handler_file_send_success', data=data)
        send_result_dto = dto_input.SessionFileSendDto(
            session_id=data.get('sessionId'),
            task_id=data.get('taskId'),
            epicrisis_id=data.get('epicrisisId'),
            message=data.get('message') or ''
        )

        self._logger.success(
            f'Task id={send_result_dto.task_id} was accepted by Platform during session id={send_result_dto.session_id}.'
        )

    async def __handler_file_send_error(self, data: dict) -> NoReturn:
        self._logger.debug('__handler_file_send_error', data=data)

        send_result_dto = dto_input.SessionFileSendDto(
            message=data.get('message') or ''
        )
        self._logger.info(
            f'Task id={send_result_dto.task_id} was not accepted or accepted with an error by Platform during session id={self._session.id}. Message: {send_result_dto.message}'
        )

    async def __create_epicrisis(self, session_file_event_info: dto_input.SessionFileDto):
        self._logger.debug(f'Get info for ={session_file_event_info.task_id}')
        epicrisis = EpicrisisFactory.get_instance(session_file_event_info)
        await self.__save_epicrisis(epicrisis, 'input')
        self._logger.debug(
            f'Epicrisis id={epicrisis.epicrisis_id} was created and saved to input dir during session id={self._session.id}',
            session_id=self._session.id,
            epicrisis_id=epicrisis.epicrisis_id)
        return epicrisis

    async def __create_solution(self, epicrisis: Epicrisis, timeoutFile: int) -> list[dict[str, Union[int, str]]]:
        self._logger.debug(
            f'Task-epicrisis id={epicrisis.task_id} was marked up during session id={self._session.id}',
        )
        try:
            marker = Marker(epicrisis)
            marked_solution = await marker.markup_async(timeoutFile)
        except Exception as error:
            # @todo конкретизировать ошибки
            self._logger.exception(f'Epicrisis id={epicrisis.task_id} was not marked up. Error: {error}')
        else:
            if marked_solution:
                self._logger.info(f'Marked up epicrisis id={epicrisis.task_id} '
                                  f'was created and saved to output dir during session id={self._session.id}')
                return marked_solution
            else:
                self._logger.info(f'M')

    async def __save_epicrisis(self, epicrisis: Epicrisis, dir_name: str):
        file = FileFactory.create(Path(f'{epicrisis.path_to_xml}'))
        epicrisis.file = file
        epicrisis.save()
