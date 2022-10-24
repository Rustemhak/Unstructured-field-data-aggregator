from os import listdir, mkdir
from os.path import isdir, join

from converting.convert_pdf_txt import pdf_to_txt, read_txt
from pipeline_for_testing import convert_chapter_pdf_to_xml, report_xml_to_xlsx
from preprocessing_text import replace_short_name, STAND_GEO_SHORT_NAMES
from testing_constant import PATHS_FOR_REPORTS_PDF, REPORTS_FOR_THE_TEST, PATHS_FOR_REPORTS_TXT, CONTENT_G, CONTENT_B
from yargy_utils import number_extractor


if __name__ == '__main__':
    # print('converting pdf to txt...')
    # path = PATHS_FOR_REPORTS_PDF['path_b2']
    # for idx_beg, idx_end, chapter_id in REPORTS_FOR_THE_TEST['content_b2']:
    #     print(f"{chapter_id} из {REPORTS_FOR_THE_TEST['content_b2'][-1][-1]}")
    #     pdf_to_txt(path, idx_beg, idx_end, chapter_id, 'baydankinskoe')

    # print('replacing words...')
    # path_to_upd_txt = join(*PATHS_FOR_REPORTS_TXT['path_b1'].replace('baydankinskoe', 'baydankinskoe/upd').split('/')[:-1])
    # for i in [i[2] for i in REPORTS_FOR_THE_TEST['content_b2']]:
    #     print(f"{i} из {REPORTS_FOR_THE_TEST['content_b2'][-1][-1]}")
    #     chapter_path = f"{PATHS_FOR_REPORTS_TXT['path_b2']}_{i}.txt"
    #
    #     raw_text = read_txt(chapter_path)
    #     upd_text = replace_short_name(raw_text, STAND_GEO_SHORT_NAMES)
    #     upd_text = number_extractor.replace_groups(upd_text)
    #
    #     if not isdir(path_to_upd_txt):
    #         mkdir(path_to_upd_txt)
    #     with open(f'{path_to_upd_txt}\\{i}upd.txt', "w", encoding="utf-8") as upd_file:
    #         upd_file.write(upd_text)
    #
    # print('converting txt to xml...')
    # for chapter, chapter_path in list(zip(REPORTS_FOR_THE_TEST['content_b2'], listdir(path_to_upd_txt))):
    #     print(f"{chapter[-1]} из {REPORTS_FOR_THE_TEST['content_b2'][-1][-1]}")
    #     convert_chapter_pdf_to_xml("", *chapter, 'baydankinskoe', join(path_to_upd_txt, chapter_path))

    print("Success .////.")

    path_to_xml = join('..', 'reports', 'xml', 'baydankinskoe')
    list_of_paths = [join(path_to_xml, f"chapter{end_path}.xml") for end_path in CONTENT_B]
    report_xml_to_xlsx(list_of_paths, 'baydankinskoe')
