# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class ColorRef:
    
    def __init__(self) -> None:
        self.__isauto = False
        self.__r = 0
        self.__g = 0
        self.__b = 0
    
    @property
    def is_auto(self) -> bool:
        return self.__isauto
    @is_auto.setter
    def is_auto(self, value) -> bool:
        self.__isauto = value
        return self.__isauto
    
    @property
    def r(self) -> int:
        return self.__r
    @r.setter
    def r(self, value) -> int:
        self.__r = value
        return self.__r
    
    @property
    def g(self) -> int:
        return self.__g
    @g.setter
    def g(self, value) -> int:
        self.__g = value
        return self.__g
    
    @property
    def b(self) -> int:
        return self.__b
    @b.setter
    def b(self, value) -> int:
        self.__b = value
        return self.__b
    
    @staticmethod
    def _from_bytes(value : bytearray, offset : int) -> 'ColorRef':
        c = ColorRef()
        c.r = value[0]
        c.g = value[1]
        c.b = value[2]
        c.is_auto = value[3] != (0)
        return c