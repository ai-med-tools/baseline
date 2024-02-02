import fire, os, json, psutil
import mureq
from ipcqueue import posixmq
from baseline_constants import session_start_success_const, solution_file_doesnt_exist_const
from baseline_constants import data_not_resolved_const
from cfg_support import get_current_session_id
from cfg_support import get_current_epicrisis_id
from cfg_support import get_current_task_id
from validator import Validator, NotJsonContentInFileError, TooManyObjectsInTheArrayError
from validator import JsonIsEmpty, StructureJsonIsIncorrect, LimitKeysInJson
from cfg_support import get_perfomance
import socketio
import datetime as dt
from push_log import logger


class BaselineCommands(object):
    def __init__(self):
        self.main_input_queue = posixmq.Queue('/baseline')
        self.main_output_queue = posixmq.Queue('/inline')

    def core(self):
        perfomance = get_perfomance()

        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline() == ['python', 'core.py']:
                pid = proc.pid
        if pid:
            print("Baseline process is already started. PID - " + str(pid))
            return

        try:
            # standard Python
            ping = 'ping'
            sio = socketio.Client()
            sio.connect(f'{perfomance["aimed_host"]}?token={perfomance["token"]}&ping={ping}',
                        namespaces=['/baselinemrdtcgmegy'],
                        transports=['websocket'], wait=True, wait_timeout=3)
            sio.disconnect()
        except Exception as e:
            print(e)
            print(f'Please check the correctness of the entered address in the creds.cfg file or contact'
                  f' the platform administrator.'
                  f' The platform does not respond to connection requests over WS.')
            return

        try:
            os.system('python core.py')
            print(f'Core start successfully.')
        except Exception as error:
            print(error)
            print(f'An error occurred while starting the core.')

    def kill(self):
        try:
            pid = None
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                if proc.cmdline() == ['python', 'core.py']:
                    proc.kill()
            print("Core successfully killed.")
        except:
            print("An exception occurred.")

    def start(self, contest, stage, type, count=None, timeout=None, nosology=None):
        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline() == ['python', 'core.py']:
                pid = proc.pid
        if not pid:
            print(f'Baseline CORE was not started, the command cannot be executed')
            return

        print(contest, stage, type, count, timeout, nosology)
        if type not in ["training", "estimated-training"]:
            print(type)
            if count or timeout:
                print(f'Parameter setting is allowed only in the training session.')
                return

        if contest in ["doctor"]:
            if type in ["training"]:
                if not count:
                    count = 100

        if type in [ "estimated-training"]:
            if count:
                print(f'Parameter count cannot be specified in this session type.')
                return
        nosology_string = ''
        if nosology:
            if isinstance(nosology, int):
                nosology_string = str(nosology)
            else:
                nosology_string = ','.join(map(str,nosology))

        initial_params = dict(
            op='start',
            data={
                'contest': contest,
                'params': {
                    'stage': stage,
                    'sessionType': type,
                }
            }
        )
        if count:
            initial_params["data"]["params"]["countFiles"] = count

        if timeout:
            initial_params["data"]["params"]["time"] = timeout

        if nosology_string != "":
            initial_params["data"]["params"]["nosologyString"] = nosology_string

        self.main_input_queue.put(
            initial_params,
            priority=1
        )

        answer = self.main_output_queue.get()

        print(answer)
        pass

    def send(self, path, taskid):
        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline() == ['python', 'core.py']:
                pid = proc.pid
        if not pid:
            print(f'Baseline CORE was not started, the command cannot be executed')
            return

        check_file = os.path.isfile(path)
        if not check_file:
            print(solution_file_doesnt_exist_const)
            return

        if not taskid:
            print(f'taskid is required argument, the command cannot be executed')
            return

        currentsessionid = get_current_session_id()
        currentepicrisisid = get_current_epicrisis_id()
        currenttasksid = get_current_task_id()

        if not currentsessionid or not currentepicrisisid or not currenttasksid:
            print(data_not_resolved_const)
            return

        try:
            validator = Validator(path)
            validator.validate()
        except NotJsonContentInFileError as nje:
            print(nje)
            return
        except TooManyObjectsInTheArrayError as tmo:
            print(tmo)
            return
        except JsonIsEmpty as jie:
            print(jie)
            return
        except StructureJsonIsIncorrect as sjii:
            print(sjii)
            return
        except LimitKeysInJson as lkij:
            print(lkij)
            return 

        try:
            a = dt.datetime.now()
            perfomance = get_perfomance()
            main_dir = os.path.dirname(os.path.abspath(__file__))
            check_file = os.path.join(main_dir, path)
            with open(check_file, 'r') as f:
                solution_raw_content = f.read()

            solution_from_file = json.loads(solution_raw_content)
            response = mureq.post(perfomance["download_host"] + '/upload-result',
                                  json={'token': perfomance["token"], 'taskId': taskid, 'answer': solution_from_file})
            b = dt.datetime.now()
            less = (b-a).total_seconds()
            if response.status_code == 201:
                logger.info(dict(op='file-send', status='success',
                            message=dict(session=currentsessionid, task=taskid, time=less)))
                print(f'File {currentepicrisisid} - successfuly sent. Upload time -  {less}')
                return
            else:
                raise Exception

        except Exception as e:
            logger.info(dict(op='file-send', status='error',
                        message=dict(session=currentsessionid, task=taskid)))
            print('File do not sent. Error.')
            print(e)
            return

    def abort(self):
        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline() == ['python', 'core.py']:
                pid = proc.pid
        if not pid:
            print(f'Baseline CORE was not started, the command cannot be executed')
            return

        try:
            perfomance = get_perfomance()
            response = mureq.post(perfomance["download_host"] + '/abort', json={'token': perfomance["token"]})
            if response.status_code == 201:
                logger.info(dict(op='session-abort', status='success',
                            message='Termination of session completed successfully'))
                print('Session abort success.')
                return
            else:
                raise Exception
        except Exception as e:
            logger.info(dict(op='session-abort', status='error',
                        message='Session - was not aborted.'))
            print('Session - was not aborted.')
            print(e)
            return

    def check(self):
        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline() == ['python', 'core.py']:
                pid = proc.pid
        if pid:
            print("Baseline process is now started. PID - " + str(pid))
            print("Current INPUT queue state - " + str(self.main_input_queue.qsize()))
            print("Current OUTPUT queue state - " + str(self.main_output_queue.qsize()))
        else:
            print("Baseline process not launched. \nIf you want to raise the connection to the AIMED platform"
                  " - enter the command `python baseline.py core`")

    def flush(self):
        input_queue_size = self.main_input_queue.qsize()
        if input_queue_size > 0:
            print("Current INPUT queue state - " + str(self.main_input_queue.qsize()) + ". Delete pending tasks")
            for i in range(0, input_queue_size, 1):
                self.main_input_queue.get_nowait()
        else:
            print("INPUT queue is empty. Skip.")

        output_queue_size = self.main_output_queue.qsize()
        if output_queue_size > 0:
            print("Current OUTPUT queue state - " + str(self.main_output_queue.qsize()) + ". Delete pending tasks")
            for i in range(0, output_queue_size, 1):
                self.main_output_queue.get_nowait()
        else:
            print("OUTPUT queue is empty. Skip.")

    ## python baseline.py test --test_id=1 --description="Lorem ipsum dolor sit amet"
    ## ограничение на кол-во символов в обосновании диагноза (500)
    ## давать список исследований нельзя - это подсказка (но а как узнать, что вообще представлено и как обрабатывать случаи матчинга имён?) (!)
    ## нужна проверка на сумму 100% для всех гипотез
    ## не пускаем на платформу невалидный запрос исследований или проверяем - проверяем по справочнику

    ## - список нозологий закладываем в бейзлайн (!)
    def test(self, test_id: int, description: str):
        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline() == ['python', 'core.py']:
                pid = proc.pid
        if not pid:
            print(f'Baseline CORE was not started, the command cannot be executed')
            return

        if len(description) > 500:
            print("The 'description' field is limited to 500 characters")
            return

        if test_id not in [1, 2, 3, 4, 5, 6]:
            print("Test with this ID (test_id param) does not exist")

            return

        currentsessionid = get_current_session_id()
        currentepicrisisid = get_current_epicrisis_id()
        currenttaskid = get_current_task_id()

        self.main_input_queue.put(
            dict(
                op="gettest",
                data={
                    "description": description,
                    "sessionId": currentsessionid,
                    "epicrisisId": currentepicrisisid,
                    "testId": test_id,
                    "taskId": currenttaskid
                }
            )
        )

        answer = self.main_output_queue.get()

        print(answer)
        pass


if __name__ == '__main__':
    fire.Fire(BaselineCommands)
