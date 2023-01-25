from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline
from yargy import rule, and_, Parser, or_
from yargy.predicates import is_capitalized, gte, lte

from read_report import read_pdf
from yargy_utils import NUMERO_SIGN, INT, show_json, ADJF, SLASH, COLON
from act_tables import process_tales


def show_from_act(my_rule, lines):
    parser = Parser(my_rule)
    matches = list(parser.findall(lines))
    if matches:
        match = matches[0]
        fact = match.fact
        show_json(fact.as_json)


path = 'AKT_KRS_2850_АЗН_пример.PDF'
text_act = read_pdf(path, 1, 1)

#print(text_act)

"""
Название поля № Скважины
Значение: число
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
#
"""
Название поля: Назначение скважины : до / после
Значение: прилагательное (собственное или нарицательное?)
"""
Well_purpose = fact(
    'Well_purpose',
    ['field_name', 'value']
)
WELL_PURPOSE_WORDS = morph_pipeline(['Назначение скважины : до / после'])
# именное прилагательное
CAP_ADJF = rule(and_(ADJF,
                     is_capitalized()))
WELL_PURPOSE = rule(WELL_PURPOSE_WORDS.interpretation(Well_purpose.field_name)
                    , rule(CAP_ADJF, SLASH, CAP_ADJF).interpretation(Well_purpose.value)).interpretation(Well_purpose)
show_from_act(WELL_PURPOSE, text_act)
# Способ эксплуатации: до / после
"""
Название поля: Способ эксплуатации: до / после
Значение: Закачка по НКТ с пакером / Закачка по НКТ с пакером (какие ещё могут быть?)
"""
Method_operation = fact(
    'Method_operation',
    ['field_name', 'value']
)
METHOD_OPERATION_WORDS = morph_pipeline(['Способ эксплуатации: до / после'])
VALUE_METHOD_OPERATION = morph_pipeline(['Закачка по НКТ с пакером'])
METHOD_OPERATION = rule(METHOD_OPERATION_WORDS.interpretation(Method_operation.field_name)
                        , rule(VALUE_METHOD_OPERATION, SLASH, VALUE_METHOD_OPERATION)
                        .interpretation(Method_operation.value)).interpretation(Method_operation)
show_from_act(METHOD_OPERATION, text_act)

"""
Название поля: Начало / оконч. ремонта
Значение: дата / дата
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

REPAIR = rule(REPAIR_WORD.interpretation(Repair.field_name),
              rule(DATE, '/', DATE).interpretation(Repair.value)).interpretation(Repair)
show_from_act(REPAIR, text_act)

"""
Название поля: Месторождение
Значение: название месторождения
"""
#
Field = fact(
    'Field',
    ['field_name', 'value']
)
FIELD_WORD = morph_pipeline(['месторождение'])
FIELD = rule(FIELD_WORD.interpretation(Field.field_name),
             COLON, CAP_ADJF.interpretation(Field.value)).interpretation(Field)
show_from_act(FIELD, text_act)
# Площадь
"""
Название поля: площадь
Значение: объект (номер залежи либо название месторождения)
"""
Square = fact(
    'Square',
    ['field_name', 'value']
)
SQUARE_WORD = morph_pipeline(['площадь'])
DEPOSIT = morph_pipeline(['залежь'])
SQUARE_VALUE = or_(CAP_ADJF, rule(DEPOSIT, NUMERO_SIGN, INT))
SQUARE = rule(SQUARE_WORD.interpretation(Square.field_name),
              COLON, SQUARE_VALUE.interpretation(Square.value)).interpretation(Square)
show_from_act(SQUARE, text_act)
# Признак
"""
Название поля: признак
Значение: ПНП
"""
Sign = fact(
    'Sign',
    ['field_name', 'value']
)
SIGN_WORD = morph_pipeline(['признак'])
SIGN_VALUE = morph_pipeline(['ПНП'])
SIGN = rule(SIGN_WORD.interpretation(Sign.field_name),
            SIGN_VALUE.interpretation(Sign.value)).interpretation(Sign)
show_from_act(SIGN, text_act)

# Из первой таблицы вытащить нужные колонки
# Вид работы
# Метод работы
# Причина ремонта

process_tales(path)
# Вся таблица Перфорация, отключение пластов

# Расход материала, используемые при ремонте
