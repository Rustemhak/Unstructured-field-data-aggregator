# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.word.FibRgCswNew import FibRgCswNew

class FibRgCswNew2000(FibRgCswNew):
    
    def __init__(self) -> None:
        super().__init__()
        self.__cquicksavesnew = 0
    
    @property
    def _cquick_saves_new(self) -> int:
        return self.__cquicksavesnew
    @_cquick_saves_new.setter
    def _cquick_saves_new(self, value) -> int:
        self.__cquicksavesnew = value
        return self.__cquicksavesnew