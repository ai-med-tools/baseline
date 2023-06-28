from abc import ABC
import asyncio
import random
import json
import os.path
import time

from typing import Union
from pathlib import Path
from loguru import logger

from baseline.tools.env_config import DEBUG_MAX_MARKUP_DEMO_DELAY, CHECK_DIRECTORY_ANSWER, CHECK_DIRECTORY_ANSWER_DELAY, AUTOMATIC_ANSWER_FILE_GENERATE

from baseline.solution.implementation.solution_abstract import SolutionAbstract
from baseline.epicrisis.epicrisis import Epicrisis
from baseline.epicrisis.file import FileAbstract, FileFactory

class SolutionDemo(SolutionAbstract):
    ## Размечаемый эпикриз
    epicrisis: Epicrisis

    xPath: str
    start: int
    end: int
    decorCode: str
    pathToAnswer: str

    _logger = logger

    __DEMO_SOLUTION = {
        'start': 0,
        'end': 1,
        'decorCode': 'diagnosisMain',
        'code': 'X101',
        'name': 'Рак лёгких',
        'xPath': ''
    }

    def __init__(self, epicrisis: Epicrisis):
        self.epicrisis = epicrisis
        self.__DEMO_SOLUTION = [{
            'start': 0,
            'end': 1,
            'decorCode': 'diagnosisMain',
            'code': 'X101',
            'name': 'Рак лёгких',
            'xPath': ''
        }]

    async def execute_async(self, timeoutFile: int) -> list[dict[str, Union[int, str]]]:
        await asyncio.sleep(random.randrange(0, DEBUG_MAX_MARKUP_DEMO_DELAY + 1))

        self._logger.info(f'sessions/{self.epicrisis.session_id}/output/'
                          f'{self.epicrisis.epicrisis_id}_{self.epicrisis.version_id}'
                          f'_{self.epicrisis.task_id}.json')

        if CHECK_DIRECTORY_ANSWER:
            self._logger.info(f'Env- CHECK_DIRECTORY_ANSWER = {CHECK_DIRECTORY_ANSWER} '
                              f'- solution file will be searched in the directory.')

            directory_conventional_name = f'sessions/{self.epicrisis.session_id}/output/' \
                                          f'{self.epicrisis.epicrisis_id}_{self.epicrisis.version_id}' \
                                          f'_{self.epicrisis.task_id}.json'
            self._logger.info(f'Custom file send delay set to {CHECK_DIRECTORY_ANSWER_DELAY}. '
                              f'Platform limit = {timeoutFile}')

            if AUTOMATIC_ANSWER_FILE_GENERATE:
                self._logger.info(f'ENV - AUTOMATIC_ANSWER_FILE_GENERATE - {AUTOMATIC_ANSWER_FILE_GENERATE}.'
                                  f' Solution file will be generated automatically')

                dictionary = [{
                    'start': 0,
                    'end': 1,
                    'decorCode': 'diagnosisMain',
                    'code': 'X101',
                    'name': 'Рак лёгких',
                    'xPath': ''
                }]

                # Serializing json
                json_object = json.dumps(dictionary, indent=4)

                file = FileFactory.create(Path(f'{directory_conventional_name}'))
                file.write_dict(json_object)

                self._logger.info(f'Solution file was created in automatic mode.')
                self._logger.info(os.path.exists(f'files/{directory_conventional_name}'))

            delay = (CHECK_DIRECTORY_ANSWER_DELAY if (CHECK_DIRECTORY_ANSWER_DELAY <= timeoutFile and CHECK_DIRECTORY_ANSWER_DELAY != 0) else timeoutFile)
            counter = 0
            self._logger.info(delay)

            if CHECK_DIRECTORY_ANSWER_DELAY:
                self._logger.info(f'Sleep {CHECK_DIRECTORY_ANSWER_DELAY}.')
                time.sleep(CHECK_DIRECTORY_ANSWER_DELAY)
                counter = CHECK_DIRECTORY_ANSWER_DELAY

            if AUTOMATIC_ANSWER_FILE_GENERATE:
                while not (counter == delay):
                    self._logger.info(f'while loop')
                    self._logger.info(f'counter - {counter}')
                    time.sleep(1)
                    counter += 1
                    if os.path.isfile(f'files/{directory_conventional_name}'):
                        self._logger.info(
                            f'Solution file found. {self.epicrisis.epicrisis_id}_'
                            f'{self.epicrisis.version_id}'
                            f'_{self.epicrisis.task_id}.json')

                        with open(f'files/{directory_conventional_name}') as f:
                            data = f.read()
                        solution_from_file = json.loads(data)
                        ## Валидация найденного объекта
                        return solution_from_file
                    else:
                        continue
                self._logger.info(f'timer is out, exit')
                return None
            else:
                while not (os.path.exists(f'files/{directory_conventional_name}') or (counter == delay)):
                    self._logger.info(f'while loop')
                    self._logger.info(f'counter - {counter}')
                    time.sleep(1)
                    counter += 1
                    if os.path.isfile(f'files/{directory_conventional_name}'):
                        self._logger.info(
                            f'Solution file found. {self.epicrisis.epicrisis_id}_'
                            f'{self.epicrisis.version_id}'
                            f'_{self.epicrisis.task_id}.json')

                        with open(f'files/{directory_conventional_name}') as f:
                            data = f.read()
                        solution_from_file = json.loads(data)
                        ## Валидация найденного объекта
                        return solution_from_file
                    else:
                        continue
                self._logger.info(f'timer is out, exit')
                return None
        else:
            self._logger.info(f'Env- CHECK_DIRECTORY_ANSWER = {CHECK_DIRECTORY_ANSWER} '
                              f'- the solution will be taken from the get_solution method.')
            return self.get_solution()


    def get_solution(self):
        ## make magic with epicrisis
        return self.__DEMO_SOLUTION

    def execute(self, timeoutFile: int) -> list[dict[str, Union[int, str]]]:
        return self.__execute()

    def __execute(self) -> list[dict[str, Union[int, str]]]:
        ## make magic with epicrisis

        self.__DEMO_SOLUTION = [{
            'start': 0,
            'end': 1,
            'decorCode': 'diagnosisMain',
            'code': 'X101',
            'name': 'Рак лёгких',
            'xPath': ''
        }]

        # self.xPath = self.__DEMO_SOLUTION.get('xPath')
        # self.start = self.__DEMO_SOLUTION.get('start')
        # self.end = self.__DEMO_SOLUTION.get('end')
        # self.decorCode = self.__DEMO_SOLUTION.get('decorCode')
        # self.code = self.__DEMO_SOLUTION.get('code')
        # self.name = self.__DEMO_SOLUTION.get('name')
        return self.__DEMO_SOLUTION

    def to_json(self) -> str:
        file_content: dict = {
            'xPath': self.xPath,
            'start': self.start,
            'end': self.end,
            'decorCode': self.decorCode,
            'code': self.code,
            'name': self.name,
        }
        return json.dumps(file_content, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4, ensure_ascii=False)
