import re
from xml.etree import ElementTree
import json


class XPath:
    ANAMNESIS_XPATH = """def:component/def:structuredBody/def:component[{component_num}]/def:section/def:text"""


class Document:
    """
    Class for convenient work with medical document and response to it
    """
    root_namespace = {}

    def __init__(self, path_to_doc: str, path_to_res: str, com_num=2):
        """
        Init method. Just it
        :param path_to_doc: path to source xml file
        :param path_to_res: path to result from json file
        """

        self.doc = path_to_doc
        self.res = path_to_res
        self.doc_xml = ElementTree.parse(self.doc)
        root_tag = self.doc_xml.getroot().tag
        root_namespace = root_tag[root_tag.find('{') + 1:root_tag.rfind('}')]
        assert root_namespace is not None
        self.root_namespace['def'] = root_namespace
        self.anamnesis = self.doc_xml.getroot().find(XPath.ANAMNESIS_XPATH.format(component_num=com_num),
                                                     namespaces=self.root_namespace).text.strip()
        assert self.anamnesis is not None

    def get_anamnesis(self) -> str:
        """
        method for returning anamnesis section
        :return:
        """
        return self.anamnesis

    def get_position_in_anamnesis(self, words: str = None) -> tuple:
        """
        Method for returning position of words on anamnesis
        :param words:
        :return:
        """

        result = re.search(words, self.anamnesis)
        start_pos, end_pos = result.start(), result.end()
        return start_pos, end_pos
