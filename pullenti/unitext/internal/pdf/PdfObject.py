# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class PdfObject:
    
    def __init__(self) -> None:
        self.source_file = None
        self.id0_ = 0
        self.version = 0
        self.tag = None;
    
    def is_simple(self, lev : int) -> bool:
        return False
    
    def to_string_ex(self, lev : int) -> str:
        return "?"
    
    def __str__(self) -> str:
        return self.to_string_ex(0)
    
    def get_double(self) -> float:
        return 0