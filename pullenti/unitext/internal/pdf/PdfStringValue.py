# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.pdf.PdfObject import PdfObject
from pullenti.util.MiscHelper import MiscHelper

class PdfStringValue(PdfObject):
    
    def __init__(self) -> None:
        super().__init__()
        self.is_hex = False
        self.val = None;
    
    def to_string_ex(self, lev : int) -> str:
        str0_ = PdfStringValue.get_string_by_bytes(self.val)
        if (len(str0_) > 100): 
            str0_ = (str0_[0:0+100] + "...")
        return "\"{0}\"".format(str0_)
    
    def is_simple(self, lev : int) -> bool:
        return True
    
    @staticmethod
    def get_string_by_bytes(buf : bytearray) -> str:
        if (buf is None): 
            return None
        if (len(buf) > 2 and buf[0] == (0xFF) and buf[1] == (0xFE)): 
            return MiscHelper.decode_string_unicode(buf, 2, len(buf) - 2)
        if (len(buf) > 2 and buf[0] == (0xFE) and buf[1] == (0xFF)): 
            return MiscHelper.decode_string_unicodebe(buf, 2, len(buf) - 2)
        return MiscHelper.decode_string_ascii(buf, 0, -1)