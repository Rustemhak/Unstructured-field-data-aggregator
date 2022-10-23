import xml.etree.ElementTree as ET
from yargy import Parser


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
    fact_local = None
    for sentence in chapter:
        matches = list(parser.findall(sentence.text))
        if matches:
            for match in matches:
                fact_local = match.fact
                sentence.set(tag_attr, eval(tag_attr + '__str__')(fact_local))

        if extra_parser and fact_local:
            extra_matches = list(extra_parser.findall(sentence.text))
            if extra_matches:
                for match in extra_matches:
                    sentence.set(tag_attr, eval(tag_attr + '__str__')(fact_local))
    # return res+text[end_prev:]


def set_tag_attr_for_field(tag_attr: str, chapter: ET.SubElement, parser: Parser):
    '''
    Устанавливает атрибут-характеристику, если есть атрибут месторождение в текущем предложении
    :param tag_attr: соответсвующий атрибут XML-tag'a
    :param chapter: часть XML-документа, который содержит текст нужной главы
    :param parser: парсер на поданном правиле, откуда будем брать атрибуты сущности
    '''
    for sentence in chapter:
        if 'field' in sentence.attrib:
            matches = list(parser.findall(sentence.text))
            if matches:
                for match in matches:
                    fact = match.fact
                    sentence.set(tag_attr, eval(tag_attr + '__str__')(fact))
