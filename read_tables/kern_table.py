import pandas as pd
import pdfplumber
from yargy import Parser

from read_report.read_report import clean_text_from_report
from read_tables.res_test_table import read_table_res_test_short
from rules.kern_rule import KERN
from yargy_utils import TOKENIZER


def recognize_to_read_table(path: str, idx_beg: int, idx_end: int, clean: bool = True) -> pd.DataFrame:
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
    page_idx = []
    text = ''
    parser = Parser(KERN, tokenizer=TOKENIZER)
    with pdfplumber.open(path) as pdf:
        pages_len = len(pdf.pages)
        if pages_len:
            # text = ' '.join([
            #     page.dedupe_chars().extract_text(y_tolerance=6) or '' for page in pdf.pages[idx_beg:idx_end] if page
            # ])
            for i in range(idx_beg, idx_end):
                if pages_len <= idx_end:
                    break
                page = pdf.pages[i]
                if page:
                    text = page.dedupe_chars().extract_text(y_tolerance=6)
                    text = clean_text_from_report(text)
                    matches = list(parser.findall(text))
                    if matches:
                        page_idx.append(i)
        for idx in page_idx:
            if len(pdf.pages[idx].extract_tables()) > 0:
                # print(pdf.pages[idx].extract_tables())
                # print(len(pdf.pages[idx].extract_tables()))
                return read_table_res_test_short(path, idx)
