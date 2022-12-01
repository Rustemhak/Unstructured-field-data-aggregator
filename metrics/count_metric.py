def precision(list_true: list[str], list_pred: list[str]):
    """
    :param list_true: список данных с правильными результатами
    :param list_pred: список данных с полученными результатами
    :return: точность алгоритма
    """
    tp = 0
    fp = 0
    for pred in list_pred:
        if pred in list_true:
            tp += 1
        else:
            fp += 1
    return tp / (tp - fp)
