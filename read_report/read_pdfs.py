import pdfplumber
from cleantext import clean


def clean_text_from_pdf(text: str) -> str:
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


def read_pdf(path: str, idx_beg: int, idx_end: int, clean: bool = True) -> str:
    """
    Читает конкретную часть (обычно это конкретный раздел) из pdf-документа

    :param path: путь, где находится данный документ
    :param idx_beg: страница начала раздела
    :param idx_end: страница конца раздела
    :param clean: флаг, того что применять очистку
    :return: текст из главы документа
    """
    # поскольку нумерация начинается с нуля
    idx_beg -= 1
    text = ''
    with pdfplumber.open(path) as pdf:
        if len(pdf.pages):
            text = ' '.join([
                page.dedupe_chars().extract_text(y_tolerance=6) or '' for page in pdf.pages[idx_beg:idx_end] if page
            ])
    if clean:
        return clean_text_from_pdf(text)
    return text
