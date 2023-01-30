import pdfplumber
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline
from yargy import rule, and_, Parser, or_
from yargy.predicates import is_capitalized, gte, lte
from collections import defaultdict
from read_report import read_pdf
from yargy_utils import NUMERO_SIGN, INT, show_json, ADJF, SLASH, COLON, TOKENIZER
from act_tables import process_tales
import pandas as pd

NAMES_FIELDS = ['Назначение скважины : до / после', 'Способ эксплуатации: до / после', 'Начало / оконч. ремонта:',
                'Название поля: Начало / оконч. ремонта', 'Месторождение', 'Площадь', 'Признак', 'Акт принят']
NEEDED_FIELDS = ['Назначение скважины : до / после', 'Способ эксплуатации: до / после', 'Начало / оконч. ремонта:',
                 'Название поля: Начало / оконч. ремонта', 'Месторождение', 'Площадь', 'Признак', 'Акт принят']


class Match(object):
    def __init__(self, fact, spans):
        self.fact = fact
        self.spans = spans


class Extractor(object):
    def __init__(self, MAIN_FIELD, OTHER_FIELDS=None):
        self.left_parser = Parser(MAIN_FIELD, tokenizer=TOKENIZER)
        self.right_parser = Parser(OTHER_FIELDS, tokenizer=TOKENIZER)

    def __call__(self, line):
        """
        Извлекает значение параметра между названиями полей
        :param line: строка, в кото
        :return: значение параметра
        """
        left_matches = self.left_parser.findall(line)
        left_spans = [_.span for _ in left_matches]
        right_matches = self.right_parser.findall(line)
        right_spans = [_.span for _ in right_matches]
        if left_spans and right_spans:
            return line[left_spans[0].stop:right_spans[0].start].strip()


def show_from_act(my_rule, lines):
    parser = Parser(my_rule)
    matches = list(parser.findall(lines))
    if matches:
        match = matches[0]
        fact = match.fact
        show_json(fact.as_json)


def get_field_value(my_rule, lines):
    parser = Parser(my_rule)
    matches = list(parser.findall(lines))
    if matches:
        match = matches[0]
        fact = match.fact
        return fact


def get_field_value_second(my_rule, lines):
    parser = Parser(my_rule)
    for line in lines:
        line = line.strip()
        match = list(parser.findall(line))
        if line is not None and len(line) and len(match):
            fact = match[0].fact
            fact.value = line.replace(fact.field_name, '').strip()
            print('fact', fact)
            return fact


# задавать самому путь
path = 'AKT_KRS_2850_АЗН_пример.PDF'
pdf = pdfplumber.open(path)
p0 = pdf.pages[0]
text_act = p0.extract_text(
    layout=True,
    use_text_flow=True
)

print(text_act)

lines = text_act.split('\n')

data_for_df1 = defaultdict(list)

"""
Название поля № Скважины
Значение: число
Примечание: универсально!
"""
WELL_WORD = morph_pipeline(['Скв'])
# NUMERO_SIGN
Well = fact(
    'Well',
    ['field_name', 'value']
)
WELL = rule(rule(WELL_WORD, NUMERO_SIGN).interpretation(Well.field_name),
            INT.interpretation(Well.value)).interpretation(Well)
show_from_act(WELL, text_act)
result = get_field_value(WELL, text_act)
data_for_df1[result.field_name].append(result.value)
#
"""
Название поля: Назначение скважины : до / после
Значение: идёт после названия поля
Примечание: Работает, если параметр в отдельной строчке

"""
Well_purpose = fact(
    'Well_purpose',
    ['field_name', 'value']
)
WELL_PURPOSE_WORDS = morph_pipeline(['Назначение скважины : до / после'])
# именное прилагательное
CAP_ADJF = rule(and_(ADJF,
                     is_capitalized()))
