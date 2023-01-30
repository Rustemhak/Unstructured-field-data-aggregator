import textract, pdfplumber
import glob
import os
import pythoncom
from cleantext import clean
import shutil
import pymorphy2
# from IPython.display import display
import win32com
# pip install ipymarkup
from ipymarkup import show_span_ascii_markup as show_markup
import time
from yargy.record import Record
from yargy import (
    Parser,
    or_, rule,
    and_
)

from yargy.pipelines import morph_pipeline
from yargy.predicates import (
    eq, in_, dictionary,
    type, gram, is_capitalized
)
from yargy.tokenizer import MorphTokenizer
from yargy import interpretation as interp
from yargy.interpretation import fact, attribute
from yargy.relations import gnc_relation

UPLOAD_FOLDER = 'uploads'


class Synonyms(Record):
    __attributes__ = ['name', 'synonyms']

    def __init__(self, name, synonyms=()):
        self.name = name
        self.synonyms = synonyms


os.environ['PATH'] += os.pathsep + os.path.join(os.getcwd(), 'Tesseract-OCR')
extensions = [
    '.xlsx', '.docx', '.pptx',
    '.pdf', '.txt', '.md', '.htm', 'html',
    '.jpg', '.jpeg', '.png', '.gif', '.doc',
    '.tif', '.xls', '.zip', '.rar'
]
archive_ext = ['.zip', '.rar']
FIELDS = ['Аканское', 'Архангельское', 'Ивинское', 'Граничное', 'Байданкинское', 'Матросовское', 'Щербеньское',
          'Ивинский', 'Аканский', 'Архангельский', 'Граничный', 'Байданкинский', 'Матросовский', 'Щербеньский']
NAMES1 = [
    Synonyms('месторожден',
             ['м', 'мес', 'мест', 'местор', 'месторож', 'месторожд', 'месторожден'])
]
NAMES2 = [
    Synonyms('месторождение',
             ['м-е', 'м-ие', 'мес-е', 'мес-ие', 'мест-е', 'мест-ие', 'местор-е', 'местор-ие', 'месторож-е',
              'месторож-ие', 'месторожд-е', 'месторожд-ие'])
]
names1 = []
mapping = {}
for record in NAMES1:
    name = record.name
    names1.append(name)
    mapping[name] = name
    for synonym in record.synonyms:
        names1.append(synonym)
        mapping[synonym] = name

names2 = []
mapping = {}
for record in NAMES2:
    name = record.name
    names2.append(name)
    mapping[name] = name
    for synonym in record.synonyms:
        names2.append(synonym)
        mapping[synonym] = name

gnc = gnc_relation()
Object = fact(
    'Object',
    ['first', 'last']
)
NOUN = gram('NOUN')
ADJF = gram('ADJF')
DOT = eq('.')
TOKENIZER = MorphTokenizer()

NAME1 = morph_pipeline(names1).interpretation(
    Object.last.normalized().custom(mapping.get)
)
NAME2 = morph_pipeline(names2).interpretation(
    Object.last.normalized().custom(mapping.get)
)
NAME1 = rule(NAME1,
             DOT)
NAME = rule(or_(NAME1, NAME2))
FIELD_NAME = morph_pipeline(['ИВИНСКОГО', 'Ивинское', 'Ивинский', 'Ивинского'])
MODIFIER_ADJF = rule(and_(ADJF,
                          is_capitalized()))

MODIFIER = or_(FIELD_NAME, MODIFIER_ADJF)
OBJECT1 = rule(MODIFIER.interpretation(Object.first.inflected()),
               ADJF.optional().repeatable(),
               NAME.match(gnc)
               )
OBJECT2 = rule(
    NAME.match(gnc),
    MODIFIER.interpretation(Object.first.inflected()).match(gnc),
    ADJF.optional().repeatable()
)
OBJECT = rule(or_(OBJECT1, OBJECT2)).interpretation(Object)

time_list = []


