from abc import ABC, abstractmethod
from pathlib import Path

from baseline.epicrisis import constants


class FileAbstract(ABC):
    _path: Path

    _absolute_path: Path

    def __init__(self, path: Path):
        self._path = path
        self._absolute_path = constants.FILES_ROOT_DIR.joinpath(self._path)

    @abstractmethod
    def read(self) -> str:
        pass

    @abstractmethod
    def write(self, content) -> None:
        pass


class File(FileAbstract):
    def read(self) -> str:
        with open(self._absolute_path) as file:
            return file.read()

    def write(self, content) -> None:
        self.__check_dir()
        with open(self._absolute_path, 'wb') as file:
            file.write(content)

    def write_dict(self, content) -> None:
        self.__check_dir()
        with open(self._absolute_path, 'w') as file:
            file.write(content)

    def __check_dir(self) -> None:
        if not self._absolute_path.parent.exists():
            self._absolute_path.parent.mkdir(mode=0o775, parents=True)


class FileFactory:
    @staticmethod
    def create(path: Path):
        return File(path)
