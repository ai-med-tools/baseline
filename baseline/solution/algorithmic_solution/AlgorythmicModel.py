from .DocumentModel import Document


class AlgorythmicModel:
    """
    Класс для решения алгоритмической секции конкурса
    """

    def __init__(self, document: Document):
        self.document = document

    def get_simple_solution(self):
        anamnesis_text = self.document.get_anamnesis()
        return [{
            'start': 0,
            'end': len(anamnesis_text),
            'decorCode': 'anamnesis',
            'code': '',
            'name': anamnesis_text,
            'xPath': "/ClinicalDocument/component/structuredBody/component[2]/section/text"
        }]
