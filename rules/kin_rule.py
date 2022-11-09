from yargy import rule, or_, Parser
from yargy.interpretation import fact, attribute
from yargy.pipelines import morph_pipeline

from yargy_utils import INT, COMMA, DOT, TOKENIZER, ID_TOKENIZER, show_json
from yargy_utils.skip_part_text import select_span_tokens

Kin = fact('Kin', ['object_name_kin', 'kin_value'])


def get_KIN(text):
    """
    Важно: берём первые значения встретившие КИНа  для каждого объекта
    :param text:
    :return: Kin
    """
    kin_type_list = ['принятые для подсчета', 'утвержденный']
    kin_word_list = ['КИН', 'коэффициент извлечения нефти']
    names_list = ['каширский', 'башкирский', 'верейский', 'бобриковский', 'ярус',
                  'горизонт', 'алексинский', 'тульский', 'турнейский',
                  'кыновско-пашийский', 'кыновский+пашийский', 'шешминский']
    objects_list = ['ярус', 'горизонт']
    unit_list = ['доля', 'единица', 'ед.']
    kin_tokens_list = kin_type_list + kin_word_list + objects_list + \
                      names_list + unit_list
    tokens = list(TOKENIZER(text))
    KIN_TOKENS = morph_pipeline(kin_tokens_list)
    DECIMAL = rule(INT,
                   or_(COMMA, DOT),
                   INT)
    parser = Parser(or_(rule(KIN_TOKENS), DECIMAL), tokenizer=ID_TOKENIZER)
    matches = parser.findall(tokens)
    spans = [_.span for _ in matches]
    # print(spans)
    if matches:
        # вторым парсером возьму раздельные факты
        tokens = list(select_span_tokens(tokens, spans))
        # print([_.value for _ in tokens])
        KIN_WORD = morph_pipeline(kin_word_list)
        KIN_TYPE = morph_pipeline(kin_type_list)
        KIN_COMMON = rule(KIN_TYPE, KIN_WORD)
        NAMES = morph_pipeline(names_list)
        OBJECTS = morph_pipeline(names_list)
        KIN_OBJECT = rule(NAMES, OBJECTS.optional()).interpretation(Kin.object_name_kin.inflected())
        SHARE = morph_pipeline(['доля'])
        UNITS = morph_pipeline(['единиц', 'ед.'])
        UNITS_DICT = {
            'доля единица': 'д. ед.'
        }
        KIN_VAL = rule(DECIMAL, SHARE, UNITS).repeatable().interpretation(Kin.kin_value)
        KIN_OBJECT_VAL = rule(KIN_OBJECT, KIN_VAL).interpretation(Kin)
        KIN_FULL = rule(KIN_COMMON, KIN_OBJECT_VAL.repeatable())
        parser_full = Parser(KIN_FULL, tokenizer=ID_TOKENIZER)
        matches_full = list(parser_full.findall(tokens))
        if matches_full:
            parser_object = Parser(KIN_OBJECT_VAL, tokenizer=ID_TOKENIZER)
            matches_object = list(parser_object.findall(tokens))
            if matches_object:
                for match in matches_object:
                    fact = match.fact
                    show_json(fact.as_json)
            return matches_object
