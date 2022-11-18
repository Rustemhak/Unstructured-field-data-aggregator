# import textract
from cleantext import clean
# import pythoncom
# from read_report.convert_doc_to_docx import save_as_docx

from read_report import read_pdf


def clean_text_from_report(text: str) -> str or None:
    """
    Очищает текст от служебных символов и соединяет слова, если присутсвует знак переноса
    :param text: сырой текст
    :return: обработанный и "чистый" текст
    """
    if text is None:
        return text
    # отдельно убирает знаки переноса
    text = text.replace('-\n', '')
    # text = text.replace('\\\\','\\')
    # очистка с помощью библиотеки cleantext
    text = clean(text,
                 lang='ru', to_ascii=False, lower=False, no_line_breaks=True
                 )
    return text


# def read_report(path, idx_beg=None, idx_end=None, clean=True) -> str:
#     """
#     Поддерживает расширения: pdf, docx
#     :param path: путь к файлу
#     :param idx_beg: страница начала
#     :param idx_end: страница конца
#     :param clean: применять ли очистку
#     :return: текст отчёта
#     """
#     text = ''
#     if path.endswith('.pdf'):
#         text = read_pdf(path, idx_beg, idx_end)
#     elif path.endswith('.docx'):
#         text = textract.process(path, language='rus+eng').decode('utf-8')
#     elif path.lower().endswith('.doc'):
#         pythoncom.CoInitialize()
#         save_as_docx(path)
#         path = path + 'x'
#         text = textract.process(path, language='rus+eng').decode('utf-8')
#     if clean:
#         return clean_text_from_report(text)
#     return text
