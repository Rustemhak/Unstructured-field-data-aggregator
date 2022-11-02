import pandas as pd
import pdfplumber


def clear_enter(text: str) -> str:
    """
    Очищает текст от символов переноса строки и соединяет слова, если присутсвует знак переноса
    :param text: сырой текст
    :return: обработанный и "чистый" текст
    """
    if text is None:
        return text
    # отдельно убирает знаки переноса
    text = text.replace('-\n', '')
    text = text.replace('\n', '')
    return text


def read_table_res_test_short(path, id_page: int, preproccess: bool = True) -> pd.DataFrame:
    """
    Возвращает (предобратанную) таблицу из pdf в формате датафрейма пандаса
    :param path: путь к pdf-документу
    :param id_page: номер страницы, в которой содержится таблица
    :param preproccess: выполнять ли предобработку в таблице
    :return: датафрейм в пандасе
    """
    table_settings = {
        "text_y_tolerance": 6
    }
    # id_page -= 1
    with pdfplumber.open(path) as pdf:
        if len(pdf.pages):
            table = pdf.pages[id_page].extract_tables(table_settings)
    # print(table)
    table = table[0]
    if preproccess:
        table = list(map(lambda x: list(map(lambda y: clear_enter(y), x)), table))
    df = pd.DataFrame(table)
    df.columns = list(df.iloc[0])[:2] + list(df.iloc[1])[2:]
    df.drop(df.index[:2], inplace=True, axis=0)
    df.reset_index(inplace=True, drop=True)
    return df.replace('-', 0)
