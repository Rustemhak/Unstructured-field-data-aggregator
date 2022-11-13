# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.internal.rtf.RichTextItem import RichTextItem

class RichTextRow(RichTextItem):
    
    class CellInfo:
        
        def __init__(self) -> None:
            self.id0_ = 0
            self.hor_merge = False
            self.vert_merge_first = False
            self.vert_merge_next = False
            self.width = 0
        
        def __str__(self) -> str:
            return "{0} {1}{2}{3}".format(self.id0_, ("Merge " if self.hor_merge else ""), ("VertMergeFirst " if self.vert_merge_first else ""), ("VertMergeNext " if self.vert_merge_next else ""))
        
        @staticmethod
        def _new230(_arg1 : int) -> 'CellInfo':
            res = RichTextRow.CellInfo()
            res.id0_ = _arg1
            return res
    
    def __init__(self) -> None:
        super().__init__()
        self._end_of = False
        self._last_row = False
        self._cells_info = list()
    
    def _add_cmd(self, cmd : str) -> bool:
        if (cmd is None): 
            return False
        if (cmd == "lastrow"): 
            self._last_row = True
            return True
        last = (None if len(self._cells_info) == 0 else self._cells_info[len(self._cells_info) - 1])
        if (cmd.startswith("cellx")): 
            idd = 0
            wrapidd231 = RefOutArgWrapper(0)
            inoutres232 = Utils.tryParseInt(cmd[5:], wrapidd231)
            idd = wrapidd231.value
            if (inoutres232): 
                if (idd > 0): 
                    for ii in self._cells_info: 
                        if (ii.id0_ == idd): 
                            if (last.id0_ == 0): 
                                if (last.hor_merge): 
                                    ii.hor_merge = True
                                if (last.vert_merge_first): 
                                    ii.vert_merge_first = True
                                if (last.vert_merge_next): 
                                    ii.vert_merge_next = True
                                self._cells_info.remove(last)
                            return True
                    if (last is not None and last.id0_ == 0): 
                        last.id0_ = idd
                    else: 
                        self._cells_info.append(RichTextRow.CellInfo._new230(idd))
            return True
        if (cmd.startswith("clwWidth")): 
            wi = 0
            wrapwi233 = RefOutArgWrapper(0)
            inoutres234 = Utils.tryParseInt(cmd[8:], wrapwi233)
            wi = wrapwi233.value
            if (inoutres234): 
                if (last is None or last.id0_ > 0): 
                    last = RichTextRow.CellInfo()
                    self._cells_info.append(last)
                last.width = wi
                return True
        if (cmd == "clmgf"): 
            if (last is None or last.id0_ > 0): 
                last = RichTextRow.CellInfo()
                self._cells_info.append(last)
            last.hor_merge = True
            return True
        if (cmd == "clvmgf"): 
            if (last is None or last.id0_ > 0): 
                last = RichTextRow.CellInfo()
                self._cells_info.append(last)
            last.vert_merge_first = True
            return True
        if (cmd == "clvmrg"): 
            if (last is None or last.id0_ > 0): 
                last = RichTextRow.CellInfo()
                self._cells_info.append(last)
            last.vert_merge_next = True
            return True
        return False
    
    def __str__(self) -> str:
        return "{0}{1}{2}".format(("LastRow " if self._last_row else ""), ("HasEnd " if self._end_of else ""), super().__str__())