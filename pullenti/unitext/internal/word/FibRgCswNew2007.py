# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.word.FibRgCswNew2000 import FibRgCswNew2000

class FibRgCswNew2007(FibRgCswNew2000):
    
    def __init__(self) -> None:
        super().__init__()
        self.__lidthemeother = 0
        self.__lidthemefe = 0
        self.__lidthemecs = 0
    
    @property
    def _lid_theme_other(self) -> int:
        return self.__lidthemeother
    @_lid_theme_other.setter
    def _lid_theme_other(self, value) -> int:
        self.__lidthemeother = value
        return self.__lidthemeother
    
    @property
    def _lid_themefe(self) -> int:
        return self.__lidthemefe
    @_lid_themefe.setter
    def _lid_themefe(self, value) -> int:
        self.__lidthemefe = value
        return self.__lidthemefe
    
    @property
    def _lid_themecs(self) -> int:
        return self.__lidthemecs
    @_lid_themecs.setter
    def _lid_themecs(self, value) -> int:
        self.__lidthemecs = value
        return self.__lidthemecs