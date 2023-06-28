import pytest
import json

from baseline.essay.essay import EssayFactory, EssayAbstract, Essay
from baseline.essay.meta import MetaFactory, MetaAbstract
from baseline.essay.selection import SelectionFactory, SelectionCollection

@pytest.fixture
def meta_dict():
    return {
        "class": "11",
        "expert": "",
        "id": "0000078",
        "name": "0000078_ru_his_period_1825__1855_noexp.txt",
        "subject": "hist",
        "taskText": "",
        "test": "егэ тренировка",
        "theme": "Период 1825 – 1855",
        "uuid": "a81dad61-76f2-4e23-85e9-7af643089081",
        "year": 2020
    }

@pytest.fixture
def meta_init(meta_dict):
    meta = MetaFactory.get_instance()
    meta.fill(meta_dict)
    return meta

@pytest.fixture
def selection_instance():
    selection = SelectionFactory.get_instance()
    selection.fill({
        "comment": "",
        "correction": "",
        "endSelection": 20,
        "explanation": "",
        "group": "error",
        "id": 111,
        "startSelection": 10,
        "subtype": "",
        "tag": "",
        "type": "И.личность"
    })
    return selection

@pytest.fixture
def essay_dict_init():
    return {
        "meta": {
            "class": "11",
            "expert": "",
            "id": "0000078",
            "name": "0000078_ru_his_period_1825__1855_noexp.txt",
            "subject": "hist",
            "taskText": "",
            "test": "егэ тренировка",
            "theme": "Период 1825 – 1855",
            "uuid": "a81dad61-76f2-4e23-85e9-7af643089081",
            "year": 2020
        },
        "text": "Период 1825 – 1855 является временем правления Николая 1. В данный исторический отрезок времени происходят такие события, как подавление восстания"
    }

@pytest.fixture
def essay_json_string():
    return '{"meta":{"class":"11","expert":"","id":"0000078","name":"0000078_ru_his_period_1825__1855_noexp.txt","subject":"hist","taskText":"","test":"егэ тренировка","theme":"Период 1825 – 1855","uuid":"a81dad61-76f2-4e23-85e9-7af643089081","year":2020},"selections":[],"text":"Период 1825 – 1855 является временем правления Николая 1. В данный исторический отрезок времени происходят такие события, как подавление восстания"}'

@pytest.fixture
def essay_instance(meta_init):
    return EssayFactory.get_instance('test text', meta_init)

class TestEssay:
    # correct case
    def test_json_parse_correct(self, essay_json_string):
        essay_dict = EssayAbstract.parse_json(essay_json_string)

        assert isinstance(essay_dict, dict)
        assert 'text' in essay_dict
        assert 'meta' in essay_dict
        assert 'id' in essay_dict.get('meta')

    def test_factory_correct_instance(self, meta_init):
        essay = EssayFactory.get_instance('test text', meta_init)
        assert isinstance(essay, EssayAbstract)
        assert isinstance(essay.meta, MetaAbstract)
        assert essay.meta.id == '0000078'
        assert len(essay.meta.subject) > 2

    def test_factory_correct_instance_from_json(self, essay_json_string):
        essay = EssayFactory.get_instance_from_json(essay_json_string)
        assert isinstance(essay, EssayAbstract)
        assert isinstance(essay.meta, MetaAbstract)
        assert essay.meta.id == '0000078'
        assert len(essay.meta.subject) > 2

    def test_factory_correct_instance_from_dict(self, essay_dict_init):
        essay = EssayFactory.get_instance_from_dict(essay_dict_init)
        assert isinstance(essay, EssayAbstract)
        assert isinstance(essay.meta, MetaAbstract)
        assert essay.meta.id == '0000078'
        assert len(essay.meta.subject) > 2

    def test_load_correct_abstract(self, essay_dict_init):
        essay = Essay.load(essay_dict_init)
        assert isinstance(essay, EssayAbstract)
        assert isinstance(essay.meta, MetaAbstract)
        assert essay.meta.id == '0000078'
        assert len(essay.meta.subject) > 2

    def test_load_correct_concrete(self, essay_dict_init):
        essay = Essay.load(essay_dict_init)
        assert isinstance(essay, Essay)
        assert isinstance(essay.meta, MetaAbstract)
        assert essay.meta.id == '0000078'
        assert len(essay.meta.subject) > 2

    def test_essay_to_dict_is_correct(self, essay_instance: EssayAbstract):
        essay_dict = essay_instance.to_dict()

        assert 'text' in essay_dict
        assert 'meta' in essay_dict
        assert 'id' in essay_dict.get('meta')
        assert 'subject' in essay_dict.get('meta')

    def test_essay_to_json_is_correct(self, essay_instance: EssayAbstract):
        essay_json = essay_instance.to_json()
        assert len(essay_json) > 0
        assert '"text":' in essay_json, 'text field didn`t exist in essay as json'
        assert '"meta":' in essay_json, 'meta field didn`t exist in essay as json'

    def test_essay_selections_correct(self, essay_instance: EssayAbstract):
        assert isinstance(essay_instance.selections, SelectionCollection)
        assert len(essay_instance.selections) == 0
        assert 'selections' not in essay_instance.to_dict()

    # fall case
    def test_json_parse_fall(self, essay_json_string):
        with pytest.raises(json.decoder.JSONDecodeError):
            EssayAbstract.parse_json(essay_json_string + 'fail')

    def test_essay_incorrect_init(self, meta_init):
        with pytest.raises(ValueError, match=r'.* "meta" .*'):
            EssayFactory.get_instance('test text', {})

        with pytest.raises(ValueError, match=r'.* "text" .*'):
            EssayFactory.get_instance('', meta_init)


"""
Test cases Essay

Positive
- Factory return correct class. The EssayFactory.get_instance method will return a correct class instance.
- The "load" method correct. Take correct dict and return correct essay.
- EssayAbstract.parse_json return correct dict essay
- Copy is work. After using the .copy method we will get a copy of the essay
- Validate without errors.

Negative
- The "load" method fall with incorrect data in dict argument
- If give a incorrect argument type (meta, selection) init object is fall
-  
"""