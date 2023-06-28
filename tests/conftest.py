import pytest
from baseline.essay.meta import MetaFactory, MetaAbstract, Meta
from pathlib import Path

@pytest.fixture(name='meta_dict_correct')
def meta_dict_correct():
    return {
        "class": "11",
        "expert": "",
        "id": "00000781",
        "name": "0000078_ru_his_period_1825__1855_noexp.txt",
        "subject": "hist",
        "taskText": "",
        "test": "егэ тренировка",
        "theme": "Период 1825 – 1855",
        "uuid": "a81dad61-76f2-4e23-85e9-7af643089081",
        "year": 2020
    }


@pytest.fixture(name='meta_dict_incorrect')
def meta_dict_incorrect():
    return {
        "class": 123,
        "expert": 321,
        "id": "0000078",
        "name": "asd",
        "subject": "qwe",
        "taskText": "",
        "test": "егэ тренировка",
        "theme": 321,
        "uuid": 321,
        "year": 2020
    }


@pytest.fixture()
def file_path_correct():
    # Выход из папки, т.к ко
    return Path('../files/tests/test_file_read.json')

@pytest.fixture()
def file_path_incorrect():
    # Выход из папки, т.к ко
    return Path('../files/tests/incorrect.json')
