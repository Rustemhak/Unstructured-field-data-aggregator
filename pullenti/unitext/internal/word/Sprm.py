# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.internal.word.SinglePropertyModifiers import SinglePropertyModifiers

class Sprm:
    
    @property
    def _ispmd(self) -> int:
        return ((self._sprm) & 0x1FF)
    
    @property
    def _fspec(self) -> bool:
        return (((self._sprm) & 0x200)) != 0
    
    @property
    def _sgc(self) -> int:
        return ((((self._sprm) >> 10)) & 0x07)
    
    @property
    def _spra(self) -> int:
        return ((((self._sprm) >> 13)) & 0x07)
    
    def __init__(self, sprm : int=0) -> None:
        self._sprm = 0
        self._sprm = sprm
    
    def __str__(self) -> str:
        sprm_name = None
        wrapsprm_name491 = RefOutArgWrapper(None)
        inoutres492 = Utils.tryGetValue(SinglePropertyModifiers._map0_, self._sprm, wrapsprm_name491)
        sprm_name = wrapsprm_name491.value
        if (inoutres492): 
            return sprm_name
        else: 
            return "sprm: 0x" + "{:4X}".format(self._sprm)