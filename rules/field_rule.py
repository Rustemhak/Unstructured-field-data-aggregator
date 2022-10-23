from yargy import rule, and_
from yargy.interpretation import fact, attribute
from yargy.predicates import normalized
from yargy.predicates import is_capitalized

from yargy_utils import ADJF, gnc

# создание объекта "месторождение"
Field = fact(
    'Field',
    ['first', 'last']
)

# слово месторождение
NAME = rule(normalized('месторождение'))
# именное прилагательное
CAP_ADJF = rule(and_(ADJF,
                     is_capitalized()))
OIL = rule(normalized('нефть'))
# создание правила для месторождения
FIELD = rule(CAP_ADJF.interpretation(Field.first.inflected()).match(gnc),
             ADJF.optional().repeatable().match(gnc),
             NAME.interpretation(Field.last.inflected()).match(gnc),
             OIL.optional()).interpretation(Field)
