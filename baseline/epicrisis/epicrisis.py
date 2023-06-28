from abc import ABC
from baseline.epicrisis.copy_abstract import CopyAbstract
from baseline.session.dto import input as dto_input
from baseline.epicrisis.file import FileAbstract, FileFactory
from baseline.epicrisis.exceptions import NotHasRequiredFieldError, FileIsExistError, ValidationError
from baseline.tools.env_config import DOWNLOAD_HOST, TOKEN
import requests


class Epicrisis(CopyAbstract, ABC):
    session_id: int
    epicrisis_id: int
    version_id: int
    team_id: int
    task_id: int
    session_type_code: str
    aws_link: str
    path_to_xml: str

    _file: FileAbstract = None

    def __init__(self, data: dto_input.SessionFileDto):
        self.session_id = data.session_id
        self.epicrisis_id = data.epicrisis_id
        self.version_id = data.version_id
        self.team_id = data.team_id
        self.task_id = data.task_id
        self.session_type_code = data.session_type_code
        self.aws_link = data.aws_link
        self.path_to_xml = f'sessions/{self.session_id}/input/{self.epicrisis_id}_{self.version_id}_{self.task_id}.xml'

    def copy(self) -> 'Epicrisis':
        return self.__class__._copy(self)

    def __copy__(self) -> 'Epicrisis':
        return self.__class__._copy(self)

    def __deepcopy__(self, memo={}) -> 'Epicrisis':
        return self.__class__._copy(self)

    @classmethod
    def _copy(cls, original: 'Epicrisis') -> 'Epicrisis':
        pass

    @property
    def file(self) -> FileAbstract:
        return self._file

    @file.setter
    def file(self, file: FileAbstract):
        if self._file is not None:
            raise FileIsExistError()
        self._file = file

    def save(self, path: str = None) -> None:
        if self._file is None:
            if path is None:
                raise Exception('File is not exist and path not entered')
        else:
            payload = {'baselineToken': TOKEN, 'epicrisisId': self.epicrisis_id}
            response = requests.get(DOWNLOAD_HOST, params=payload)
            self._file.write(response.content)


class EpicrisisFactory:
    @staticmethod
    def get_instance(data: dto_input.SessionFileDto) -> Epicrisis:
        return Epicrisis(data)
