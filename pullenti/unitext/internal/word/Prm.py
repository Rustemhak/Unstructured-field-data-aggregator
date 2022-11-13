# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class Prm:
    
    def __init__(self) -> None:
        self._prm = 0
    
    @property
    def _fcomplex(self) -> bool:
        return (((self._prm) & 1)) != 0
    
    @property
    def _isprm(self) -> int:
        return ((((self._prm) >> 1)) & 0x7F)
    
    @property
    def _val(self) -> int:
        return ((((self._prm) >> 8)) & 0xFF)
    
    @property
    def _igrpprl(self) -> int:
        return ((((self._prm) >> 1)) & 0x7FFF)