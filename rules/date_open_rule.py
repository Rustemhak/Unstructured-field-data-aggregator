from yargy import rule
from yargy.interpretation import fact, attribute
from yargy.pipelines import morph_pipeline
from yargy.predicates import gram

from yargy_utils.date_rules import DATE

OPEN_VERBS = morph_pipeline([
    'открыть'
])
Open = fact('Open', ['date'])
# предлог
PREP = gram('PREP')
# сущиствительное
NOUN = gram('NOUN')
# прилагательное
ADJF = gram('ADJF')

OPEN_DATE = rule(OPEN_VERBS,
                 PREP,
                 DATE
                 .interpretation(Open.date.inflected())).interpretation(Open)


def open_date__str__(open_date):
    return open_date.date
