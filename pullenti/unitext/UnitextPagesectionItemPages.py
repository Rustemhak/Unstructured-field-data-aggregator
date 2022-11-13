# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class UnitextPagesectionItemPages(IntEnum):
    """ Страницы, на которые распространяется элемент сегмента """
    DEFAULT = 0
    """ Дефолтовая (если другие не применились) """
    FIRST = 1
    """ Для первой страницы """
    EVEN = 2
    """ Для чётных страниц """
    ODD = 3
    """ Для нечётных страниц """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)