import time
from os import listdir
from os.path import join, isdir
from random import choice
from shutil import rmtree
from string import ascii_letters

import streamlit as st

from testing.pipeline_for_testing import convert_chapter_pdf_to_xml, report_xml_to_xlsx
from testing.main_testing import save_objects_with_kern


def random_string_generator(str_size):
    return ''.join(choice(ascii_letters) for _ in range(str_size))


def get_result(report, on_csv=False):
    """
    Пайплайн для обработки отчета из pdf документа в результирующую xlsx таблицу

    :param report: путь к файлу (pdf).
    :param on_csv: вернуть результат в виде csv файла или в виде xlsx таблицы
    :return: файл результирующей таблицы (xlsx).
    """

    workdir = f"workdir_{random_string_generator(15)}"

    idx_chap = 0
    active = True
    while active:
        active = convert_chapter_pdf_to_xml(report, idx_chap * 50 + 1, (idx_chap + 1) * 50, idx_chap, workdir)
        idx_chap += 1

    content_for_kern = [(i * 50 + 1, (i + 1) * 50) for i in range(idx_chap)]
    save_objects_with_kern(report, content_for_kern, workdir)

    path_to_xml_chapters = join('..', 'reports', 'xml', workdir)
    list_of_paths_to_xml = [join(path_to_xml_chapters, path_to_chapter) for path_to_chapter in
                            listdir(path_to_xml_chapters)]
    result = report_xml_to_xlsx(list_of_paths_to_xml, workdir, on_csv=on_csv)

    if isdir(path_to_xml_chapters):
        rmtree(path_to_xml_chapters)
    path_to_kern = join('..', 'reports', 'objects_with_kern', workdir)
    if isdir(path_to_kern):
        rmtree(path_to_kern)

    if result is not None:
        return result
    return None


if __name__ == '__main__':
    t1 = time.time()
    get_result('../reports/pdfs/Архангельское_месторождение_Пересчет_запасов_КГ.pdf')
    t2 = time.time()
    print(f"time to execute get_result for Архангельское_месторождение_Пересчет_запасов_КГ.pdf = {t2-t1} s")
    get_result('../reports/pdfs/Отчет_Аканское месторождение.pdf')
    print(f"time to execute get_result for Отчет_Аканское месторождение.pdf = {time.time() - t2} s")

