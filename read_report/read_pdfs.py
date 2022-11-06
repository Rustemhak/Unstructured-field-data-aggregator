import pdfplumber


def read_pdf(path: str, idx_beg: int, idx_end: int) -> str:
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
    return text
