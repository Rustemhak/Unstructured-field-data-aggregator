# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class UnitextMiscType(IntEnum):
    """ Тип нетекстового элемента """
    UNDEFINED = 0
    """ Не определено """
    HORIZONTALLINE = 1
    """ Горизонтальная линия """
    ANCHOR = 2
    """ Якорь, на который ссылаются из Hyperlink с IsInternal = true (Href равен Id).
    Оптимизатор удаляет по возможности якоря и переадресует ссылки на Id реальных элементов,
    но если вдруг не получилось, то якорь остаётся... """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)