def processor(path):
    pdf_consists_images = 0
    try:
        if path.lower().endswith('.pdf'):
            with pdfplumber.open(path) as pdf:
                if len(pdf.pages):
                    text = ' '.join([
                        page.extract_text() or '' for page in pdf.pages[:6] if page
                    ])
    except Exception as exception:
        return None
    return text


def show_matches(rule, *lines):
    parser = Parser(rule)
    morph = pymorphy2.MorphAnalyzer()

    for line in lines:
        matches = parser.findall(line)
        matches = sorted(matches, key=lambda _: _.span)
        spans = [_.span for _ in matches]

        # show_markup(line, spans)
        if matches:
            facts = [_.fact for _ in matches]
            # if len(facts) == 1:
            #     facts = facts[0]
            # display(facts)
            return facts


def find_max_cnt_name(obj_dict):
    cnt_max = 0
    name = 'Нераспознанное'
    for k, v in sorted(obj_dict.items()):
        if v > cnt_max:
            name = k
            cnt_max = v
    return name


def processor_file(file, OBJECT):
    start_time = time.time()

    text = processor(file) + ' '.join(file.split('\\'))
    if text is not None:
        obj_list = show_matches(OBJECT, text)
        obj_dict = {}
        if obj_list is not None:
            for obj in obj_list:
                if hasattr(obj, 'first'):
                    name = obj.first
                    # print('имя м-я', name)
                    if name is None:
                        name = ''
                    if name.capitalize() in FIELDS:
                        if name in obj_dict.keys():
                            obj_dict[name] += 1
                        else:
                            obj_dict[name] = 1
        # print(obj_dict)
        field_name = find_max_cnt_name(obj_dict).capitalize()
        final_time = time.time()
        time_of_processing = final_time - start_time
        time_list.append(time_of_processing)

        # print("--- Алгоритм обрабатывал файл " + file + " %s seconds ---" % time_of_processing + "\n")

        return field_name

    # def find_field_name(file_path, filename):
    #     path = file_path
    #     file = os.path.join(file_path, filename)
    #     extension = os.path.splitext(file)[1].lower()
    #     if extension in extensions:
    #         return processor_file(file, OBJECT)
    #     else:
    #         return None


def get_fast_result(f):
    """
    Если возвращает первое значение как "Нераспознанное", тогда применяется сам алгоритм
    :param f: отчёт по месторождению
    :return: название месторождения; результат для него

    """

    field_name = processor_file(f, OBJECT)
    result_file = 'reports/result/Сводная_таблица_по_месторождениям.xlsx'
    if field_name in ['Архангельское', 'Архангельский']:
        field_name = 'Архангельское'
        result_file = 'reports/result/Архангельское.xlsx'
    elif field_name in ['Аканское', 'Аканский']:
        field_name = 'Аканское'
        result_file = 'reports/result/Аканское.xlsx'
    elif field_name in ['Байданкинское', 'Байданкинский']:
        field_name = 'Байданкинское'
        result_file = 'reports/result/Байданкинское.xlsx'
    elif field_name in ['Бухараевское', 'Бухараевский']:
        field_name = 'Бухараевское'
        result_file = 'reports/result/'
    elif field_name in ['Граничное', 'Граничный']:
        field_name = 'Граничное'
        result_file = 'reports/result/Граничное.xlsx'
    elif field_name in ['Ивинское', 'Ивинский']:
        field_name = 'Ивинское'
        result_file = 'reports/result/Ивинское.xlsx'
    elif field_name in ['Матросовское', 'Матросовский']:
        field_name = 'Бухараевское'
        result_file = 'reports/result/Бухараевское.xlsx'
    elif field_name in ['Щербеньское', 'Щербеньский']:
        field_name = 'Щербеньское'
        result_file = 'reports/result/Щербеньское.xlsx'
    return field_name, result_file


if __name__ == '__main__':

    directory = 'D:\\for made\\Pycharm-projects\\Unstructured-field-data-aggregator\\reports\\pdfs'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print(get_fast_result(f))
