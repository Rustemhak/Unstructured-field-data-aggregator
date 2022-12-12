from os import mkdir
from os.path import isdir, join
from read_report import read_pdf


def pdf_to_txt(path: str, idx_beg: int, idx_end: int, chapter_id: int, txt_dir_name: str) -> None:
    text = read_pdf(path, idx_beg=idx_beg, idx_end=idx_end)
    path_to_txt_dir = join('..', 'reports', 'txt')
    path_to_txt = join(path_to_txt_dir, txt_dir_name)

    if not isdir(path_to_txt_dir):
        mkdir(path_to_txt_dir)

    if not isdir(path_to_txt):
        mkdir(path_to_txt)

    with open(join(path_to_txt, f"{chapter_id}raw.txt"), "w", encoding="utf-8") as file_txt:
        file_txt.write(text)


def read_txt(path) -> str:
    print(path)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text
