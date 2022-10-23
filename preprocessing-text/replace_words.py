def replace_short_name(text: str, dict_short: dict) -> str:
    '''
    Заменяет сокращенные названия на полные названия
    :param text: исходный текст
    :param dict_short: словарь сокращений
    :return: обновленный текст
    '''
    for name in dict_short.keys():
        text = text.replace(name, dict_short[name])
    return text