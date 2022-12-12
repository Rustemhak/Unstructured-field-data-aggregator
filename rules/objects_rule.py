import os.path
import re

import numpy as np
import pandas as pd
from yargy import rule, Parser
from yargy.pipelines import morph_pipeline

from yargy_utils import TOKENIZER, show_json


def merge_names(name_horizon):
    """
    Функция для слияния названий горизонтов
    :param name_horizon: название горизонта из таблицы
    :return: название горизонта через дефис или без него
    """
    if name_horizon is not np.NAN and '+' in name_horizon:
        cleaned_name = re.sub(r"\s+", "", name_horizon)
        n1, n2 = cleaned_name.split('+')
        return 'о-'.join([n1[:-2], n2])
    return name_horizon


def preproccess_df_code_layers(path_df: str) -> pd.DataFrame:
    """
    Пайплайн предобработки таблицы коды пластов
    :param path_df: путь к таблице
    :return: подготовленный датафрейм
    """
    df = pd.read_excel(path_df)
    df['indexes'] = [set() for _ in range(df.shape[0])]
    first_column = df.pop('indexes')
    # insert column using insert(position,column_name,first_column) function
    df.insert(0, 'indexes', first_column)
    df['stratigraphic_index'] = df['stratigraphic_index'].apply(lambda x: x.replace(' ', ''))
    df['horizon'] = df['horizon'].apply(lambda x: merge_names(x))
    return df


def cut_name(name):
    return re.sub(r' \(\w+\)', '', name)


def create_dict_strat_obj(obj_pd: pd.DataFrame, name_object: str) -> tuple:
    """
    Формирует список объектов сущности(добавляется множество номеров строк) и уникальных названий
    :param obj_pd: датафрейм
    :param name_object: название сущности
    :return: множество объектов и множество уникальных названий сущности
    """
    objects_set = []
    object_names = []
    for row in obj_pd.loc[:, : name_object].itertuples():
        cur_name_object = getattr(row, name_object)
        if cur_name_object is not np.NAN:
            cur_name_object = cut_name(cur_name_object)
            if cur_name_object not in object_names:
                row.indexes.add(row.Index)
                objects_set.append(row)
                object_names.append(cur_name_object)
            else:
                # случай если название уже встречалось
                objects_set[-1].indexes.add(row.Index)
    return objects_set, object_names


if os.path.exists("../reports/xlsx/Layers_codes.xlsx"):
    path_xlsx = "../reports/xlsx/Layers_codes.xlsx"
elif os.path.exists("reports/xlsx/Layers_codes.xlsx"):
    path_xlsx = "reports/xlsx/Layers_codes.xlsx"
else:
    raise FileNotFoundError(
        "No such file or directory: '../reports/xlsx/Layers_codes.xlsx' or 'reports/xlsx/Layers_codes.xlsx'"
    )

df_code_layers = pd.read_excel(path_xlsx)
df_copy1 = preproccess_df_code_layers(path_xlsx)
df_copy2 = preproccess_df_code_layers(path_xlsx)
df_copy3 = preproccess_df_code_layers(path_xlsx)
horizons_set, horizons_names = create_dict_strat_obj(df_copy1, 'horizon')
stages_set, stages_names = create_dict_strat_obj(df_copy2, 'stage')

from yargy.interpretation import fact, attribute
from yargy.predicates import normalized

Horizon_object = fact('Horizon_object', ['name'])
HORIZON_WORD = rule(normalized('горизонт'))
HORIZON_NAMES = morph_pipeline(horizons_names)
HORIZON = rule(HORIZON_NAMES.interpretation(Horizon_object.name.inflected()), HORIZON_WORD).interpretation(
    Horizon_object)


def horizon_object__str__(horizon_object):
    return horizon_object.name


from yargy.interpretation import fact, attribute

Stage_object = fact('Stage_object', ['name'])
STAGE_WORD = rule(normalized('ярус'))
STAGE_NAMES = morph_pipeline(stages_names)
STAGE = rule(STAGE_NAMES.interpretation(Stage_object.name.inflected()), STAGE_WORD).interpretation(Stage_object)


def stage_object__str__(stage_object):
    return stage_object.name


def set_horizon_object(chapter):
    for sentence in chapter:
        text = sentence.text
        parser = Parser(HORIZON, tokenizer=TOKENIZER)
        matches = list(parser.findall(text))
        if matches:
            match = matches[0]
            for idx, match in enumerate(matches):
                fact = match.fact
                show_json(fact.as_json)
                sentence.set(f'horizon_object{idx}', eval('horizon_object__str__')(fact))


def set_stage_object(chapter):
    for sentence in chapter:
        text = sentence.text
        parser = Parser(STAGE, tokenizer=TOKENIZER)
        matches = list(parser.findall(text))
        if matches:
            match = matches[0]
            for idx, match in enumerate(matches):
                fact = match.fact
                show_json(fact.as_json)
                sentence.set(f'stage_object{idx}', eval('stage_object__str__')(fact))