WELL_PURPOSE = rule(WELL_PURPOSE_WORDS.interpretation(Well_purpose.field_name)).interpretation(Well_purpose)
result = get_field_value_second(WELL_PURPOSE, lines)
data_for_df1[result.field_name].append(result.value)
# Способ эксплуатации: до / после
"""
Название поля: Способ эксплуатации: до / после
Значение: идёт после названия поля
Примечание: Работает, если параметр в отдельной строчке
"""
Method_operation = fact(
    'Method_operation',
    ['field_name', 'value']
)
METHOD_OPERATION_WORDS = morph_pipeline(['Способ эксплуатации: до / после'])
VALUE_METHOD_OPERATION = morph_pipeline(['Закачка по НКТ с пакером'])
METHOD_OPERATION = rule(METHOD_OPERATION_WORDS.interpretation(Method_operation.field_name)).interpretation(
    Method_operation)
result = get_field_value_second(METHOD_OPERATION, lines)
data_for_df1[result.field_name].append(result.value)

"""
Название поля: Начало / оконч. ремонта
Значение: дата / дата
Примечание: привязано к конкретному формату даты, умеет пропускать слово "месторождение"
"""
Repair = fact(
    'Repair',
    ['field_name', 'value']
)
REPAIR_WORD = morph_pipeline(['Начало / оконч. ремонта:'])
MONTH = and_(
    gte(1),
    lte(12)
)
DAY = and_(
    gte(1),
    lte(31)
)
YEAR = and_(
    gte(1900),
    lte(2100)
)
DATE = or_(
    rule(DAY, '/', MONTH, '/', YEAR),
).named('DATE')
FIELD_WORD = morph_pipeline(['месторождение'])
REPAIR = rule(REPAIR_WORD.interpretation(Repair.field_name), FIELD_WORD.optional(),
              rule(DATE, '/', DATE).interpretation(Repair.value)).interpretation(Repair)
show_from_act(REPAIR, text_act)
result = get_field_value(REPAIR, text_act)
data_for_df1[result.field_name].append(result.value)

"""
Название поля: Месторождение
Значение: название месторождения
Примечание: умеет пропускать слово "месторождение"
"""
#
Field = fact(
    'Field',
    ['field_name', 'value']
)
FIELD = rule(FIELD_WORD.interpretation(Field.field_name).optional(),
             COLON, CAP_ADJF.interpretation(Field.value)).interpretation(Field)
show_from_act(FIELD, text_act)
result = get_field_value(FIELD, text_act)
result.field_name = 'Месторождение'
data_for_df1[result.field_name].append(result.value)
# Площадь
"""
Название поля: площадь
Значение: объект (номер залежи либо название месторождения)
Примечание: Берет значение между парметрами
"""
Square = fact(
    'Square',
    ['field_name', 'value']
)
SQUARE_NAME = ['Площадь :']
SQUARE_WORD = morph_pipeline(SQUARE_NAME)
SIGN_NAME = ['Признак']
SIGN_WORD = morph_pipeline(SIGN_NAME)

extractor = Extractor(SQUARE_WORD, SIGN_WORD)
match = extractor(text_act)
if match:
    data_for_df1[SQUARE_NAME[0]].append(match)

# Признак
"""
Название поля: признак
Значение: ПНП
Примечание: Берет значение между парметрами
"""
Sign = fact(
    'Sign',
    ['field_name', 'value']
)

OTHER_FIELDS = morph_pipeline(['Акт принят'])
# result = get_field_value(SIGN, text_act)
# data_for_df1[result.field_name].append(result.value)
extractor = Extractor(SIGN_WORD, OTHER_FIELDS)
match = extractor(text_act)
if match:
    data_for_df1[SIGN_NAME[0]].append(match)

print(data_for_df1)
df1_7 = pd.DataFrame(data=data_for_df1)

# Из первой таблицы вытащить нужные колонки
# Вид работы
# Метод работы
# Причина ремонта
# Вся таблица Перфорация, отключение пластов
# Вся таблица Расход материала, используемые при ремонте

df8_10, df11_17, df_18_28 = process_tales(path)

combined_data = pd.concat([df1_7, df8_10, df11_17, df_18_28], axis=0)
combined_data.to_excel('Результат.xlsx')
print(combined_data)
