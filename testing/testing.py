import json
from os import listdir, mkdir
from os.path import isdir, join

import pandas as pd
from yargy import Parser, rule

from converting.convert_pdf_txt import pdf_to_txt, read_txt
from pipeline_for_testing import convert_chapter_pdf_to_xml, report_xml_to_xlsx, get_objects_with_kern
from preprocessing_text import replace_short_name, STAND_GEO_SHORT_NAMES
from read_tables.kern_table import recognize_to_read_table
from in_field_functions import in_archangel_field
from testing_constant import *
from yargy_utils import number_extractor, ADJF


def converting_pdf_to_txt(path_name: str, content_name: str, field_name: str) -> None:
    """
    Конвертировать pdf файлы в txt файлы (Из pdf файлов берется текст)

    :param path_name: Имя пути к отчету (Example: 'path_a1')
    :param content_name: Имя содержания отчета (Example: 'content_a1')
    :param field_name: Имя месторождения (Example: 'archangelsk')
    """
    print('converting pdf to txt...')
    path = PATHS_FOR_REPORTS_PDF[path_name]
    for idx_beg, idx_end, chapter_id in REPORTS_FOR_THE_TEST[content_name]:
        print(f"{chapter_id} из {REPORTS_FOR_THE_TEST[content_name][-1][-1]}")
        pdf_to_txt(path, idx_beg, idx_end, chapter_id, field_name)


def replacing_words(path_name: str, content_name: str, field_name: str) -> str:
    """
    Обработать текст txt файлов по месторождению и сохранить в новые txt файлы.
    Вернуть путь к папке с получившимися файлами

    :param path_name: Имя пути к отчету (Example: 'path_a1')
    :param content_name: Имя содержания отчета (Example: 'content_a1')
    :param field_name: Имя месторождения (Example: 'archangelsk')
    :return: Путь к папке с txt файлами обработанного текса
    """
    print('replacing words...')
    path_to_upd_txt = join(
        *PATHS_FOR_REPORTS_TXT[path_name].replace(field_name, f'{field_name}/upd').split('/')[:-1])
    for i in [i[2] for i in REPORTS_FOR_THE_TEST[content_name]]:
        print(f"{i} из {REPORTS_FOR_THE_TEST[content_name][-1][-1]}")
        chapter_path = f"{PATHS_FOR_REPORTS_TXT[path_name]}_{i}.txt"

        raw_text = read_txt(chapter_path)
        upd_text = replace_short_name(raw_text, STAND_GEO_SHORT_NAMES)
        upd_text = number_extractor.replace_groups(upd_text)

        if not isdir(path_to_upd_txt):
            mkdir(path_to_upd_txt)
        with open(f'{path_to_upd_txt}\\{i}upd.txt', "w", encoding="utf-8") as upd_file:
            upd_file.write(upd_text)

    return path_to_upd_txt


def converting_txt_to_xml(content_name: str, field_name: str, path_to_upd_txt: str) -> None:
    """
    Конвертировать txt файлы обработанного текса по месторождению в xml файлы

    :param content_name: Имя содержания отчета (Example: 'content_a1')
    :param field_name: Имя месторождения (Example: 'archangelsk')
    :param path_to_upd_txt: Путь к папке с txt файлами обработанного текста по месторождению
    """
    print('converting txt to xml...')
    content = REPORTS_FOR_THE_TEST[content_name]
    paths_to_upd_txt = [join(path_to_upd_txt, f'{chapter[2]}upd.txt') for chapter in content]
    for chapter, chapter_path in list(zip(content, paths_to_upd_txt)):
        print(f"{chapter[-1]} из {content[-1][-1]}")
        convert_chapter_pdf_to_xml("", *chapter, field_name, chapter_path)

    print("Success .////.")


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


