# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.internal.pdf.PdfObject import PdfObject
from pullenti.util.MiscHelper import MiscHelper

class PdfRealValue(PdfObject):
    
    def __init__(self) -> None:
        super().__init__()
        self.val = None;
    
    def get_double(self) -> float:
        res = 0
        wrapres219 = RefOutArgWrapper(0)
        inoutres220 = MiscHelper.try_parse_double(self.val, wrapres219)
        res = wrapres219.value
        if (not inoutres220): 
            return 0
        return res
    
    def to_string_ex(self, lev : int) -> str:
        return self.val
    
    def is_simple(self, lev : int) -> bool:
        return True