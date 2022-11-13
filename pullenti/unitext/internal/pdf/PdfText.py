# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.pdf.PdfRect import PdfRect

class PdfText(PdfRect):
    
    def __init__(self) -> None:
        super().__init__()
        self.text = None;
        self.font_type3 = False
        self.font_size = 0
        self.space_width = 0
    
    def __str__(self) -> str:
        return "{0}: \"{1}\"".format(super().__str__(), Utils.ifNotNull(self.text, "?"))
    
    def merge_with(self, p : 'PdfText') -> None:
        self.text += p.text
        if (p.x1 < self.x1): 
            self.x1 = p.x1
        if (p.x2 > self.x2): 
            self.x2 = p.x2
        if (p.y1 < self.y1): 
            self.y1 = p.y1
        if (p.y2 > self.y2): 
            self.y2 = p.y2
    
    def can_be_merged_with(self, p : 'PdfText') -> bool:
        if (self.font_size != p.font_size): 
            return False
        d = p.x1 - self.x2
        if (d < -1): 
            if (p.x2 > self.x2 and p.x1 > self.x1): 
                pass
            else: 
                return False
        if (d > self.space_width): 
            return False
        if (d > (self.space_width / (2))): 
            wi = ((self.width + p.width)) / ((len(self.text) + len(p.text)))
            if (d > (wi / (3))): 
                return False
        if (p.font_type3 or self.font_type3): 
            return False
        if (self.y1 <= p.y1 and p.y2 <= self.y2): 
            return True
        if (p.y1 <= self.y1 and self.y2 <= p.y2): 
            return True
        if (p.text == " " or ((len(p.text) == 1 and (ord(p.text[0])) == 0xA0))): 
            if (self.y1 <= p.y1 and (p.y1 < self.y2)): 
                return True
        d = (self.y1 - p.y1)
        if (d < 0): 
            d = (- d)
        if (d >= 1): 
            if (p.y1 <= self.y1 and p.y2 >= self.y2): 
                pass
            return False
        d = (self.y2 - p.y2)
        if (d < 0): 
            d = (- d)
        if (d >= 1): 
            return False
        return True