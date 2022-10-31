import re

import numpy as np
import pandas as pd


def cut_name(name):
    return re.sub(r' \(\w+\)', '', name)


def create_dict_strat_obj(obj_pd: pd.DataFrame, name_object: str) -> tuple:
    '''
    Формирует список объектов сущности(добавляется множество номеров строк) и уникальных названий
    :param obj_pd: датафрейм
    :param name_object: название сущности
    :return: множество объектов и множество уникальных названий сущности
    '''
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
