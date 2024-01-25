import json


class Validator:
    solution_from_file: dict

    def __init__(self, path):
        self._path = path

    def validate(self):
        self.validate_json_is_it()
        self.validate_json_is_empty()
        self.validate_count_objects()
        self.validate_json_structure()
        self.validate_limit_keys()
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
        for val in self.solution_from_file:
            if "decorCode" in val:
                if val['decorCode'] == 'attendDisease':
                    count_desease += 1
                if val['decorCode'] == 'diagnosisSup':
                    count_sup += 1

        if count_sup >= 10 or count_desease >= 10:
            raise LimitKeysInJson()
        pass


class JsonIsEmpty(Exception):
    def __str__(self):
        return f'Answer JSON is empty.'


class StructureJsonIsIncorrect(Exception):
    def __str__(self):
        return f'The structure of the JSON sent in the response does not match the TR.'


class LimitKeysInJson(Exception):
    def __str__(self):
        return f'The number of decorCode key in the attendDisease and diagnosisSup values has been exceeded'


class NotJsonContentInFileError(Exception):
    def __str__(self):
        return f'The file at the specified path does not contain json.'


class TooManyObjectsInTheArrayError(Exception):
    def __str__(self):
        return f'The maximum length of an array of objects with a response is 100 elements.'
