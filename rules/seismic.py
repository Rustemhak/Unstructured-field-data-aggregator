from yargy import rule
from yargy.interpretation import fact, attribute
from yargy.pipelines import morph_pipeline

from yargy_utils.date_rules import DATE

# FIELD + date + пробурить + NUMR + скважина + , + оборот + NUMR + тип скважин
Year_seismic = fact(
    'Year_seismic',
    ['year_seismic']
)
Type_work = fact(
    'Type_work',
    ['type_work']
)
TYPE_WORK = morph_pipeline(['3D',
                            '2D', '2Д', '3Д']).interpretation(Type_work.type_work.inflected()).interpretation(Type_work)
SEISMIC_EXPLORATION = morph_pipeline(['сейморазведочные работы',
                                      'сейсморазведочные исследования',
                                      'сейсмоисследования'])
MOGT_WORD = rule('МОГТ')

YEAR_SEISMIC = DATE.interpretation(Year_seismic.year_seismic.inflected()).interpretation(Year_seismic)
SEISMIC = rule(YEAR_SEISMIC, MOGT_WORD, TYPE_WORK)
