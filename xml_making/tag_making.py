import xml.etree.ElementTree as ET
from yargy import Parser

from models.characteristics import *

models_dict = {'field': FieldName,
               'location': Location,
               'open_date': OpenDate,
               'exploit_date': ExploitDate}


def set_tag_attr(tag_attr: str, chapter: ET.SubElement, parser: Parser, extra_parser: Parser = None) -> None:
    """
    Размечает предложения главы с соответствующими атрибутами и его значениями для тега <s>

    :param tag_attr: соответсвующий атрибут XML-tag'a
    :param parser: парсер на поданном правиле, откуда будем брать атрибуты сущности
    :param chapter: часть XML-документа, который содержит текст нужной главы
    :param extra_parser: parser для разрешения референций
    (если встречается объект без явного названия).
    "Месторождение" в текущем предложении, а в предыдущем "Архангельское месторождение"
    """
    model_class = models_dict[tag_attr]
    model = model_class(None)

    for sentence in chapter:
        matches = list(parser.findall(sentence.text))
        if matches:
            for match in matches:
                model.fact = match.fact
                sentence.set(tag_attr, str(model))

        if extra_parser and model.fact:
            extra_matches = list(extra_parser.findall(sentence.text))
            if extra_matches:
                for match in extra_matches:
                    sentence.set(tag_attr, str(model))
    # return res+text[end_prev:]


def set_tag_attr_for_field(tag_attr: str, chapter: ET.SubElement, parser: Parser):
    """
    Устанавливает атрибут-характеристику, если есть атрибут месторождение в текущем предложении

    :param tag_attr: соответсвующий атрибут XML-tag'a
    :param chapter: часть XML-документа, который содержит текст нужной главы
    :param parser: парсер на поданном правиле, откуда будем брать атрибуты сущности
    """

    model_class = models_dict[tag_attr]
    model = model_class(None)
    for sentence in chapter:
        if 'field' in sentence.attrib:
            matches = list(parser.findall(sentence.text))
            if matches:
                for match in matches:
                    model.fact = match.fact
                    sentence.set(tag_attr, str(model))


def set_xml_tag_sentences(sentences: list, chapter: ET.SubElement):
    """
    Проставляет тег предложение и конкретный ID в XML-документе для текущей главы

    :param  sentences: список предложений
    :param chapter: глава из XML-файла
    """
    for i, sent in enumerate(sentences):
        if isinstance(sent, list):
            # print('list', type(sent))
            for j, subsent in enumerate(sent[:-1]):
                if j == 0:
                    sentence = ET.SubElement(chapter, 's')
                    sentence.set('ID', str(i))
                    sentence.text = subsent + ':'
                else:
                    sentence = ET.SubElement(chapter, 's')
                    sentence.set('ID', str(i) + '.' + str(j))
                    sentence.text = subsent + ';'
        else:
            sentence = ET.SubElement(chapter, 's')
            sentence.set('ID', str(i))
            # print('no list', type(sent))
            sentence.text = sent