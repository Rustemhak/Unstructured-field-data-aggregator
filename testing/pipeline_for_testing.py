import json
import os
import xml.etree.ElementTree as ET
from os import mkdir, path as pth
from os.path import isdir, join

import textract
from yargy import Parser
import pandas as pd
import streamlit as st

from converting.convert_pdf_txt import read_txt
from preprocessing_text import replace_short_name, STAND_GEO_SHORT_NAMES
from read_report import read_pdf
from rules.date_exploit_rule import EXPLOIT_DATE
from rules.date_open_rule import OPEN_DATE
from rules.field_rule import FIELD, NAME
from rules.kin_rule import get_KIN
from rules.location_rule import LOC
from rules.oil_deposit_rule import set_tag_attr_oil_deposit
from sentenizer.segment_sentences import segment_to_sent
from .testing_constant import CONTENT_G1, CONTENT_G2, CONTENT_B1, CONTENT_B2, REPORTS_FOR_THE_TEST, \
    PATHS_FOR_REPORTS_PDF, CONTENT_A1, CONTENT_A2
from xml_making.tag_making import set_xml_tag_sentences, set_tag_attr, set_tag_attr_for_field, \
    set_tag_attr_object_charact, set_tag_attr_kin_kvit
from yargy_utils import TOKENIZER, number_extractor


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def get_modifed(string: str, language: str):
    """Возвращает модифицированную строку. Приводит строку к английским буквам."""
    eq = {
        'o': 'о', 'e': 'е',
        'c': 'с', 'p': 'р',
        'O': 'О', 'E': 'Е',
        'C': 'С', 'P': 'Р'
    }
    if string:
        for en, ru in eq.items():
            if language == 'en':
                string = string.replace(ru, en)
            elif language == 'ru':
                string = string.replace(en, ru)
            else:
                raise AttributeError(f"attribute language expected 'ru' or 'en', but got {language}")

        return string
    return None


def convert_chapter_pdf_to_xml(path_pdf: str = None, idx_beg_chap: int = None, idx_end_chap: int = None,
                               chap_id: int = 1, path_xml: str = None, path_txt: str = None, path_docx=None):
    """
    Пайплайн для конвертации главы отчёта в формате pdf в XML
    Результат в 'output.xml'

    :param path_pdf: путь, где находится данный документ
    :param idx_beg_chap: страница начала раздела
    :param idx_end_chap: страница конца раздела
    :param chap_id: номер главы
    :param path_xml: путь для сохранения xml в папке reports/xml
    :param path_txt: путь к документу в формате txt, если документ был конвертирован из pdf в txt
    :param path_docx: путь к документу в формате docx.
    """

    if path_pdf:
        text = read_pdf(path_pdf, idx_beg_chap, idx_end_chap)
        if not text:
            print(f"Текст на страницах {idx_beg_chap} - {idx_end_chap} не найден.")
            return False

    elif path_txt:
        text = read_txt(path_txt)

    elif path_docx:
        text = textract.process(path_docx, language='rus+eng').decode('utf-8')

    else:
        raise AttributeError(f"Expected path_pdf or path_txt or path_docx but got nothing")

    text = replace_short_name(text, STAND_GEO_SHORT_NAMES)
    text = number_extractor.replace_groups(text)

    # создание тега "отчёт"
    report = ET.Element('report')
    # создание тега "главы"
    chapters = ET.SubElement(report, 'chapters')
    # создание тега "глава"
    chapter = ET.SubElement(chapters, 'chapter')
    chapter.set('ID', str(chap_id))
    # chapter.text = text

    sentences = segment_to_sent(text)

    set_xml_tag_sentences(sentences, chapter)

    parser = Parser(FIELD, tokenizer=TOKENIZER)
    extra_parser = Parser(NAME, tokenizer=TOKENIZER)
    set_tag_attr('field', chapter, parser, extra_parser)

    parser = Parser(LOC, tokenizer=TOKENIZER)
    set_tag_attr_for_field('location', chapter, parser)

    parser = Parser(OPEN_DATE, tokenizer=TOKENIZER)
    set_tag_attr_for_field('open_date', chapter, parser)

    parser = Parser(EXPLOIT_DATE, tokenizer=TOKENIZER)
    set_tag_attr_for_field('exploit_date', chapter, parser)

    set_tag_attr_oil_deposit(chapter)

    set_tag_attr_object_charact(chapter, 'oil_sat')
    set_tag_attr_object_charact(chapter, 'porosity')

    set_tag_attr_kin_kvit(chapter, 'kin')
    set_tag_attr_kin_kvit(chapter, 'kvit')

    tree = ET.ElementTree(report)
    indent(report)
    if report is not None:
        # writing xml
        # print(report.items())
        # ET.dump(report)

        if isdir(temp_path := join('..', 'reports', 'xml')):
            path_beg = temp_path
        elif isdir(temp_path := join('reports', 'xml')):
            path_beg = temp_path
        else:
            raise FileNotFoundError(
                r"No such file or directory: '..\reports\xml' or 'reports\xml'"
            )

        path_to_xml_dir = join(path_beg, path_xml)
        if not isdir(path_to_xml_dir):
            mkdir(path_to_xml_dir)
        tree.write(join(path_to_xml_dir, f'chapter{chap_id}.xml'), encoding="utf-8", xml_declaration=True)
        return True
    return False


