import json
from os import listdir, mkdir
from os.path import isdir, join

import pandas as pd

from converting.convert_pdf_txt import pdf_to_txt, read_txt
from pipeline_for_testing import convert_chapter_pdf_to_xml, report_xml_to_xlsx, get_objects_with_kern
from preprocessing_text import replace_short_name, STAND_GEO_SHORT_NAMES
from read_tables.kern_table import recognize_to_read_table
from in_field_functions import in_archangel_field
from testing_constant import *
from yargy_utils import number_extractor


def converting_pdf_to_txt(path_name: str, content_name: str, field_name: str):
    """

    :param path_name:
    :param content_name:
    :param field_name:
    :return:
    """
    print('converting pdf to txt...')
    path = PATHS_FOR_REPORTS_PDF[path_name]
    for idx_beg, idx_end, chapter_id in REPORTS_FOR_THE_TEST[content_name]:
        print(f"{chapter_id} из {REPORTS_FOR_THE_TEST[content_name][-1][-1]}")
        pdf_to_txt(path, idx_beg, idx_end, chapter_id, field_name)


def replacing_words(path_name: str, content_name: str, field_name: str):
    """

    :param path_name:
    :param content_name:
    :param field_name:
    :return:
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


def converting_txt_to_xml(content_name: str, field_name: str, path_to_upd_txt: str):
    """

    :param content_name:
    :param field_name:
    :param path_to_upd_txt:
    :return:
    """
    print('converting txt to xml...')
    for chapter, chapter_path in list(zip(REPORTS_FOR_THE_TEST[content_name], listdir(path_to_upd_txt))):
        print(f"{chapter[-1]} из {REPORTS_FOR_THE_TEST[content_name][-1][-1]}")
        convert_chapter_pdf_to_xml("", *chapter, field_name, join(path_to_upd_txt, chapter_path))

    print("Success .////.")


def get_modifed(string: str):
    """Возвращает модифицированную строку. Приводит строку к английским буквам."""
    eq = {
        'o': 'о', 'e': 'е',
        'c': 'с', 'p': 'р',
        'O': 'О', 'E': 'Е',
        'C': 'С', 'P': 'Р'
    }
    if string:
        for en, ru in eq.items():
            string = string.replace(ru, en)

        return string
    return None


def save_objects_with_kern(path_name: str, content_name: str or tuple[int], field_name) -> [str]:
    """

    :param path_name:
    :param content_name:
    :param field_name:
    :return:
    """
    kern_dataframe = pd.DataFrame()
    path = PATHS_FOR_REPORTS_PDF[path_name]
    if isinstance(content_name, tuple):
        kern_dataframe = kern_dataframe.append(recognize_to_read_table(path, content_name[0], content_name[1]))
    else:
        content = REPORTS_FOR_THE_TEST[content_name]
        for chapter in content:
            kern_dataframe = kern_dataframe.append(recognize_to_read_table(path, chapter[0], chapter[1]))

    list_of_columns = kern_dataframe.columns
    list_of_codes_objects = list(kern_dataframe[list_of_columns[0]])

    for i in range(len(list_of_codes_objects)):
        list_of_codes_objects[i] = get_modifed(list_of_codes_objects[i])

    object_code_dataframe = pd.read_excel(join('..', 'reports', 'xlsx', 'Layers_codes.xlsx'), usecols='M,N')
    codes = list(object_code_dataframe['stratigraphic_index'])
    objects = list(object_code_dataframe['horizon'])

    for i in range(len(codes)):
        codes[i] = get_modifed(codes[i])

    code_object_dict = {}

    for code, obj in zip(codes, objects):
        code_object_dict[code.replace(' ', '')] = obj

    list_of_objects = []
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


def converting_xml_to_xlsx(field_name: str, content: [], in_field=lambda x: True):
    """

    :param field_name:
    :param content:
    :param contents_name:
    :param in_field:
    :return:
    """
    path_to_xml = join('..', 'reports', 'xml', field_name)
    list_of_paths = [join(path_to_xml, f"chapter{chapter_number}.xml") for chapter_number in content]

    report_xml_to_xlsx(list_of_paths, field_name, in_field)


def testing(path_name: str or [str], content_name: str or [str], field_name: str,
            content: [], in_field=lambda x: True):
    """

    :param path_name:
    :param content_name:
    :param field_name:
    :param content:
    :param in_field:
    :return:
    """
    if not isinstance(path_name, list):
        path_name = [].append(path_name)
    if not isinstance(content_name, list):
        content_name = [].append(content_name)

    for name in zip(path_name, content_name):
        save_objects_with_kern(name[0], name[1], field_name)
        converting_pdf_to_txt(*name, field_name)
        path_to_upd_txt = replacing_words(*name, field_name)
        converting_txt_to_xml(name[1], field_name, path_to_upd_txt)

    converting_xml_to_xlsx(field_name, content, in_field)

    # if isinstance(content[0], list):
    #     for con in content:
    #         converting_xml_to_xlsx(field_name, con, path_name, full_content, in_field)
    # else:
    #     converting_xml_to_xlsx(field_name, content, path_name, full_content, in_field)


if __name__ == '__main__':
    # save_objects_with_kern('path_i1', (84, 84), 'ivinskoe')
    # save_objects_with_kern('path_a1', (78, 78), 'archangelsk')

    # testing(
    #     ['path_a1', 'path_a2'],
    #     ['content_a1', 'content_a2'],
    #     'archangelsk',
    #     CONTENT_A1 + CONTENT_A2,
    #     in_archangel_field
    # )
    # testing(
    #     'path_i1',
    #     'content_i1',
    #     'ivinskoe',
    #     CONTENT_I
    # )
    # testing(
    #     'path_sh1',
    #     'content_sh',
    #     'sherbenskoe',
    #     CONTENT_SH
    # )
    # testing(
    #     ['path_b1', 'path_b2'],
    #     ['content_b1', 'content_b2'],
    #     'baydankinskoe',
    #     (CONTENT_B1, CONTENT_B2)
    # )
    # testing(
    #     'path_ac',
    #     'content_ac',
    #     'acanskoe',
    #     CONTENT_AC
    # )
    # testing(
    #     ['path_g1', 'path_g2'],
    #     ['content_g1', 'content_g2'],
    #     'granichnoe',
    #     CONTENT_G1
    # )

    # save_objects_with_kern('path_i1', 'content_i1', 'ivinskoe')
    # save_objects_with_kern('path_sh1', 'content_sh1', 'sherbenskoe')
    # save_objects_with_kern('path_b1', 'content_b1', 'baydankinskoe')
    # save_objects_with_kern('path_b2', 'content_b2', 'baydankinskoe')
    # save_objects_with_kern('path_ac', 'content_ac1', 'acanskoe')
    # save_objects_with_kern('path_g1', 'content_g1', 'granichnoe')
    # save_objects_with_kern('path_g2', 'content_g2', 'granichnoe')

    # converting_xml_to_xlsx('archangelsk', CONTENT_A1 + CONTENT_A2, in_archangel_field)
    converting_xml_to_xlsx('ivinskoe', CONTENT_I)
    # converting_xml_to_xlsx('sherbenskoe', CONTENT_SH)
    # converting_xml_to_xlsx('baydankinskoe', CONTENT_B1 + CONTENT_B2)
    # converting_xml_to_xlsx('acanskoe', CONTENT_AC)
    # converting_xml_to_xlsx('granichnoe', CONTENT_G1 + CONTENT_G2)
