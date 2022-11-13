# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class GetHtmlParamFootnoteOutType(IntEnum):
    """ Тип вывода сносок при генерации HTML """
    ASHINT = 0
    """ Хинтом к звёздочке, саму сноску не отображать. """
    INBRACKETS = 1
    """ В скобках в месте вставки (...) """
    ENDOFUNIT = 2
    """ В конце ближайшего нумерованного раздела или главы UnitextDocblock
    (если структура документа выделена). """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)