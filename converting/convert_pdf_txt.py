from os import mkdir
from os.path import isdir, join
from read_report import read_pdf


def pdf_to_txt(path: str, idx_beg: int, idx_end: int, chapter_id: int, txt_dir_name: str) -> None:
    text = read_pdf(path, idx_beg=idx_beg, idx_end=idx_end)
    path_to_txt = path[:-4].replace('pdfs', 'txt/'+txt_dir_name)
    path_to_txt_dir = join(*path_to_txt.split('/')[:-1])

    if not isdir(path_to_txt_dir):
        mkdir(path_to_txt_dir)

    with open(path_to_txt + f"_{chapter_id}.txt", "w", encoding="utf-8") as f:
            f.write(text)


def read_txt(path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text
