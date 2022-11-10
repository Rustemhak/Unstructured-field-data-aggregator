import xml.etree.ElementTree as ET
from yargy import Parser

from models.characteristics import *
from rules.kin_rule import get_KIN
from rules.kvit_rule import get_kvit
from rules.objects_rule import HORIZON, STAGE
from rules.oil_sat_rule import get_oil_sat
from rules.porosity_rule import get_porosity
from yargy_utils import TOKENIZER

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


horizon_parser = Parser(HORIZON, tokenizer=TOKENIZER)
stage_parser = Parser(STAGE, tokenizer=TOKENIZER)


def set_tag_attr_object_charact(chapter: ET.SubElement, tag_name: str) -> None:
    """
    Устанавливает атрибут-характеристику для объектов: нефтенасыщенность или пористость

    :param chapter: глава из XML-файла
    :param tag_name: имя тега характеристики: oil_sat or porosity
    """
    if tag_name == 'oil_sat':
        charact_fun = get_oil_sat
        CharactModel = OilSat
    elif tag_name == 'porosity':
        charact_fun = get_porosity
        CharactModel = Porosity
    else:
        raise AttributeError(f"Attribute tag_name expected 'oil_sat' or 'porosity', but got {tag_name}")

    object_name = ''

    for sentence in chapter:
        text = sentence.text

        matches = list(stage_parser.findall(text))
        if matches:
            match = matches[-1]
            fact = match.fact
            object_name = fact.name

        matches = list(horizon_parser.findall(text))
        if matches:
            match = matches[-1]
            fact = match.fact
            object_name = fact.name

        list_of_object_charact = charact_fun(text)
        if list_of_object_charact:
            charact_model = CharactModel(list_of_object_charact[0].fact)
            sentence.set(tag_name, str(charact_model))

            # if charact_model.fact.object_name:
            #     object_name = charact_model.fact.object_name

            sentence.set(f'object_{tag_name}', object_name)

            # На случай, если в одном предложении будет больше одного значения нефтенасыщенности или пористости
            # for idx, charact in enumerate(list_of_object_charact):
            #     charact_model = CharactModel(charact.fact)
            #     sentence.set(f'{tag_name}{idx}', str(charact_model))
            #
            #     if charact_model.fact.object_name:
            #         object_name = charact_model.fact.object_name
            #
            # sentence.set('object', object_name)


def set_tag_attr_kin_kvit(chapter: ET.SubElement, charact_name: str) -> None:
    """
    Устанавливает атрибут кин или квыт

    :param chapter: глава из XML-файла
    :param charact_name: имя характеристики: kin или kvit
    """
    if charact_name == 'kin':
        charact_fun = get_KIN
    elif charact_name == 'kvit':
        charact_fun = get_kvit
    else:
        raise AttributeError(f"Attribute tag_name expected 'kin' or 'kvit', but got {charact_name}")

    for sentence in chapter:
        text = sentence.text
        list_of_charact = charact_fun(text)
        if list_of_charact:
            for idx, match in enumerate(list_of_charact):
                if charact_name == 'kin':
                    sentence.set(f'object_name_kin_{idx}', match.fact.object_name_kin)
                    sentence.set(f'kin_value_{idx}', match.fact.kin_value)
                else:
                    sentence.set(f'object_name_kvit_{idx}', match.fact.object_name_kvit)
                    sentence.set(f'kvit_value_{idx}', match.fact.kvit_value)
