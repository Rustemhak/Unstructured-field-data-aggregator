from replace_words import *
from yargy_utils import number_extractor
STAND_GEO_SHORT_NAMES = {'скв.': 'скважина', 'мест.': 'месторождение'}

path = '../reports/pdfs/Архангельское_месторождение_Пересчет_запасов_КГ.pdf'

with open(f'{path[:-3]}txt', "r", encoding="utf-8") as f:
    text = f.read()
    print(text)
    text = replace_short_name(text, STAND_GEO_SHORT_NAMES)
    # перевод в числовое представление
    text = number_extractor.replace_groups(text)
    print(text)
with open(f'{path[:-3]}txt', "w", encoding="utf-8") as f:
    f.write(text)