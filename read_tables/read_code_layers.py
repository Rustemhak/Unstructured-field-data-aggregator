import re

import numpy as np
import pandas as pd


def merge_names(name_horizon):
    '''
    Функция для слияния названий горизонтов
    :param name_horizon: название горизонта из таблицы
    :return: название горизонта через дефис или без него
    '''
    if name_horizon is not np.NAN and '+' in name_horizon:
        cleaned_name = re.sub(r"\s+", "", name_horizon)
        n1, n2 = cleaned_name.split('+')
        return 'о-'.join([n1[:-2], n2])
    return name_horizon


def preproccess_df_code_layers(path_df: str) -> pd.DataFrame:
    '''
    Пайплайн предобработки таблицы коды пластов
    :param path_df: путь к таблице
    :return: подготовленный датафрейм
    '''
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
