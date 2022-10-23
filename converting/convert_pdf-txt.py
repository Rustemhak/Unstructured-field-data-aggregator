from read_report import read_pdf

path = '../reports/pdfs/Архангельское_месторождение_Пересчет_запасов_КГ.pdf'
text = read_pdf(path, idx_beg=1, idx_end=293)
with open(f'{path[:-3]}txt', "w", encoding="utf-8") as f:
    f.write(text)


with open(f'{path[:-3]}txt', "r", encoding="utf-8") as f:
    text = f.read()
print(text)

# path = '../reports/pdfs/Ивинское, книга 1.pdf'
# text = read_pdf(path, idx_beg=1, idx_end=453)
# with open(f'{path[:-3]}txt', "w", encoding="utf-8") as f:
#     f.write(text)
