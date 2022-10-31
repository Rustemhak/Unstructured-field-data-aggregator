import xml.etree.ElementTree as ET
from os import mkdir
from os.path import isdir

from yargy import Parser
import pandas as pd

from converting.convert_pdf_txt import read_txt
from preprocessing_text import replace_short_name, STAND_GEO_SHORT_NAMES
from read_report import read_pdf
from rules.date_exploit_rule import EXPLOIT_DATE
from rules.date_open_rule import OPEN_DATE
from rules.field_rule import FIELD, NAME
from rules.location_rule import LOC
from rules.oil_deposit_rule import set_tag_attr_oil_deposit
from sentenizer.segment_sentences import segment_to_sent
from xml_making.tag_making import set_xml_tag_sentences, set_tag_attr, set_tag_attr_for_field
from yargy_utils import TOKENIZER


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


def convert_chapter_pdf_to_xml(path_pdf: str, idx_beg_chap: int, idx_end_chap: int, chap_id: int, path_xml,
                               path_txt: str = None):
    """
    Пайплайн для конвертации главы отчёта в формате pdf в XML
    Результат в 'output.xml'

    :param path_pdf: путь, где находится данный документ
    :param idx_beg_chap: страница начала раздела
    :param idx_end_chap: страница конца раздела
    :param chap_id: номер главы
    :param path_xml: путь для сохранения xml в папке reports/xml
    :param path_txt: путь к документу в формате txt, если документ был конвертирован из pdf в txt
    """

    if path_txt is None:
        text = read_pdf(path_pdf, idx_beg_chap, idx_end_chap)
    else:
        text = read_txt(path_txt)

    # text = extractor.replace_groups(text)
    # создание тега "отчёт"
    report = ET.Element('report')
    # создание тега "главы"
    chapters = ET.SubElement(report, 'chapters')
    # создание тега "глава"
    chapter = ET.SubElement(chapters, 'chapter')
    chapter.set('ID', str(chap_id))
    # chapter.text = text

    text = replace_short_name(text, STAND_GEO_SHORT_NAMES)
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

    tree = ET.ElementTree(report)
    indent(report)
    if report is not None:
        # writing xml
        # print(report.items())
        ET.dump(report)
        path_to_xml_dir = f"..//reports//xml//{path_xml}"
        if not isdir(path_to_xml_dir):
            mkdir(path_to_xml_dir)
        tree.write(f"{path_to_xml_dir}//chapter{chap_id}.xml", encoding="utf-8", xml_declaration=True)


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


def report_xml_to_xlsx(list_paths_chapters: [str], report_name: str, in_field=lambda x: True):
    """
    Перевод отчета из xml в xlsx.

    :param list_paths_chapters: список путей к главам отчета в формате xml.
    :param in_field: функция для проверки имен объектов на их наличие в месторождении.
    """
    report_pd = pd.DataFrame()
    for chapter_path in list_paths_chapters:
        chapter_pd = chapter_xml_to_pd(chapter_path)
        report_pd = pd.concat((report_pd, chapter_pd))

    field = report_pd['field'].dropna().unique()[0]
    try:
        exploit_date = report_pd['exploit_date'].dropna().unique()[0]
        open_date = report_pd['open_date'].dropna().unique()[0]
        location = report_pd['location'].dropna().unique()[0]
        # oil_deposit = report_pd['oil_deposit'].dropna()
    except KeyError:
        raise KeyError("Одна из характеристик не была найдена")

    list_of_columns_object = []
    for column in list(report_pd.columns):
        if 'object' in column:
            list_of_columns_object.append(column)
    object_oil_deposit = [list(report_pd[column].dropna().items()) for column in list_of_columns_object]
    if not object_oil_deposit:
        print('Object_oil_deposit не нашлись(')
    else:
        object_oil_deposit_raw = [i[0][1] for i in object_oil_deposit]
        object_oil_deposit = []
        for obj in object_oil_deposit_raw:
            idx_end_name = obj.find('count')
            object_name = obj[7:idx_end_name - 1]
            object_count = obj[idx_end_name + 9:]

            if not in_field(object_name):
                continue

            object_oil_deposit.append((object_name, int(object_count)))

        report_dict = {'Месторождение': [field], 'Год открытия': [open_date],
                       'Год начала эксплуатации': [exploit_date], 'Местоположение': [location],
                       'объекты': [object_oil_deposit[0][0]], 'количество залежей': [object_oil_deposit[0][1]]}
        report_df = pd.DataFrame(data=report_dict)
        for i in object_oil_deposit[1:]:
            report_df = report_df.append({'объекты': i[0], 'количество залежей': i[1]}, ignore_index=True)

        report_df.to_excel(f"..//reports//xlsx//{report_name}.xlsx")
