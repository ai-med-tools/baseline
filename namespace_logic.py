import socketio, os
from cfg_support import get_perfomance
from utils import get_inline_queue, create_dirs_for_session
from baseline_constants import system_logs_path, connect_success_const, disconnect_success_const, abort_success_const, abort_error_const
from baseline_constants import connection_auth_error_const, session_start_error_const, session_start_success_const, reconnect_success_const, session_start_blank_const
import mureq
from cfg_support import set_current_session_id
from cfg_support import set_current_task_id
from cfg_support import set_current_epicrisis_id
from cfg_support import set_current_epicrisis_path
from cfg_support import get_current_input_path
from cfg_support import get_current_test_path
from state_log import logger
import datetime as dt


class BaselineNamespace(socketio.ClientNamespace):
    def on_connect(self):
        logger.info(connect_success_const)
        pass

    def on_disconnect(self):
        logger.info(disconnect_success_const)
        pass

    def on_connection_auth_error(self, data):
        logger.info(connection_auth_error_const)

        qi = get_inline_queue()
        qi.put(data)

    def on_session_start_error(self, data):
        # error_default = session_start_error_const
        # if data["message"] and data["message"] != "":
        #     error_default["message"] = data["message"]
        logger.info(session_start_error_const)

        if data["message"] and data["message"] != "":
            session_start_error_const["message"] = data["message"]

        qi = get_inline_queue()
        qi.put(session_start_error_const)

    def on_session_start_success(self, data):
        set_current_session_id(str(data["sessionId"]))

        create_dirs_for_session(str(data["sessionId"]))

        logger.info(session_start_success_const)
        logger.info(data["sessionId"])

        qi = get_inline_queue()
        qi.put(session_start_success_const)

    def on_session_send_next_file(self, data):
        try:
            a = dt.datetime.now()
            set_current_session_id(str(data["sessionId"]))

            logger.info(
                dict(
                    op='file-income',
                    status='success',
                    message=f'Epicrisis sent from the platform - ID - {data["epicrisisId"]}, Version - {data["versionId"]}, TaskId - {data["taskId"]}'
                )
            )

            set_current_epicrisis_id(str(data["epicrisisId"]))
            set_current_task_id(str(data["taskId"]))

            perfomance = get_perfomance()
            input_path = get_current_input_path()

            current_epicrisis_path = os.path.join(input_path,
                                                  f'{data["epicrisisId"]}_{data["versionId"]}_{data["taskId"]}.xml')
            set_current_epicrisis_path(current_epicrisis_path)

            payload = {'baselineToken': perfomance["token"], 'epicrisisId': data["epicrisisId"]}
            response = mureq.get(perfomance["download_host"], params=payload)

            with open(current_epicrisis_path, 'wb') as file:
                file.write(response.content)

            b = dt.datetime.now()
            less = (b-a).total_seconds()
            logger.info(
                dict(
                    op='file-income',
                    status='success',
                    message=f'Finish write file - ID - {data["epicrisisId"]}, Version - {data["versionId"]}, TaskId - {data["taskId"]}'
                )
            )
            logger.info(
                dict(
                    op='file-download-time',
                    status='success',
                    message=f'Download time in seconds - {less}'
                )
            )
            response = mureq.post(perfomance["download_host"]+'/receive-callback',
                                  json={'token': perfomance["token"], 'epicrisisId': data["epicrisisId"]})
            if response.status_code == 201:
                logger.info(dict(op='file-received-callback', status='success'))
            else:
                raise Exception
        except Exception as e:
            logger.info(dict(op='file-received-callback', status='error', error=str(e)))

        pass

    def on_session_reconnect_success(self, data):
        logger.info(
            dict(
                op='reconnect-status',
                status='success',
                message=f'Session - {data["sessionId"]} - was successfully reconnected.'
            )
        )


    def on_session_close(self, data):
        logger.info(
            dict(
                op='session-finished',
                status='success',
                message=f'Session - was successfully finished.'
            )
        )

    def on_session_blank_start(self):
        logger.info(
            dict(
                op='session-start',
                status='error',
                message=f'The session has already started, skip.'
            )
        )

        qi = get_inline_queue()
        qi.put(session_start_blank_const)


    def on_session_get_test_success(self, data):
        logger.info(
            dict(
                op='session-get-test',
                status='success',
                message=f'Get test for epicrisis is success. Download test'
            )
        )

        perfomance = get_perfomance()
        test_path = get_current_test_path()

        current_test_path = os.path.join(test_path, f'{data["epicrisisId"]}_{data["taskId"]}_{data["testId"]}.xml')

        payload = {'baselineToken': perfomance["token"], 'epicrisisId': data["epicrisisId"], 'testId': data["testId"]}
        response = mureq.get(perfomance["download_host"]+'/fragment', params=payload)

        with open(current_test_path, 'wb') as file:
            file.write(response.content)

        qi = get_inline_queue()
        qi.put(dict(
            op="gettest",
            message="Get epicrisis test success"
        ))

        pass

    def on_session_get_test_error(self, data):
        logger.info(
            dict(
                op='session-get-test',
                status='error',
                message=f'An error occurred while trying to request a study'
            )
        )

        qi = get_inline_queue()
        qi.put(dict(
            op="Get epicrisis test error"
        ))
        pass




