from yargy import rule, or_, Parser
from yargy.pipelines import morph_pipeline

from yargy_utils import INT, COMMA, DOT, TOKENIZER, ID_TOKENIZER, show_json
from yargy_utils.skip_part_text import select_span_tokens

from yargy.interpretation import fact, attribute

Kvit = fact('Kvit', ['object_name_kvit', 'kvit_value'])


def get_kvit(text):
    """
    examples: Текст_отчета_2021_Том_1.docx, Глава 8.docx

    :param text: текст предложения из отчёта
    :return: Kvit objects
    """
    kvit_word_list = ['Квыт', 'коэффициент вытеснения']
    names_list = ['каширский', 'башкирский', 'верейский', 'бобриковский', 'ярус',
                  'горизонт', 'алексинский', 'тульский', 'турнейский',
                  'кыновско-пашийский', 'кыновский+пашийский', 'шешминский', 'кыновский']
    objects_list = ['ярус', 'горизонт']
    unit_list = ['доля', 'единица', 'ед.', 'д.', 'ед', 'д']
    kvit_tokens_list = kvit_word_list + names_list + objects_list + unit_list
    tokens = list(TOKENIZER(text))
    KVIT_TOKENS = morph_pipeline(kvit_tokens_list)
    DECIMAL = rule(INT,
                   or_(COMMA, DOT),
                   INT)
    parser = Parser(or_(rule(KVIT_TOKENS), DECIMAL), tokenizer=ID_TOKENIZER)
    matches = parser.findall(tokens)
    spans = [_.span for _ in matches]
    # print(spans)
    if matches:
        # вторым парсером возьму раздельные факты
        tokens = list(select_span_tokens(tokens, spans))
        # print([_.value for _ in tokens])
        KVIT_WORD = morph_pipeline(kvit_word_list)
        NAMES = morph_pipeline(names_list)
        OBJECTS = morph_pipeline(names_list)
        KVIT_TOKENS = rule(NAMES, OBJECTS.optional()).interpretation(Kvit.object_name_kvit.inflected())
        SHARE = morph_pipeline(['доля', 'д.', 'д'])
        UNITS = morph_pipeline(['единиц', 'ед.', 'ед'])
        UNITS_DICT = {
            'доля единица': 'д. ед.'
        }
        KVIT_VAL = rule(DECIMAL, SHARE, UNITS).repeatable().interpretation(Kvit.kvit_value)
        KVIT_OBJECT = rule(NAMES, OBJECTS.optional()).interpretation(Kvit.object_name_kvit.inflected())
        KVIT_OBJECT_VAL = rule(KVIT_OBJECT.optional(), KVIT_VAL).interpretation(Kvit)
        KVIT_FULL = rule(KVIT_WORD, KVIT_OBJECT_VAL.repeatable())
        parser_full = Parser(KVIT_FULL, tokenizer=ID_TOKENIZER)
        matches_full = list(parser_full.findall(tokens))
        if matches_full:
            parser_object = Parser(KVIT_OBJECT_VAL, tokenizer=ID_TOKENIZER)
            matches_object = list(parser_object.findall(tokens))
            if matches_object:
                for match in matches_object:
                    fact = match.fact
                    show_json(fact.as_json)
            return matches_object


"""
код для обработки случаев, когда в предыдущем предложении сама характеристика
а потом значение
kvit_find = False
for sent in chapter:
    text = sent.text
    tokens = list(TOKENIZER(text))
    KVIT_VAL = rule(DECIMAL, SHARE.optional(), UNITS.optional()).repeatable().interpretation(Kvit.kvit_value)
    parser_val = Parser(KVIT_WORD, tokenizer=ID_TOKENIZER)
    matches_val = list(parser_val.findall(tokens))
    if matches_val and kvit_find:
        ## заносим значение
        pass
    KVIT_WORD = morph_pipeline(kvit_word_list)
    parser_kvit = Parser(KVIT_WORD, tokenizer=ID_TOKENIZER)
    matches_kvit = list(parser_full.findall(tokens))
    if matches_kvit:
        kvit_find = True
    else:
        kvit_find = False
"""