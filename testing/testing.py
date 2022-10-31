from os import listdir, mkdir
from os.path import isdir, join

from converting.convert_pdf_txt import pdf_to_txt, read_txt
from pipeline_for_testing import convert_chapter_pdf_to_xml, report_xml_to_xlsx
from preprocessing_text import replace_short_name, STAND_GEO_SHORT_NAMES
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


def converting_xml_to_xlsx(field_name: str, content: [], path_name, content_name, in_field=lambda x: True):
    """

    :param field_name:
    :param content:
    :param path_name:
    :param content_name:
    :param in_field:
    :return:
    """
    path_to_pdf_document = PATHS_FOR_REPORTS_PDF[path_name]
    path_to_xml = join('..', 'reports', 'xml', field_name)
    list_of_paths = [join(path_to_xml, f"chapter{chapter_number}.xml") for chapter_number in content]

    if isinstance(content_name, tuple):
        full_content = content_name
    else:
        full_content = REPORTS_FOR_THE_TEST[content_name]

    report_xml_to_xlsx(list_of_paths, field_name, path_to_pdf_document, full_content, in_field)


def testing(path_name: str or [str], content_name: str or [str], field_name: str,
            content: [], in_field=lambda x: True, full_content=None):
    """

    :param path_name:
    :param content_name:
    :param field_name:
    :param content:
    :param in_field:
    :param full_content:
    :return:
    """
    if not isinstance(path_name, list):
        path_name = [].append(path_name)
    if not isinstance(content_name, list):
        content_name = [].append(content_name)

    for name in zip(path_name, content_name):
        converting_pdf_to_txt(*name, field_name)
        path_to_upd_txt = replacing_words(*name, field_name)
        converting_txt_to_xml(name[1], field_name, path_to_upd_txt)

    if not full_content:
        full_content = content_name

    converting_xml_to_xlsx(field_name, content, path_name, full_content, in_field)

    # if isinstance(content[0], list):
    #     for con in content:
    #         converting_xml_to_xlsx(field_name, con, path_name, full_content, in_field)
    # else:
    #     converting_xml_to_xlsx(field_name, content, path_name, full_content, in_field)


if __name__ == '__main__':
    testing(
        ['path_a1', 'path_a2'],
        ['content_a1', 'content_a2'],
        'archangelsk',
        CONTENT_A1 + CONTENT_A2,
        in_archangel_field
    )
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

    # converting_xml_to_xlsx('archangelsk', (CONTENT_A1, CONTENT_A2), 'path_a1', (78, 79), in_archangel_field)
    # converting_xml_to_xlsx('ivinskoe', CONTENT_I, 'path_a1', (78, 79), in_archangel_field)
    # converting_xml_to_xlsx('sherbenskoe', CONTENT_SH, 'path_a1', (78, 79), in_archangel_field)
    # converting_xml_to_xlsx('baydankinskoe', (CONTENT_B1, CONTENT_B2), 'path_a1', (78, 79), in_archangel_field)
    # converting_xml_to_xlsx('acanskoe', CONTENT_AC, 'path_a1', (78, 79), in_archangel_field)
    # converting_xml_to_xlsx('granichnoe', (CONTENT_G1, CONTENT_G2), 'path_a1', (78, 79), in_archangel_field)
