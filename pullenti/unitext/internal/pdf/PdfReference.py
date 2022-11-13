# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.pdf.PdfObject import PdfObject

class PdfReference(PdfObject):
    
    def to_string_ex(self, lev : int) -> str:
        return "[R 0 {0}]".format(self.id0_)