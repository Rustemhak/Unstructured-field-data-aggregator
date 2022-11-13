# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class PdfFontGlyph:
    
    def __init__(self) -> None:
        self.width = 0
        self.code = 0
        self.char0_ = '\x00'
        self.char2 = '\x00'
        self.undef_mnem = None;
    
    def __str__(self) -> str:
        return "{0} -> '{1}' (w={2})".format("{:04X}".format(self.code), ('?' if (ord(self.char0_)) == 0 else self.char0_), self.width)
    
    @staticmethod
    def _new193(_arg1 : float, _arg2 : int) -> 'PdfFontGlyph':
        res = PdfFontGlyph()
        res.width = _arg1
        res.code = _arg2
        return res
    
    @staticmethod
    def _new200(_arg1 : int) -> 'PdfFontGlyph':
        res = PdfFontGlyph()
        res.code = _arg1
        return res