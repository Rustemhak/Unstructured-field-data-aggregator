# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.rtf.RichTextBlock import RichTextBlock

class RichTextCell(RichTextBlock):
    
    def __init__(self) -> None:
        super().__init__()
        self.cols_span = 1
        self.rows_span = 1
        self._column_id = 0
        self._end_of = False
        self._merge_to_top = False
        self._merge_bottoms = False
        self._fist_grid = -1
        self._last_grid = -1
        self._res_col_index = -1
    
    def __str__(self) -> str:
        str0_ = "ColId={0}, {1}".format(self._column_id, super().__str__())
        if (self.cols_span > 1): 
            str0_ = "{0}, ColSpan={1}".format(str0_, self.cols_span)
        if (self.rows_span > 1): 
            str0_ = "{0}, RowSpan={1}".format(str0_, self.rows_span)
        if (self._end_of): 
            str0_ += " EndOf"
        if (self._merge_to_top): 
            str0_ += " MergeToTop"
        if (self._merge_bottoms): 
            str0_ += " MergeBottoms"
        return str0_