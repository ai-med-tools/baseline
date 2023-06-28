from __future__ import annotations

import baseline.session.session as m_session
from .session_connector_abstract import SessionConnectorAbstract
from .session_websocket_connector import SessionWebsocketConnector


class SessionConnectorFactory:
    @staticmethod
    def get(session: m_session.Session) -> SessionConnectorAbstract:
        return SessionWebsocketConnector(session)
