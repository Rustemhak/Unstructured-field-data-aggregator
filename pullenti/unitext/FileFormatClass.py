# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class FileFormatClass(IntEnum):
    """ Класс формата """
    UNDEFINED = 0
    """ Неопределён """
    ARCHIVE = 1
    """ Архивы (zip, rar ...) """
    IMAGE = 2
    """ Картинки """
    OFFICE = 3
    """ Документы MS Office и Open Office """
    PAGELAYOUT = 4
    """ Тексто-графические (PDF, DjVu) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)