def save_objects_with_kern(path_name: str, content_name: str or tuple[int], field_name) -> [str]:
    """
    Сохранить в json файл и вернуть список объектов с керном

    :param path_name: Имя пути к отчету (Example: 'path_a1')
    :param content_name: Имя содержания отчета (Example: 'content_a1') для поиска таблицы по керну по всему отчету.
        Если передан итерируемый объект со страницами начала и конца диапазона, то поиск ведется только в нем.
    :param field_name: Имя месторождения (Example: 'archangelsk')
    :return: Список объектов с керном, или пустой список, если таблица по керну не найдена
    """
    kern_dataframe = pd.DataFrame()
    path = PATHS_FOR_REPORTS_PDF[path_name]

    if isinstance(content_name, tuple):
        kern_dataframe = pd.concat((kern_dataframe, recognize_to_read_table(path, content_name[0], content_name[1])))
        # kern_dataframe = kern_dataframe.append(recognize_to_read_table(path, content_name[0], content_name[1]))
    else:
        content = REPORTS_FOR_THE_TEST[content_name]
        for chapter in content:
            kern_dataframe = pd.concat((kern_dataframe, recognize_to_read_table(path, chapter[0], chapter[1])))
            # kern_dataframe = kern_dataframe.append(recognize_to_read_table(path, chapter[0], chapter[1]))

    list_of_columns = kern_dataframe.columns
    if list_of_columns:
        list_of_codes_objects = list(kern_dataframe[list_of_columns[0]])

        for i in range(len(list_of_codes_objects)):
            list_of_codes_objects[i] = get_modifed(list_of_codes_objects[i], 'en')

        object_code_dataframe = pd.read_excel(join('..', 'reports', 'xlsx', 'Layers_codes.xlsx'), usecols='M,N')
        codes = list(object_code_dataframe['stratigraphic_index'])
        objects = list(object_code_dataframe['horizon'])

        for i in range(len(codes)):
            codes[i] = get_modifed(codes[i], 'en')

        code_object_dict = {}

        for code, obj in zip(codes, objects):
            code_object_dict[code.replace(' ', '')] = obj

        list_of_objects = []

        # Правило для прилагательного
        # Если в списке кодов объектов есть прилагательное, то там уже названия объектов
        adjf_rule = rule(ADJF)
        adjf_parser = Parser(adjf_rule)

        if adjf_parser.findall(list_of_codes_objects[0]):
            # Если в таблице по керну были указаны имена объектов, то сразу берем их
            list_of_objects = list_of_codes_objects
        else:
            # Иначе сверяем коды объектов из таблицы с именами объектов из Layers_codes.xlsx
            for code in list_of_codes_objects:
                if code:
                    code = code.replace(' ', '')
                    if code in code_object_dict:
                        obj = code_object_dict[code]
                        if isinstance(obj, str):
                            list_of_objects.append(obj.lower())

        if list_of_objects:
            if not isdir(f'../reports/objects_with_kern/{field_name}'):
                mkdir(f'../reports/objects_with_kern/{field_name}')

            with open(
                    f'../reports/objects_with_kern/{field_name}/{path_name.split("_")[1]}.json',
                    'w', encoding='utf-8'
            ) as file:
                json.dump(list_of_objects, file, ensure_ascii=False)
            print('Данные о керне получены')
            return list_of_objects
    print('Информация о керне отсутствует')
    return []


def converting_xml_to_xlsx(field_name: str, content: [], in_field=lambda x: True) -> None:
    """
    Конвертировать xml файлы в xlsx таблицу с результатами алгоритма

    :param field_name: Имя месторождения (Example: 'archangelsk')
    :param content: Имя содержания отчета (Example: 'content_a1')
    :param in_field: Функция, возвращающая True если объект входит в перечень объектов месторождения
    """
    path_to_xml = join('..', 'reports', 'xml', field_name)
    list_of_paths = [join(path_to_xml, f"chapter{chapter_number}.xml") for chapter_number in content]

    report_xml_to_xlsx(list_of_paths, field_name, in_field)


def testing(path_name: str or [str], content_name: str or [str], field_name: str,
            content: [int or float], in_field=lambda x: True, kern_pages=None, kern=True,
            path_to_upd_txt=None) -> None:
    """
    Пайплайн для обработки отчета из pdf документа в результирующую xlsx таблицу
    Для обработки сразу нескольких pdf файлов по одному месторождению можно передать
    имена путей и содержаний в виде списка имен (['path_a1', 'path_a2'], ['content_a1', 'content_a2'])

    :param path_name: Имя пути к отчету (Example: 'path_a1')
    :param content_name: Имя содержания отчета (Example: 'content_a1')
    :param field_name: Имя месторождения (Example: 'archangelsk')
    :param content: Список номеров глав отчета
    :param in_field: Функция, возвращающая True если объект входит в перечень объектов месторождения
    :param kern_pages: Диапазон отчета (idx_beg, idx_end, path_name), где находится таблица по керну
    :param kern: Нужно ли извлекать таблицу по керну
    :param path_to_upd_txt: Путь к папке, где расположены обработаные txt файлы
    """
    if not isinstance(path_name, list):
        path_name = [path_name]
    if not isinstance(content_name, list):
        content_name = [content_name]

    if kern_pages and kern:
        save_objects_with_kern(kern_pages[2], kern_pages[:2], field_name)

    for path_n, content_n in zip(path_name, content_name):
        if not kern_pages and kern:
            save_objects_with_kern(path_n, content_n, field_name)
        if not path_to_upd_txt:
            converting_pdf_to_txt(path_n, content_n, field_name)
            path_to_upd_txt = replacing_words(path_n, content_n, field_name)
        converting_txt_to_xml(content_n, field_name, path_to_upd_txt)

    converting_xml_to_xlsx(field_name, content, in_field)


