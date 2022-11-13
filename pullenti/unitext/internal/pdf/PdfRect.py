# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class PdfRect:
    
    def __init__(self) -> None:
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
    
    @property
    def left(self) -> float:
        return self.x1
    
    @property
    def right(self) -> float:
        return self.x2
    
    @property
    def width(self) -> float:
        return self.x2 - self.x1
    
    @property
    def top(self) -> float:
        return self.y1
    
    @property
    def bottom(self) -> float:
        return self.y2
    
    @property
    def height(self) -> float:
        return self.y2 - self.y1
    
    def __str__(self) -> str:
        return "[x1={0}, x2={1}, y1={2}, y2={3}".format(self.x1, self.x2, self.y1, self.y2)