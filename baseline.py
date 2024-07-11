import fire, os, json, psutil
import mureq
from ipcqueue import posixmq
from baseline_constants import session_start_success_const, solution_file_doesnt_exist_const
from baseline_constants import data_not_resolved_const
from cfg_support import get_current_session_id
from cfg_support import get_current_epicrisis_id
from cfg_support import get_current_task_id
from validator import Validator, NotJsonContentInFileError, TooManyObjectsInTheArrayError
from validator import JsonIsEmpty, StructureJsonIsIncorrect, LimitKeysInJson, DiagnosisMainLength
from validator import IncorrectKeyValues
from validator import ThereIsNoMainDiagnosis, NotOnlyPrepDiagnosis, DiagnosisPrepLength
from cfg_support import get_perfomance
import socketio
import datetime as dt
from push_log import logger
from cfg_support import get_current_test_path


class BaselineCommands(object):
    def __init__(self):
        self.main_input_queue = posixmq.Queue('/baseline')
        self.main_output_queue = posixmq.Queue('/inline')

    def core(self):
        perfomance = get_perfomance()

        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline()[-2:] == ['python', 'core.py']:
                pid = proc.pid
        if pid:
            print("Baseline process is already started. PID - " + str(pid))
            return

        try:
            # standard Python
            ping = 'ping'
            sio = socketio.Client()
            sio.connect(f'{perfomance["aimed_host"]}?token={perfomance["token"]}&ping={ping}',
                        namespaces=['/baselinezcllbpxcgrye'],
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
        '''ЗАВЕРШЕНИЕ ГЛАВНОГО ПРОЦЕССА. ЭКВИВАЛЕНТНО "docker compose down". Пример для Docker - LINUX - "./baseline kill" -
        WINDOWS - docker-compose exec -iT baseline sh -c "python baseline.py kill".
        Подробнее об этом в файлах docs/commands-native.md и docs/commands-windows.md'''
        try:
            pid = None
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                if proc.cmdline()[-2:] == ['python', 'core.py']:
                    proc.kill()
            print("Core successfully killed.")
        except:
            print("An exception occurred.")

    def start(self, contest, stage, type, count=None, timeout=None, nosology=None):
        '''СТАРТ СЕССИИ. Пример для Docker - LINUX - "./baseline start --contest=<contest> --stage=<stage> --type=<type> --count=<int> --timeout=<int>" -
        WINDOWS - docker-compose exec -iT baseline sh -c "python baseline.py start --contest=<contest> --stage=<stage> --type=<type> --count=<int> --timeout=<int>".
        Подробнее об этом в файлах docs/commands-native.md и docs/commands-windows.md'''
        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline()[-2:] == ['python', 'core.py']:
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

        # if contest in ["doctor"]:
        #     if type in ["training"]:
        #         if not count:
        #             count = 100

        if type in [ "estimated-training"]:
            if count:
                print(f'Parameter count cannot be specified in this session type.')
                return

        if type in [ "challenge"]:
            if nosology:
                print(f'Parameter setting is allowed only in the training session.')
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

        print(f'Parameter - contest - {contest}')
        print(f'Parameter - stage - {stage}')
        print(f'Parameter - type - {type}')

        if count:
            initial_params["data"]["params"]["countFiles"] = count
            print(f'Parameter - count - {count}')

        if timeout:
            initial_params["data"]["params"]["time"] = timeout
            print(f'Parameter - timeout - {timeout}')

        if nosology_string != "":
            initial_params["data"]["params"]["nosologyString"] = nosology_string
            print(f'Parameter - nosology string - {nosology_string}')

        self.main_input_queue.put(
            initial_params,
            priority=1
        )

        answer = self.main_output_queue.get()

        print(answer)
        pass

    def send(self, path, taskid):
        '''ОТПРАВКА РЕЗУЛЬТАТА НА ПЛАТФОРМУ. Пример для Docker - LINUX - "./baseline send --path=<path_to_solution_json> --taskid=<ID_задачи>" -
        WINDOWS - docker-compose exec -iT baseline sh -c "python baseline.py send --path=<path_to_solution_json> --taskid=<ID_задачи>".
        Подробнее об этом в файлах docs/commands-native.md и docs/commands-windows.md'''
        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline()[-2:] == ['python', 'core.py']:
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
        except DiagnosisMainLength as dml:
            print(dml)
            return
        except DiagnosisPrepLength as dpl:
            print(dpl)
            return
        except NotOnlyPrepDiagnosis as nopd:
            print(nopd)
            return
        except IncorrectKeyValues as ikv:
            print(ikv)
            return
        except ThereIsNoMainDiagnosis as tinmd:
            print(tinmd)
            return

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
        if response.status_code == 400:
            print(f'The submitted response is not validated')
            logger.info(dict(op='file-send', status='error',
                        message=dict(code=400, session=currentsessionid, task=taskid, time=less)))
        if response.status_code == 409:
            print(f'The preliminary diagnosis was sent again')
            logger.info(dict(op='file-send', status='error',
                        message=dict(code=409, session=currentsessionid, task=taskid, time=less)))
        if response.status_code == 404:
            print(f'Baseline token and task ID could not be matched. The task to which the response is sent does not exist in your current session.')
            logger.info(dict(op='file-send', status='error',
                        message=dict(code=404, session=currentsessionid, task=taskid, time=less)))
        if response.status_code == 422:
            print(f'It is impossible to send a final diagnosis without a preliminary one. Submit your preliminary diagnosis first.')
            logger.info(dict(op='file-send', status='error',
                        message=dict(code=422, session=currentsessionid, task=taskid, time=less)))
        if response.status_code == 201:
            logger.info(dict(op='file-send', status='success',
                        message=dict(session=currentsessionid, task=taskid, time=less)))
            print(f'File task ID - {taskid} - successfuly sent. Upload time -  {less}')
            return
    def abort(self):
        '''ПРЕРЫВАНИЕ СЕССИИ. Пример для Docker - LINUX - "./baseline abort" -
        WINDOWS - docker-compose exec -iT baseline sh -c "python baseline.py abort".
        Подробнее об этом в файлах docs/commands-native.md и docs/commands-windows.md'''
        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline()[-2:] == ['python', 'core.py']:
                pid = proc.pid
        if not pid:
            print(f'Baseline CORE was not started, the command cannot be executed')
            return

        try:
            perfomance = get_perfomance()
            response = mureq.post(perfomance["download_host"] + '/abort', json={'token': perfomance["token"]}, timeout=120)
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
        '''ПРЕРЫВАНИЕ СОСТОЯНИЯ УТИЛИТЫ. Пример для Docker - LINUX - "./baseline check" -
        WINDOWS - docker-compose exec -iT baseline sh -c "python baseline.py check".
        Подробнее об этом в файлах docs/commands-native.md и docs/commands-windows.md'''
        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline()[-2:] == ['python', 'core.py']:
                pid = proc.pid
        if pid:
            print("Baseline process is now started. PID - " + str(pid))
            print("Current INPUT queue state - " + str(self.main_input_queue.qsize()))
            print("Current OUTPUT queue state - " + str(self.main_output_queue.qsize()))
        else:
            print("Baseline process not launched. \nIf you want to raise the connection to the AIMED platform"
                  " - enter the command `python baseline.py core`")

    def flush(self):
        '''ОЧИСТКА ВНУТРЕННЕЙ ОЧЕРЕДИ КОМАНД. Пример для Docker - LINUX - "./baseline flush" -
        WINDOWS - docker-compose exec -iT baseline sh -c "python baseline.py flush".
        Подробнее об этом в файлах docs/commands-native.md и docs/commands-windows.md'''
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

    def test(self, taskid, code):
        '''ОТПРАВКА РЕЗУЛЬТАТА НА ПЛАТФОРМУ. Пример для Docker - LINUX - "./baseline test --taskid=<ID_задачи> --code=<code>" -
        WINDOWS - docker-compose exec -iT baseline sh -c "python baseline.py test --taskid=<ID_задачи> --code=<code>".
        Подробнее об этом в файлах docs/commands-native.md и docs/commands-windows.md'''
        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.cmdline()[-2:] == ['python', 'core.py']:
                pid = proc.pid
        if not pid:
            print(f'Baseline CORE was not started, the command cannot be executed')
            return

        perfomance = get_perfomance()
        response = mureq.post(perfomance["download_host"] + '/get-test',
                              json={'token': perfomance["token"], 'taskId': taskid, 'code': code})
        if response.status_code == 404:
            logger.info(dict(op='research-request', status='error(not-found)',
                             message=dict(task=taskid, code=code)))
            print('По вашему запросу не найдены исследования')
            return
        if response.status_code == 408:
            logger.info(dict(op='research-request', status='error(task-timeout)',
                             message=dict(task=taskid, code=code)))
            print('Задача просрочена')
            return
        if response.status_code == 400:
            logger.info(dict(op='research-request', status='error(not-prep-diagnosis)',
                             message=dict(task=taskid, code=code)))
            print('Необходимо прислать предварительный диагноз')
            return
        body = json.loads(response.body)
        if body:
            logger.info(dict(op='research-request', status='success(http-status)',
                             message=dict(task=taskid, code=code)))
            for it in body:
                if "link" in it:
                    test_path = get_current_test_path()
                    current_test_path = os.path.join(test_path,
                                                          f'{it["id"]}_{code}_{taskid}.xml')
                    response = mureq.get(it['link'])
                    with open(current_test_path, 'wb') as file:
                        file.write(response.content)
                    reqs = mureq.post(perfomance["download_host"] + '/test-is-rec',
                                          json={'token': perfomance["token"], 'taskId': taskid, 'code': code, 'id': it["id"]})
                    if reqs.status_code > 201:
                        logger.info(dict(op='research-request', status='error(set-received-time)',
                                         message=dict(task=taskid, code=code)))
                    logger.info(dict(op='research-request', status='success(saved)',
                                     message=dict(task=taskid, code=code)))
            print('Исследования сохранены.')


        pass


if __name__ == '__main__':
    fire.Fire(BaselineCommands)
