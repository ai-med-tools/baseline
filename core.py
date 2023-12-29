from ipcqueue import posixmq
from cfg_support import get_perfomance
import threading
import json
import os
import daemon, socketio, logging
from namespace_logic import BaselineNamespace
from baseline_constants import session_start_success_const, system_logs_path, main_process_start_success_const, main_process_abort_success_const
import logging

sio = socketio.Client({
    'reconnection': True,
    'upgrade': False,
    'ssl_verify': False,
})

sio.register_namespace(BaselineNamespace('/baselinemrdtcgmegy'))

main_dir = os.path.dirname(os.path.abspath(__file__))
def native_baseline_queue():
    q = posixmq.Queue('/baseline')
    qi = posixmq.Queue('/inline')
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, filename=system_logs_path, filemode="w")
    logger = logging.getLogger('main_baseline_logger')
    logger.info(main_process_start_success_const)

    while True:
        msg = q.get()
        if msg["op"] == "start":
            # logger.info("Try to start session.")
            sio.emit('session-start', msg["data"], "/baselinemrdtcgmegy")

        if msg["op"] == "start-blank":
            logger.info(
                dict(
                    op='session-start',
                    status='error',
                    message=f'The session has already started, skip.'
                )
            )
            # sio.emit("session-client-abort", "", "/baseline")

        if msg == 'status':
            socket_status = dict(op='status', websocket_status=sio.connected)
            qi.put(socket_status)
            # logger.info(socket_status)
        if msg["op"] == 'gettest':
            try:
                logger.info(dict(op="Attempt to request research", epicrisisId=msg["data"]["epicrisisId"],
                                 sessionId=msg["data"]["sessionId"], testId=msg["data"]["testId"]))
                sio.emit("session-get-test", msg["data"], "/baselinemrdtcgmegy")

            except Exception as e:
                logger.info(dict(op="Error when send file", error=str(e)))

        print(msg)
        print(msg['op'])


if __name__ == "__main__":
    perfomance = get_perfomance()
    # thread = threading.Thread(target=native_baseline_queue)
    # thread.daemon = True
    # thread.start()
    # thread.join()
    with daemon.DaemonContext():
        thread = threading.Thread(target=native_baseline_queue)
        thread.daemon = True
        thread.start()

        sio.connect(f'{perfomance["aimed_host"]}?token={perfomance["token"]}', namespaces=['/baselinemrdtcgmegy'], transports=['websocket'])
