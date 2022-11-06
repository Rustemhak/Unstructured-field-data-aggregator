def replace_short_name(text: str, dict_short: dict) -> str:
    """
    Заменяет сокращенные названия на полные названия
    :param text: исходный текст
    :param dict_short: словарь сокращений
    :return: обновленный текст
    """
    for k, v in dict_short.items():
        text = text.replace(k, v)
    return text


STAND_GEO_SHORT_NAMES = {'скв.': 'скважина', 'мест.': 'месторождение', 'ед.': 'единиц'}
