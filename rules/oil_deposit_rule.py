import xml.etree.ElementTree as ET

from yargy import Parser, or_, rule
from yargy.pipelines import morph_pipeline

from rules.objects_rule import horizons_names, stages_names
from yargy_utils import TOKENIZER, INT, ID_TOKENIZER, show_json
from yargy_utils.date_rules import DATE
from yargy_utils.skip_part_text import select_span_tokens


def oil_deposit__str__(oil_deposit):
    if oil_deposit.date is not None:
        return f'count = {oil_deposit.count} date = {oil_deposit.date}'
    else:
        return f'count = {oil_deposit.count}'


def object_oil_deposit__str__(oil_deposit):
    return f'name = {oil_deposit.object_name} count  = {oil_deposit.count}'


def set_tag_attr_oil_deposit(chapter: ET.SubElement) -> None:
    for sentence in chapter:
        text = sentence.text
        # закину сюда нужные словосочетания
        names = horizons_names + stages_names
        objects = ['месторождение', 'залежь', 'нефть']
        objects.extend(names)
        tokens = list(TOKENIZER(text))
        OIL_DEP = morph_pipeline(objects)
        parser = Parser(or_(rule(OIL_DEP), rule(INT), DATE), tokenizer=ID_TOKENIZER)
        matches = parser.findall(tokens)
        spans = [_.span for _ in matches]
        # print(spans)
        # вторым парсером возьму раздельные факты
        tokens = list(select_span_tokens(tokens, spans))
        # print([_.value for _ in tokens])

        OIL_DEPS = OIL_DEP.repeatable()
        parser = Parser(OIL_DEPS, tokenizer=ID_TOKENIZER)
        matches = parser.findall(tokens)

        from yargy.interpretation import fact, attribute

        Oil_deposit = fact('Oil_deposit', ['count', 'date'])
        OIL_DEP = morph_pipeline(['залежь'])
        OIL_NAME = morph_pipeline(['нефть'])
        FIELD_WORD = morph_pipeline(['месторождение'])
        OIL_DEP_INT = rule(DATE.optional().interpretation(Oil_deposit.date.inflected()), FIELD_WORD,
                           INT.interpretation(Oil_deposit.count.inflected()),
                           OIL_DEP, OIL_NAME).interpretation(Oil_deposit)
        parser1 = Parser(OIL_DEP_INT, tokenizer=ID_TOKENIZER)
        matches = list(parser1.findall(tokens))
        if matches:
            match = matches[0]
            for match in matches:
                fact = match.fact
                # show_json(fact.as_json)
                sentence.set('oil_deposit', eval('oil_deposit__str__')(fact))
            from yargy.interpretation import fact, attribute

            Oil_deposit = fact('Oil_deposit', ['object_name', 'count'])
            OIL_DEP = morph_pipeline(['залежь'])

            OBJECT_NAMES = morph_pipeline(names)
            OIL_DEP_INT = rule(OBJECT_NAMES.repeatable().interpretation(Oil_deposit.object_name.inflected()),
                               INT.interpretation(Oil_deposit.count.inflected()),
                               OIL_DEP.optional()).interpretation(Oil_deposit)
            parser1 = Parser(OIL_DEP_INT, tokenizer=ID_TOKENIZER)
            matches = list(parser1.findall(tokens))
            if matches:
                match = matches[0]
                for idx, match in enumerate(matches):
                    fact = match.fact
                    # show_json(fact.as_json)
                    sentence.set(f'object_oil_deposit_{idx}', eval('object_oil_deposit__str__')(fact))
