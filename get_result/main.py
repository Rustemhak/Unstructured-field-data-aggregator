import os
from os.path import join

from testing.testing import save_objects_with_kern, converting_pdf_to_txt, replacing_words, converting_txt_to_xml, \
    converting_xml_to_xlsx, converting_docx_to_txt
from testing.testing_constant import DOCX_CHAPTERS_PATHS, PATHS_FOR_REPORTS_TXT


def get_result(doc_type: str, path_name: str or [str], content_name: str or [str], field_name: str,
               content: [int or float], in_field=lambda x: True, kern_pages=None, kern=True) -> None:
    """
        Пайплайн для обработки отчета из pdf документа в результирующую xlsx таблицу
        Для обработки сразу нескольких pdf файлов по одному месторождению можно передать
        имена путей и содержаний в виде списка имен (['path_a1', 'path_a2'], ['content_a1', 'content_a2'])

        :param doc_type: формат документа отчета (pdf, docx, doc)
        :param path_name: Имя пути к отчету (Example: 'path_a1')
        :param content_name: Имя содержания отчета (Example: 'content_a1')
        :param field_name: Имя месторождения (Example: 'archangelsk')
        :param content: Список номеров глав отчета
        :param in_field: Функция, возвращающая True если объект входит в перечень объектов месторождения
        :param kern_pages: Диапазон отчета (idx_beg, idx_end, path_name), где находится таблица по керну
        :param kern: Нужно ли извлекать таблицу по керну

        """
    if not isinstance(path_name, list):
        path_name = [path_name]
    if not isinstance(content_name, list):
        content_name = [content_name]

    if kern_pages and kern:
        save_objects_with_kern(kern_pages[2], kern_pages[:2], field_name)

    for path_n, content_n in zip(path_name, content_name):
        if not kern_pages and kern and doc_type == 'pdf':
            save_objects_with_kern(path_n, content_n, field_name)

        if doc_type == 'pdf':
            converting_pdf_to_txt(path_n, content_n, field_name)
        else:
            converting_docx_to_txt(field_name, DOCX_CHAPTERS_PATHS[field_name], content)

        path_to_upd_txt = replacing_words(path_n, content)
        converting_txt_to_xml(content_n, field_name, path_to_upd_txt)

        if PATHS_FOR_REPORTS_TXT[field_name]:
            os.rmdir(PATHS_FOR_REPORTS_TXT[field_name])
        if path_to_upd_txt:
            os.rmdir(path_to_upd_txt)

    converting_xml_to_xlsx(field_name, content, in_field)
    path_to_xml = join('..', 'reports', 'xml', field_name)
    if path_to_xml:
        os.rmdir(path_to_xml)
