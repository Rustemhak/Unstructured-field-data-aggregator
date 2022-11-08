from os.path import join

from yargy import rule, or_, Parser
from yargy.interpretation import fact, attribute
from yargy.pipelines import morph_pipeline

from yargy_utils import INT, COMMA, DOT, TOKENIZER, ID_TOKENIZER, show_json
from yargy_utils.skip_part_text import select_span_tokens

Oil_sat = fact(
    'Oil_sat',
    ['oil_sat_value', 'object_name', 'num_def']
)


class Oil_sat(Oil_sat):
    def __str__(self):
        if self.object_name and self.num_def:
            return self.object_name + ' ' + self.num_def + ' ' + self.oil_sat_value
        elif self.object_name:
            return self.object_name + ' ' + self.oil_sat_value
        elif self.num_def:
            return self.num_def + ' ' + self.oil_sat_value
        else:
            return self.oil_sat_value


def get_oil_sat(text):
    objects = [
        'ярус',
        'горизонт'
    ]
    names = ['каширский', 'башкирский', 'верейский', 'бобриковский',
             'алексинский', 'тульский', 'турнейский', 'кыновско-пашийский', 'шешминский']
    # print(text)
    # FIELD + date + пробурить + NUMR + скважина + , + оборот + NUMR + тип скважи
    # среднее
    avg_list = ['средний', 'средневзвешенный', 'в среднем']
    # гис
    gis_list = ['ГИС', 'геофизические исследования', 'геофизические исследования']
    # пористость
    oil_sat_list = ['нефтенасыщенность', 'Кн']
    # значение
    value_list = ['значение']
    # коэфициент
    coef = ['коэффициент']
    # единица измерения
    unit_list = ['%', 'доли ед.', 'д. ед.']
    # составляет
    is_list = ['составлять', 'составить']
    # определение
    definition_list = ['определение', 'образец', 'пластопересечение', 'скважина']
    DECIMAL = rule(INT,
                   or_(COMMA, DOT),
                   INT)

    # ДОБАВИТЬ КЛЮЧЕВЫЕ СЛОВА ДЛЯ ПОРИСТОСТИ
    tokens = list(TOKENIZER(text))
    # IS = morph_pipeline(is_list)
    oil_sat_tokens = avg_list + gis_list + oil_sat_list + \
                     value_list + objects + names + coef  # + definition_list + unit_list
    DEF = morph_pipeline(definition_list)
    UNIT = morph_pipeline(unit_list)
    POROSITY_TOKENS = morph_pipeline(oil_sat_tokens)
    parser = Parser(or_(POROSITY_TOKENS, rule(DECIMAL, UNIT), rule(INT, DEF)), tokenizer=ID_TOKENIZER)
    matches = parser.findall(tokens)
    spans = [_.span for _ in matches]
    if matches:
        # вторым парсером возьму раздельные факты
        tokens = list(select_span_tokens(tokens, spans))
        # print([_.value for _ in tokens])

        # пример из кол-ва залежей (см.)
        OBJECTS = morph_pipeline(objects)
        # пример из кол-ва залежей (см.)
        NAMES = morph_pipeline(names)
        AVG = morph_pipeline(avg_list)
        VAL = morph_pipeline(value_list)
        OIL_SAT_WORD = morph_pipeline(oil_sat_list)
        GIS = morph_pipeline(gis_list)
        UNIT = morph_pipeline(unit_list)
        COEFF = morph_pipeline(coef)
        UNIT = morph_pipeline(unit_list)
        DEF = morph_pipeline(definition_list)

        NUM_DEF = rule(INT.interpretation(Oil_sat.num_def.inflected()), DEF).optional()

        OBJECT_NAME = rule(NAMES, OBJECTS) \
            .optional() \
            .interpretation(Oil_sat.object_name.inflected())
        POR_VAL = rule(DECIMAL.interpretation(Oil_sat.oil_sat_value.inflected()), UNIT)
        # PERCENT_VAL = rule(DECIMAL, PERCENT)
        OPTS = rule(NUM_DEF, OBJECT_NAME, NUM_DEF)

        GIS_SAT_AVG_VAL = rule(  # OPTS,
            GIS,
            # OPTS,
            VAL.optional(),
            # OPTS,
            COEFF.optional(),
            # OPTS,
            OIL_SAT_WORD,
            # OPTS,
            AVG,
            # OPTS,
            POR_VAL) \
            .interpretation(Oil_sat)
        AVG_SAT_VAL = rule(OPTS.optional(),
                           AVG,
                           OPTS.optional(),
                           VAL.optional(),
                           COEFF.optional(),
                           OPTS.optional(),
                           OIL_SAT_WORD,
                           GIS.optional(),
                           rule(INT.interpretation(Oil_sat.num_def.inflected()), DEF).optional(),
                           rule(INT, DEF).optional(),
                           rule(NAMES, OBJECTS) \
                           .optional() \
                           .interpretation(Oil_sat.object_name.inflected()),
                           # IS,
                           POR_VAL,
                           rule(INT.interpretation(Oil_sat.num_def.inflected()), DEF).optional(),
                           rule(INT, DEF).optional(), ) \
            .interpretation(Oil_sat)
        SAT_AVG_VAL = rule(
            rule(NAMES, OBJECTS) \
                .optional() \
                .interpretation(Oil_sat.object_name.inflected()),
            VAL.optional(),
            COEFF.optional(),
            OPTS.optional(),
            OIL_SAT_WORD,
            GIS.optional(),
            rule(INT.interpretation(Oil_sat.num_def.inflected()), DEF).optional(),
            rule(INT, DEF).optional(),
            rule(NAMES, OBJECTS) \
                .optional() \
                .interpretation(Oil_sat.object_name.inflected()),
            GIS.optional(),
            rule(DECIMAL, UNIT).optional().repeatable(),
            AVG,
            POR_VAL,
            rule(INT.interpretation(Oil_sat.num_def.inflected()), DEF).optional(),
            rule(INT, DEF).optional(), ) \
            .interpretation(Oil_sat)
        # POROSITY_VAL_GIS = or_(AVG_POR_GIS_VAL, GIS_POR_AVG_VAL, AVG_POR_VAL)

        parser1 = Parser(AVG_SAT_VAL, tokenizer=ID_TOKENIZER)
        matches1 = list(parser1.findall(tokens))

        parser2 = Parser(SAT_AVG_VAL, tokenizer=ID_TOKENIZER)
        matches2 = list(parser2.findall(tokens))

        parser3 = Parser(GIS_SAT_AVG_VAL, tokenizer=ID_TOKENIZER)
        matches3 = list(parser3.findall(tokens))
        if matches1:
            match = matches1[0]
            # print(f'\nmatches1, len = {len(matches1)}\n')
            # for match in matches1:
            #     print('1pars', match)
            #     fact = match.fact
            #     show_json(fact.as_json)
            return matches1
        elif matches2:
            match = matches2[0]
            # print(f'\nmatches2, len = {len(matches2)}\n')
            # for match in matches2:
            #     print('2pars', match)
            #     fact = match.fact
            #     show_json(fact.as_json)
            return matches2
        elif matches3:
            match = matches3[0]
            # print(f'\nmatches3, len = {len(matches3)}\n')
            # for match in matches3:
            #     print('3pars', match)
            #     fact = match.fact
            #     show_json(fact.as_json)
            return matches3
        # отдельно ГИС
        # elif False:
        #     pass


if __name__ == '__main__':
    path_to_upd_txt = join('..', 'reports', 'txt', 'archangelsk', 'upd')
    paths_to_upd_txt = [join(path_to_upd_txt, f'{i}upd.txt') for i in range(14)]
    for path in paths_to_upd_txt:
        print(path)
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
        get_oil_sat(text)
