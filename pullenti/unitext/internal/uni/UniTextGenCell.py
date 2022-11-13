# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class UniTextGenCell:
    
    def __init__(self) -> None:
        self.col_span = 1
        self.row_span = 1
        self.content = None;
        self.tag = 0
        self.width = None;
    
    def __str__(self) -> str:
        return "ColSpan:{0} RowSpan:{1} Content:{2}".format(self.col_span, self.row_span, ("null" if self.content is None else str(self.content)))