def get_objects_with_kern(field_name):
    objects_with_kern = []
    path_to_json = pth.join('..', 'reports', 'objects_with_kern', field_name)
    if not isdir(path_to_json):
        print('Данные по керну отсутствуют')
        return None
    paths_to_json = [pth.join(path_to_json, report_name) for report_name in os.listdir(path_to_json)]
    for path in paths_to_json:
        with open(path, 'r', encoding='utf-8') as file:
            objects_with_kern += json.load(file)
    return objects_with_kern


def chapter_xml_to_pd(path: str) -> pd.DataFrame:
    """
    :param path: путь к файлу chapter.xml (xml файл для одной главы)
    """
    chapter_xml = ET.parse(path)
    root = chapter_xml.getroot()
    chapter_str_xml = ET.tostring(root[0][0], encoding="unicode")
    chapter_pd = pd.read_xml(chapter_str_xml)
    return chapter_pd


def concat_str_from_list(string: [str]) -> str:
    res = ""
    for i in string:
        res += i + " "
    return res[:-1]


def get_charact_info_from_str(string: str) -> tuple:
    charact_num_def_idx = string.find('num_def')
    charact_value_idx = string.find('value')
    charact_num_def = 0

    if charact_num_def_idx != -1:
        charact_num_def = int(string[charact_num_def_idx + 9:charact_value_idx - 2])
    charact_value = string[charact_value_idx + 7:]

    return charact_value, charact_num_def


