# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.rtf.RichTextRow import RichTextRow
from pullenti.unitext.internal.rtf.RichTextCell import RichTextCell
from pullenti.unitext.internal.rtf.RichTextItem import RichTextItem

class RichTextTable(RichTextItem):
    
    def __init__(self) -> None:
        super().__init__()
        self._column_ids = list()
    
    def __str__(self) -> str:
        return "Table: {0} Columns, {1} Rows".format(len(self._column_ids), len(self.children))
    
    @property
    def _last_row(self) -> 'RichTextRow':
        if (self.children is None or len(self.children) == 0): 
            return None
        return Utils.asObjectOrNull(self.children[len(self.children) - 1], RichTextRow)
    
    @property
    def _last_cell(self) -> 'RichTextCell':
        r = self._last_row
        if (r is None): 
            return None
        if (r.children is None or len(r.children) == 0): 
            return None
        return Utils.asObjectOrNull(r.children[len(r.children) - 1], RichTextCell)
    
    def _correct(self) -> None:
        if (self._last_row is not None and not self._last_row._end_of and ((self._last_cell is None or not self._last_cell._end_of))): 
            del self.children[len(self.children) - 1]
        for r in self.children: 
            rr = Utils.asObjectOrNull(r, RichTextRow)
            if (rr is None): 
                continue
            if (rr.children is not None and len(rr.children) > 1): 
                la = Utils.asObjectOrNull(rr.children[len(rr.children) - 1], RichTextCell)
                if (not la._end_of and la.text is None and la.children is None): 
                    del rr.children[len(rr.children) - 1]
            for ci in rr._cells_info: 
                if (ci.id0_ > 0 and not ci.id0_ in self._column_ids): 
                    self._column_ids.append(ci.id0_)
            if (len(rr._cells_info) == len(rr.children)): 
                ii = 0
                while ii < len(rr._cells_info): 
                    rr.children[ii]._column_id = rr._cells_info[ii].id0_
                    rr.children[ii]._merge_to_top = rr._cells_info[ii].vert_merge_next
                    rr.children[ii]._merge_bottoms = rr._cells_info[ii].vert_merge_first
                    ii += 1
        self._column_ids.sort()
        vert_merge = dict()
        for r in self.children: 
            rr = Utils.asObjectOrNull(r, RichTextRow)
            if (rr is None): 
                continue
            cells = list()
            for c in rr.children: 
                if (isinstance(c, RichTextCell)): 
                    cells.append(Utils.asObjectOrNull(c, RichTextCell))
            for cel in cells: 
                cel._last_grid = Utils.indexOfList(self._column_ids, cel._column_id, 0)
            ii = 0
            while ii < len(cells): 
                if (ii == 0): 
                    cells[ii]._fist_grid = 0
                elif (cells[ii - 1]._last_grid >= 0): 
                    cells[ii]._fist_grid = (cells[ii - 1]._last_grid + 1)
                if (ii == (len(cells) - 1)): 
                    cells[ii]._last_grid = (len(self._column_ids) - 1)
                ii += 1
            ii = 0
            while ii < len(cells): 
                cel = cells[ii]
                if (cel._last_grid > cel._fist_grid and cel._fist_grid >= 0): 
                    cel.cols_span = ((cel._last_grid - cel._fist_grid) + 1)
                if (cel._merge_bottoms and cel._last_grid >= 0): 
                    if (not cel._last_grid in vert_merge): 
                        vert_merge[cel._last_grid] = cel
                    else: 
                        vert_merge[cel._last_grid] = cel
                elif (cel._merge_to_top and cel._last_grid in vert_merge): 
                    vert_merge[cel._last_grid].rows_span += 1
                    rr.children.remove(cel)
                ii += 1