if __name__ == '__main__':
    # save_objects_with_kern('path_i1', (84, 84), 'ivinskoe')
    # save_objects_with_kern('path_a1', (78, 78), 'archangelsk')

    # converting_txt_to_xml('content_a1', 'archangelsk', join('..', 'reports', 'txt', 'archangelsk', 'upd'))

    # testing(
    #     ['path_a1', 'path_a2'],
    #     ['content_a1', 'content_a2'],
    #     'archangelsk',
    #     CONTENT_A1 + CONTENT_A2,
    #     in_field=in_archangel_field,
    #     kern=False,
    #     path_to_upd_txt=join('..', 'reports', 'txt', 'archangelsk', 'upd')
    # )
    # testing(
    #     'path_i1',
    #     'content_i1',
    #     'ivinskoe',
    #     CONTENT_I,
    #     kern=False,
    #     path_to_upd_txt=join('..', 'reports', 'txt', 'ivinskoe', 'upd')
    # )
    # testing(
    #     'path_sh1',
    #     'content_sh1',
    #     'sherbenskoe',
    #     CONTENT_SH,
    #     kern=False,
    #     path_to_upd_txt=join('..', 'reports', 'txt', 'sherbenskoe', 'upd')
    # )
    converting_xml_to_xlsx('sherbenskoe', CONTENT_SH)
    # testing(
    #     ['path_b1', 'path_b2'],
    #     ['content_b1', 'content_b2'],
    #     'baydankinskoe',
    #     CONTENT_B1 + CONTENT_B2,
    #     kern=False,
    #     path_to_upd_txt=join('..', 'reports', 'txt', 'baydankinskoe', 'upd')
    # )
    # testing(
    #     'path_ac',
    #     'content_ac1',
    #     'acanskoe',
    #     CONTENT_AC,
    #     kern=False,
    #     path_to_upd_txt=join('..', 'reports', 'txt', 'acanskoe', 'upd')
    # )
    # testing(
    #     ['path_g1', 'path_g2'],
    #     ['content_g1', 'content_g2'],
    #     'granichnoe',
    #     CONTENT_G1,
    #     kern=False,
    #     path_to_upd_txt=join('..', 'reports', 'txt', 'granichnoe', 'upd')
    # )

    # save_objects_with_kern('path_a1', (78, 78), 'archangelsk')
    # save_objects_with_kern('path_i1', 'content_i1', 'ivinskoe')
    # save_objects_with_kern('path_sh1', 'content_sh1', 'sherbenskoe')
    # save_objects_with_kern('path_b1', 'content_b1', 'baydankinskoe')
    # save_objects_with_kern('path_b2', 'content_b2', 'baydankinskoe')
    # save_objects_with_kern('path_ac', 'content_ac1', 'acanskoe')
    # save_objects_with_kern('path_g1', 'content_g1', 'granichnoe')
    # save_objects_with_kern('path_g2', 'content_g2', 'granichnoe')

    # converting_xml_to_xlsx('archangelsk', CONTENT_A1 + CONTENT_A2, in_archangel_field)
    # converting_xml_to_xlsx('ivinskoe', CONTENT_I)
    # converting_xml_to_xlsx('sherbenskoe', CONTENT_SH)
    # converting_xml_to_xlsx('baydankinskoe', CONTENT_B1 + CONTENT_B2)
    # converting_xml_to_xlsx('acanskoe', CONTENT_AC)
    # converting_xml_to_xlsx('granichnoe', CONTENT_G1 + CONTENT_G2)
