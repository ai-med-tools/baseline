import fire, os, json, time, psutil
from ipcqueue import posixmq
from baseline_constants import session_start_success_const, solution_file_doesnt_exist_const
from baseline_constants import data_not_resolved_const
from cfg_support import get_current_session_id
from cfg_support import get_current_epicrisis_id
from cfg_support import get_current_task_id
from validator import Validator, NotJsonContentInFileError, TooManyObjectsInTheArrayError
from validator import JsonIsEmpty, StructureJsonIsIncorrect
from cfg_support import get_perfomance
import socketio
from datetime import datetime


class BaselineCommands(object):
    def __init__(self):
        self.main_input_queue = posixmq.Queue('/baseline')
        self.main_output_queue = posixmq.Queue('/inline')

    def core(self):
        f = open("attempt.txt", "w+")
        current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        f.write('Recorded at: %s\n' % current_datetime)
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
            sio.connect(f'{perfomance["aimed_host"]}?token={perfomance["token"]}&ping={ping}', namespaces=['/baseline'],
                        transports=['websocket'])
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

    def start(self, contest, stage, type, count=None, timeout=None):
        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline() == ['python', 'core.py']:
                pid = proc.pid
        if not pid:
            print(f'Baseline CORE was not started, the command cannot be executed')
            return

        print(contest, stage, type, count, timeout)
        if type not in ["training", "estimated-training"]:
            print(type)
            if count or timeout:
                print(f'Parameter setting is allowed only in the training session.')
                return

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

        self.main_input_queue.put(
            initial_params,
            priority=1
        )

        answer = self.main_output_queue.get()

        print(answer)
        pass

    def send(self, path):
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

        currentsessionid = get_current_session_id()
        currentepicrisisid = get_current_epicrisis_id()
        currenttasksid = get_current_task_id()

        if not currentsessionid or not currentepicrisisid or not currenttasksid:
            print(data_not_resolved_const)

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

        self.main_input_queue.put(
            dict(
                op="send",
                data={
                    "taskId": int(currenttasksid),
                    "epicrisisId": int(currentepicrisisid),
                    "sessionId": int(currentsessionid),
                    "path": path,
                }
            ), priority=1
        )

    def abort(self):
        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline() == ['python', 'core.py']:
                pid = proc.pid
        if not pid:
            print(f'Baseline CORE was not started, the command cannot be executed')
            return

        self.main_input_queue.put(
            dict(
                op="abort",
                data={}
            ), priority=1
        )
        print("abort send")
        answer = self.main_output_queue.get(True, 5)

        print(answer)
        pass

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