@st.cache
def report_xml_to_xlsx(list_paths_chapters: [str], field_name: str, in_field=lambda x: True, on_csv=False):
    """
    Перевод отчета из xml в xlsx.

    :param list_paths_chapters: список путей к главам отчета в формате xml
    :param field_name: имя месторождения
    :param in_field: функция для проверки имен объектов на их наличие в месторождении
    :param on_csv
    """
    report_pd = pd.DataFrame()
    print('list_paths_chapters', list_paths_chapters)
    for chapter_path in list_paths_chapters:
        chapter_pd = chapter_xml_to_pd(chapter_path)
        report_pd = pd.concat((report_pd, chapter_pd))

    try:
        field = report_pd['field'].dropna().unique()[0]
    except KeyError:
        field = None
        print('Название месторождения не найдено')
    try:
        exploit_date = report_pd['exploit_date'].dropna().unique()[0]
    except KeyError:
        exploit_date = None
        print('Дата введения в эксплуатацию не найдена')
    try:
        open_date = report_pd['open_date'].dropna().unique()[0]
    except KeyError:
        open_date = None
        print('Дата открытия не найдена')
    try:
        location = report_pd['location'].dropna().unique()[0]
    except KeyError:
        location = None
        print("Местоположение не найдено")

    list_of_columns_object = []
    list_of_columns_kin_object = []
    list_of_columns_kin_value = []
    list_of_columns_kvit_object = []
    list_of_columns_kvit_value = []

    for column in list(report_pd.columns):
        if 'object_oil_deposit' in column:
            list_of_columns_object.append(column)
        if 'object_name_kin' in column:
            list_of_columns_kin_object.append(column)
        if 'kin_value' in column:
            list_of_columns_kin_value.append(column)
        if 'object_name_kvit' in column:
            list_of_columns_kvit_object.append(column)
        if 'kvit_value' in column:
            list_of_columns_kvit_value.append(column)

    objects_oil_deposit = []
    if list_of_columns_object:
        objects_oil_deposit = [list(report_pd[column].dropna().items()) for column in list_of_columns_object]

    objects_kin = []
    kin_values = []
    objects_kvit = []
    kvit_values = []
    for charact in [
        (list_of_columns_kin_object, list_of_columns_kin_value, objects_kin, kin_values),
        (list_of_columns_kvit_object, list_of_columns_kvit_value, objects_kvit, kvit_values)
    ]:

        if not (charact[0] and charact[1]):
            continue

        for column_object, column_value in zip(*charact[:2]):
            charact[2].append(*(report_pd[column_object].dropna()))
            charact[3].append(*(report_pd[column_value].dropna()))

    for charact_objects in [objects_kin, objects_kvit]:
        if not charact_objects:
            continue

        for idx, object_name in enumerate(charact_objects):
            upd_name = object_name.replace(' горизонт', '').replace(' ярус', '')
            if '+' in upd_name:
                idx_beg = upd_name.find('+')
                upd_name = upd_name[:idx_beg - 2] + 'о-' + upd_name[idx_beg + 1:]
            charact_objects[idx] = upd_name

    kin_values_for_object = {}
    kvit_values_for_object = {}

    for charact_dict, charact_objects, charact_values in [
        (kin_values_for_object, objects_kin, kin_values),
        (kvit_values_for_object, objects_kvit, kvit_values)
    ]:

        if not (charact_objects and charact_values):
            continue

        for object_name, charact_value in zip(charact_objects, charact_values):
            if object_name not in charact_dict:
                charact_dict[object_name] = charact_value

    objects_with_kern = get_objects_with_kern(field_name)
    if objects_with_kern:
        for idx, obj_name in enumerate(objects_with_kern):
            objects_with_kern[idx] = get_modifed(obj_name, 'ru')

    try:
        oil_sat = list(report_pd['oil_sat'].dropna())
        objects_oil_sat = list(report_pd['object_oil_sat'].dropna())
    except KeyError:
        oil_sat = []
        objects_oil_sat = []
    try:
        porosity = list(report_pd['porosity'].dropna())
        objects_porosity = list(report_pd['object_porosity'].dropna())
    except KeyError:
        porosity = []
        objects_porosity = []

    oil_sat_dict = {}
    porosity_dict = {}

    for_charact_dict = [(oil_sat_dict, objects_oil_sat, oil_sat),
                        (porosity_dict, objects_porosity, porosity)]

    for charact_dict, objects, characts in for_charact_dict:
        for object_name, charact in zip(objects, characts):
            charact_value, charact_num_def = get_charact_info_from_str(charact)

            if object_name in charact_dict:
                if charact_num_def >= charact_dict[object_name][1]:
                    charact_dict[object_name] = (charact_value, charact_num_def)
            else:
                charact_dict[object_name] = (charact_value, charact_num_def)

    if isdir(temp_path := join('..', 'reports', 'xlsx')):
        path_to_xlsx_folder = temp_path
    elif isdir(temp_path := join('reports', 'xlsx')):
        path_to_xlsx_folder = temp_path
    else:
        raise FileNotFoundError(r"No such file or directory: '..\reports\xlsx' or 'reports\xlsx'")


    if not objects_oil_deposit:
        print('Object_oil_deposit не нашлись(')

    else:
        object_oil_deposit_raw = [i[0][1] for i in objects_oil_deposit]
        objects_oil_deposit = []
        for obj in object_oil_deposit_raw:
            idx_end_name = obj.find('count')
            object_name = obj[7:idx_end_name - 1]
            object_count = obj[idx_end_name + 9:]

            if ' ' in object_name:
                object_name = object_name.replace(' ', '-')

            if not in_field(object_name):
                continue

            if objects_with_kern:
                if object_name in objects_with_kern:
                    with_kern = 'да'
                else:
                    with_kern = 'нет'
            else:
                with_kern = ''

            object_characts = ['', '']
            for idx, charact_dict in enumerate((oil_sat_dict, porosity_dict)):
                if object_name in charact_dict:
                    object_characts[idx] = charact_dict[object_name][0]

            if object_name in kin_values_for_object:
                kin = kin_values_for_object[object_name]
            else:
                kin = ''

            if object_name in kvit_values_for_object:
                kvit = kvit_values_for_object[object_name]
            else:
                kvit = ''

            objects_oil_deposit.append((object_name, int(object_count), with_kern, *object_characts, kin, kvit))
        if open_date and exploit_date and location:
            report_dict = {'Месторождение': [field], 'Год открытия': [open_date],
                           'Год начала эксплуатации': [exploit_date], 'Местоположение': [location],
                           'объекты': [objects_oil_deposit[0][0]], 'количество залежей': [objects_oil_deposit[0][1]],
                           'керн': [objects_oil_deposit[0][2]], 'нефтенасыщенность': [objects_oil_deposit[0][3]],
                           'пористость': [objects_oil_deposit[0][4]], 'КИН': [objects_oil_deposit[0][5]],
                           'Квыт': [objects_oil_deposit[0][6]]}
            report_df = pd.DataFrame(data=report_dict)

            for object_info in objects_oil_deposit[1:]:
                report_df = pd.concat((
                    report_df,
                    pd.DataFrame({
                        'объекты': [object_info[0]],
                        'количество залежей': [object_info[1]],
                        'керн': [object_info[2]],
                        'нефтенасыщенность': [object_info[3]],
                        'пористость': [object_info[4]],
                        'КИН': [object_info[5]],
                        'Квыт': [object_info[6]]
                    })
                ))

            report_df.to_excel(join(path_to_xlsx_folder, f'{field_name}.xlsx'))

            if on_csv:
                print('report_df', report_df)
                return report_df.to_csv(sep='\t').encode('utf-8')

            return None

    if field or open_date or exploit_date or location:
        report_dict = {}

        for attr, label in [
            (field, 'Месторождение'),
            (open_date, 'Год открытия'),
            (exploit_date, 'Год начала эксплуатации'),
            (location, 'Местоположение')
        ]:
            if attr:
                report_dict[label] = [attr]

        report_df = pd.DataFrame(data=report_dict)
        report_df.to_excel(join(path_to_xlsx_folder, f'{field_name}.xlsx'))
        if on_csv:
            print('report_df', report_df)
            return report_df.to_csv(sep='\t').encode('windows-1251')

        return None

    print('Данные об месторождении не найдены')
    return None


