from os import listdir, rmdir
from os.path import join, isdir

from testing.pipeline_for_testing import convert_chapter_pdf_to_xml, report_xml_to_xlsx
from testing.testing import save_objects_with_kern


def get_result(report):
    """
    Пайплайн для обработки отчета из pdf документа в результирующую xlsx таблицу

    :param report: файл отчета (pdf).
    :return: файл результирующей таблицы (xlsx).
    """

    idx_chap = 0
    active = True
    while active:
        active = convert_chapter_pdf_to_xml(report, idx_chap * 50, (idx_chap + 1) * 50, idx_chap, 'workdir')
        idx_chap += 1

    content_for_kern = [(i * 50, (i + 1) * 50) for i in range(idx_chap - 1)]
    save_objects_with_kern(report, content_for_kern, 'workdir')

    path_to_xml_chapters = join('..', 'reports', 'xml', 'workdir')
    list_of_paths_to_xml = [join(path_to_xml_chapters, path_to_chapter) for path_to_chapter in
                            listdir(path_to_xml_chapters)]
    report_xml_to_xlsx(list_of_paths_to_xml, 'workdir')

    if isdir(path_to_xml_chapters):
        rmdir(path_to_xml_chapters)
    path_to_kern = join('..', 'reports', 'objects_with_kern', 'workdir')
    if isdir(path_to_kern):
        rmdir(path_to_kern)

    return join('..', 'reports', 'xlsx', 'workdir.xlsx')
