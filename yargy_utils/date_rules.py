# правило для даты
from yargy import and_, or_, rule
from yargy.predicates import normalized
from yargy.predicates import (
    lte,
    gte,
    dictionary
)

MONTHS = {
    'январь',
    'февраль',
    'март',
    'апрель',
    'мая',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь'
}

MONTH_NAME = dictionary(MONTHS)
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
    rule(DAY, MONTH_NAME, YEAR),
    rule(DAY, '.', MONTH, '.', YEAR, 'г', '.'),
    rule(MONTH_NAME, YEAR),
    rule(YEAR, or_(rule('г', '.'), rule(normalized('год'))))
).named('DATE')
