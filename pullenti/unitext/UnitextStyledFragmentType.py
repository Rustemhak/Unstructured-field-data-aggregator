# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class UnitextStyledFragmentType(IntEnum):
    """ Типы стилевых фрагментов UnitextStyledFragment
    Типы стилевых фрагментов
    """
    UNDEFINED = 0
    """ Не определён """
    INLINE = 1
    """ Линейный фрагмент (например, слово) """
    PARAGRAPH = 2
    """ Абзац (аналог параграфа MS Word) """
    TABLE = 3
    """ Таблица """
    TABLECELL = 4
    """ Ячейка таблицы """
    FOOTNOTE = 5
    """ Сноска """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)