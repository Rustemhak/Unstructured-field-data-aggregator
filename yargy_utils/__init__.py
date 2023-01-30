from .id_tokenizer import *
from .show_result import *
from .word_to_number import *
from yargy import (
    Parser,
    or_, rule,
    and_
)
from yargy import rule, or_
from yargy.pipelines import morph_pipeline, caseless_pipeline
from yargy.interpretation import fact, const
from yargy.predicates import eq, caseless, normalized, type, length_eq
from yargy.pipelines import morph_pipeline
from yargy.predicates import (
    eq, in_, dictionary,
    type, gram, is_capitalized, normalized
)
from yargy.tokenizer import MorphTokenizer, EOL
from yargy import interpretation as interp
from yargy.interpretation import fact, attribute
from yargy.relations import gnc_relation
from yargy.record import Record
# from number import NUMBER
from yargy.parser import Match

number_extractor = NumberExtractor()
# для согласования слов
gnc = gnc_relation()
# сущиствительное
NOUN = gram('NOUN')
# прилагательное
ADJF = gram('ADJF')
# предлог
PREP = gram('PREP')
# союз
CONJ = gram('CONJ')
# запятая
COMMA = eq(',')
# число
INT = type('INT')
# разделитель в виде союза или знака препинания
SEPARATOR = or_(COMMA, CONJ)
# точка
DOT = eq('.')
# числительное
NUMR = gram('NUMR')
PERCENT = eq('%')
NUMERO_SIGN = eq('№')
SLASH = eq('/')
DECIMAL = rule(INT,
               or_(COMMA, DOT),
               INT)
COLON = eq(':')
# любой токен (не работает)
POST = gram('POST')
# аббревиатура
ABBR = and_(
    length_eq(3),
    is_capitalized()
)
# токенайзер
TOKENIZER = MorphTokenizer().remove_types(EOL)
#IdTokenizer
ID_TOKENIZER = IdTokenizer(TOKENIZER)
