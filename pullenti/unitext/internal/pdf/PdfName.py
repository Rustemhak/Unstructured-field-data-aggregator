# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.pdf.PdfObject import PdfObject

class PdfName(PdfObject):
    
    def __init__(self) -> None:
        super().__init__()
        self.name = None;
        self._has_slash = False
    
    def to_string_ex(self, lev : int) -> str:
        return self.name
    
    def is_simple(self, lev : int) -> bool:
        return True