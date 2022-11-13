# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.word.FtsWidthType import FtsWidthType

class FtsWidth:
    
    def __init__(self) -> None:
        self.__typ = FtsWidthType.NONE
        self.__value = 0
    
    @property
    def typ(self) -> 'FtsWidthType':
        return self.__typ
    @typ.setter
    def typ(self, value_) -> 'FtsWidthType':
        self.__typ = value_
        return self.__typ
    
    @property
    def value(self) -> float:
        return self.__value
    @value.setter
    def value(self, value_) -> float:
        self.__value = value_
        return self.__value
    
    @staticmethod
    def _from_bytes(value_ : bytearray, offset : int) -> 'FtsWidth':
        raise NotImplementedError()