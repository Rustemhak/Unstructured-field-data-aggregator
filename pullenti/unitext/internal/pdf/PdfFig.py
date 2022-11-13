# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.pdf.PdfRect import PdfRect

class PdfFig(PdfRect):
    
    def __str__(self) -> str:
        return "lines [x1={0}, x2={1}, y1={2}, y2={3}]".format(self.x1, self.x2, self.y1, self.y2)