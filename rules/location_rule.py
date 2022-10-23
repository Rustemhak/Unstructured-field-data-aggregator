from yargy import rule, and_
from yargy.pipelines import morph_pipeline
from yargy.predicates import gram, is_capitalized

from yargy_utils import gnc


def location__str__(loc):
    return loc.name

from yargy.interpretation import fact, attribute

LOC_VERBS = morph_pipeline([
    'находиться',
    'расположить',
    'располагаться'
])
Loc =  fact('Loc',['name'])
PREP = gram('PREP')
# сущиствительное
NOUN = gram('NOUN')
# прилагательное
ADJF = gram('ADJF')
CAP_NOUN = rule(and_(NOUN,
                     is_capitalized()))
NAME_LOC = rule(ADJF.optional().match(gnc),
                NOUN.optional().match(gnc),
                NOUN,
                ADJF.optional(),
                NOUN.optional(),
                CAP_NOUN.optional().repeatable())
LOC = rule(LOC_VERBS, PREP, NAME_LOC.interpretation(Loc.name.inflected())).interpretation(Loc)