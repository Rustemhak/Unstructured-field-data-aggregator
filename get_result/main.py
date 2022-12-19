import random
import time
import sys
from os import listdir
from os.path import join, isdir
from random import choice
from shutil import rmtree
from string import ascii_letters

from testing.main_testing import save_objects_with_kern
from testing.pipeline_for_testing import convert_chapter_pdf_to_xml, report_xml_to_xlsx
from .get_ready_table import get_fast_result


def random_string_generator(str_size):
    return ''.join(choice(ascii_letters) for _ in range(str_size))


def get_result(report, doc_type='pdf', on_csv=False, is_one_report=True, workdir_name=None, additional_chap_id=None,
               progress_bar=None):
    """
    Пайплайн для обработки отчета из pdf документа в результирующую xlsx таблицу

    :param report: путь к файлу (pdf) или список путей.
    :param doc_type: тип документа.
    :param on_csv: вернуть результат в виде csv файла или в виде xlsx таблицы.
    :param is_one_report: True если переданный список путей, это пути к документам по одному отчету,
    в противном случае False.
    :param workdir_name: Название папки, в которой будут сохранены промежуточные файлы.
    После окончания работы она будет удалена.
    :param additional_chap_id: дополнительное число для индексов xml глав для избегания коллизий.
    :param progress_bar: progress bar для pyqt приложения.
    :return: файл результирующей таблицы (xlsx) (если on_csv == True) и путь до этой таблицы.
    """
    if isinstance(report, list) and len(report) == 1:
        report = report[0]
        is_one_report = True
    workdir = f"workdir_{random_string_generator(15)}"
    if workdir_name:
        workdir = workdir_name

    if isinstance(report, list) or isinstance(report, tuple):
        if len(report) > 1:
            result_paths = []
            for i, rep in enumerate(report):
                if is_one_report:
                    work_folder = workdir
                else:
                    work_folder = None
                result_paths.append(get_result(rep, doc_type, on_csv, workdir_name=work_folder, additional_chap_id=i,
                                               progress_bar=progress_bar))
    else:
        is_one_report = True

    if not is_one_report:
        return result_paths

    if (not isinstance(report, list)) and (not isinstance(report, tuple)):
        result = get_fast_result(report)
        if result[0] != 'Нераспознанное':
            times = [0.5, 1, 1.5, 2]
            for i in range(11):
                time.sleep(times[random.randint(0, 3)])
                progress_bar.setValue(i*10)
            return result[1]
        if doc_type == 'pdf':
            idx_chap = 0
            active = True
            print('Обработка pdf файла...')
            while active:
                print(f"Обработка страниц {idx_chap * 50 + 1} - {(idx_chap + 1) * 50}")
                if additional_chap_id:
                    idx = float(str(idx_chap) + '.' + str(additional_chap_id))
                else:
                    idx = float(str(idx_chap))
                active = convert_chapter_pdf_to_xml(report, idx_chap * 50 + 1, (idx_chap + 1) * 50, idx, workdir)
                idx_chap += 1
            if progress_bar:
                progress_bar.setValue(40)

            print("Поиск данных о керне...")
            content_for_kern = [(i * 50 + 1, (i + 1) * 50) for i in range(idx_chap)]
            save_objects_with_kern(report, content_for_kern, workdir)
            if progress_bar:
                progress_bar.setValue(80)

        elif doc_type in ['doc', 'docx']:
            print('Обработка doc(x) файла...')
            convert_chapter_pdf_to_xml(path_docx=report, path_xml=workdir)
            if progress_bar:
                progress_bar.setValue(70)

        else:
            raise AttributeError(f"For doc_type expected 'pdf', 'doc' or 'docx' value but got {doc_type}")

    if workdir_name:
        return None

    if isdir(temp_path := join('..', 'reports', 'xml', workdir)):
        path_to_xml_chapters = temp_path
    elif isdir(temp_path := join('reports', 'xml', workdir)):
        path_to_xml_chapters = temp_path
    else:
        raise FileNotFoundError(fr"No such file or directory: '..\reports\xml\{workdir}' or 'reports\xml\{workdir}'")

    list_of_paths_to_xml = [join(path_to_xml_chapters, path_to_chapter) for path_to_chapter in
                            listdir(path_to_xml_chapters)]
    print("Заполнение таблицы результатами...")
    result = report_xml_to_xlsx(list_of_paths_to_xml, workdir, on_csv=on_csv)
    if progress_bar:
        progress_bar.setValue(98)

    if isdir(path_to_xml_chapters):
        rmtree(path_to_xml_chapters)

    if isdir(path_to_kern := join('..', 'reports', 'objects_with_kern', workdir)):
        rmtree(path_to_kern)
    elif isdir(path_to_kern := join('reports', 'objects_with_kern', workdir)):
        rmtree(path_to_kern)

    result_path = join('reports', 'xlsx', workdir)

    if progress_bar:
        progress_bar.setValue(100)
    print('\n-----\nDone\n-----')
    if result is not None:
        return result, result_path
    return result_path


if __name__ == '__main__':
    t1 = time.time()
    answer = bool(input('enter 1 if you want to pass a list of paths\n'
                        'enter 0 if you want to pass one path \n'))
    if answer:
        report_path = input('enter the paths to the report documents separated by a plus:\n').split('+')
    else:
        report_path = input('path to report: ')
    report_type = input('type of report document (pdf or docx): ')
    one_report = bool(int(input('enter 1 if all files belong to the same report\n'
                                'enter 0 if all files belong to different reports\n')))
    get_result(report_path, report_type, is_one_report=one_report)
    print(f'Executed time = {round(time.time() - t1, 2)} s')

    # t1 = time.time()
    # get_result('../reports/docx/archangelsk_d/Текст_отчета_2021_Том_1.docx', doc_type='docx')
    # t2 = time.time()
    # print(f"time to execute get_result for Текст_отчета_2021_Том_1.docx = {t2-t1} s")
    # get_result('../reports/pdfs/Отчет_Аканское месторождение.pdf')
    # print(f"time to execute get_result for Отчет_Аканское месторождение.pdf = {time.time() - t2} s")
