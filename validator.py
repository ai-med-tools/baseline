import json


class Validator:
    solution_from_file: dict

    def __init__(self, path):
        self._path = path

    def validate(self):
        self.validate_json_is_it()
        self.validate_json_is_empty()
        self.validate_count_objects()
        self.validate_prep_keys()
        self.validate_json_structure()
        self.validate_limit_keys()
        self.validate_diagnosis_length()
        self.validate_diagnosis_exists()
        self.validate_incorrect_key_values()
        pass

    def validate_json_is_it(self):
        try:
            with open(self._path) as f:
                solution_raw_content = f.read()

            self.solution_from_file = json.loads(solution_raw_content)
        except:
            raise NotJsonContentInFileError()

    def validate_json_is_empty(self):
        if len(self.solution_from_file) < 1:
            raise JsonIsEmpty()
        pass

    def validate_count_objects(self):
        if len(self.solution_from_file) > 100:
            raise TooManyObjectsInTheArrayError()
        pass

    def validate_json_structure(self):
        av_keys = ['decorCode', 'code']
        for val in self.solution_from_file:
            list = val.keys()
            for key in list:
                if key not in av_keys:
                    raise StructureJsonIsIncorrect()
            # status = "start" in val and "end" in val and "decorCode" in val and "code" in val and "name" in val \
            #          and "xPath" in val
            # if not status:
            #     raise StructureJsonIsIncorrect()

        pass

    def validate_limit_keys(self):
        count_desease = 0
        count_sup = 0
        count_main = 0
        count_prep = 0
        for val in self.solution_from_file:
            if "decorCode" in val:
                if val['decorCode'] == 'attendDisease':
                    count_desease += 1
                if val['decorCode'] == 'diagnosisSup':
                    count_sup += 1
                if val['decorCode'] == 'diagnosisMain':
                    count_main += 1
                if val['decorCode'] == 'diagnosisPreliminary':
                    count_prep += 1

        if count_sup > 10 or count_desease > 10 or count_main > 1 or count_prep > 1:
            raise LimitKeysInJson()
        pass

    def validate_incorrect_key_values(self):
        av_keys = ['attendDisease', 'diagnosisSup', 'diagnosisMain']
        for val in self.solution_from_file:
            if "decorCode" in val:
                if val['decorCode'] not in av_keys:
                    raise IncorrectKeyValues()
        pass

    def validate_prep_keys(self):
        count_prep = 0
        another_list = []
        for val in self.solution_from_file:
            if "decorCode" in val:
                if val['decorCode'] == 'diagnosisPreliminary':
                    count_prep += 1
                else:
                    another_list.append(val['decorCode'])

        if count_prep == 1:
            if not another_list:
                raise NotOnlyPrepDiagnosis()
        pass

    def validate_diagnosis_exists(self):
        count_main = 0
        for val in self.solution_from_file:
            if "decorCode" in val:
                if val['decorCode'] == 'diagnosisMain':
                    count_main += 1

        if count_main == 0:
            raise ThereIsNoMainDiagnosis()
        pass

    def validate_diagnosis_length(self):
        diagnosis_length = 10
        for val in self.solution_from_file:
            if "decorCode" in val:
                if val['decorCode'] == 'diagnosisMain':
                    if len(val['code']) > diagnosis_length:
                        raise DiagnosisMainLength()
        pass


class JsonIsEmpty(Exception):
    def __str__(self):
        return f'Answer JSON is empty.'


class StructureJsonIsIncorrect(Exception):
    def __str__(self):
        return f'The structure of the JSON sent in the response does not match the TR.'


class LimitKeysInJson(Exception):
    def __str__(self):
        return f'The number of decorCode key in the attendDisease or diagnosisSup or diagnosisMain or diagnosisPreliminary values has been exceeded'

class IncorrectKeyValues(Exception):
    def __str__(self):
        return f'The decorCode field uses invalid key values'

class DiagnosisMainLength(Exception):
    def __str__(self):
        return f'The length of the main diagnosis line exceeded 10 characters'

class NotJsonContentInFileError(Exception):
    def __str__(self):
        return f'The file at the specified path does not contain json.'

class ThereIsNoMainDiagnosis(Exception):
    def __str__(self):
        return f'The main diagnosis does not exist in the sent markup.'

class NotOnlyPrepDiagnosis(Exception):
    def __str__(self):
        return f'You sent something other keys than a preliminary diagnosis.'


class TooManyObjectsInTheArrayError(Exception):
    def __str__(self):
        return f'The maximum length of an array of objects with a response is 100 elements.'