if __name__ == '__main__':
    convert_chapter_pdf_to_xml('../reports/pdfs/Архангельское_месторождение_Пересчет_запасов_КГ.pdf', 1, 50, 0,
                               'tester')

    # path_to_test = join('..', 'reports', 'xml', 'archangelsk')
    # paths = [join(path_to_test, f'chapter{i}.xml') for i in CONTENT_A1 + CONTENT_A2]
    # report_xml_to_xlsx(paths, 'archangelsk')

    # convert_chapter_pdf_to_xml('', 0, 0, 2.3,
    #                            join('..', 'reports', 'xml', 'archangelsk_d'),
    #                            path_txt=join('..', 'reports', 'txt', 'archangelsk_d', 'upd', '2.3upd.txt'))

    # for chapter in REPORTS_FOR_THE_TEST['content_a2']:
    #     convert_chapter_pdf_to_xml(PATHS_FOR_REPORTS_PDF['path_a2'], *chapter,
    #                                'test_kin_a')

    # for i in CONTENT_A1 + CONTENT_A2:
    #     convert_chapter_pdf_to_xml('', 0, 0, i, 'test_kin_a',
    #                                f"../reports/txt/archangelsk/upd/{i}upd.txt")

    # for i in range(15):
    #     convert_chapter_pdf_to_xml('', 0, 0, i,
    #                                'test_porosity_and_oil_sat_i',
    #                                f'../reports/txt/ivinskoe/upd/{i}upd.txt')
    #
    # for i in range(15):
    #     convert_chapter_pdf_to_xml('', 0, 0, i,
    #                                'test_porosity_and_oil_sat_sh',
    #                                f'../reports/txt/sherbenskoe/upd/{i}upd.txt')
    #
    # for i in (CONTENT_G1 + CONTENT_G2):
    #     convert_chapter_pdf_to_xml('', 0, 0, i,
    #                                'test_porosity_and_oil_sat_g',
    #                                f'../reports/txt/granichnoe/upd/{i}upd.txt')
    #
    # for i in (CONTENT_B1 + CONTENT_B2):
    #     convert_chapter_pdf_to_xml('', 0, 0, i,
    #                                'test_porosity_and_oil_sat_b',
    #                                f'../reports/txt/baydankinskoe/upd/{i}upd.txt')
    #
    # for i in range(7):
    #     convert_chapter_pdf_to_xml('', 0, 0, i,
    #                                'test_porosity_and_oil_sat_ac',
    #                                f'../reports/txt/acanskoe/upd/{i}upd.txt')
