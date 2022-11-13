# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class UnitextPlaintextType(IntEnum):
    """ Тип плоского текста """
    SIMPLE = 0
    """ Обычный текст """
    SUP = 1
    """ Верхний индекс """
    SUB = 2
    """ Нижний индекс """
    GENERATED = 3
    """ Текст сгенерирован (на основе автонумерации, например) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)