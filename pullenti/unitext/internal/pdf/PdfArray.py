# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.pdf.PdfObject import PdfObject
from pullenti.unitext.internal.pdf.PdfReference import PdfReference

class PdfArray(PdfObject):
    
    def __init__(self) -> None:
        super().__init__()
        self.__m_items = list()
    
    @property
    def items_count(self) -> int:
        return len(self.__m_items)
    
    def get_item(self, ind : int) -> 'PdfObject':
        if ((ind < 0) or ind >= len(self.__m_items)): 
            return None
        if (isinstance(self.__m_items[ind], PdfReference)): 
            obj = self.source_file.get_object(self.__m_items[ind].id0_)
            if (obj is None): 
                return None
            self.__m_items[ind] = obj
        return self.__m_items[ind]
    
    def is_simple(self, lev : int) -> bool:
        if (len(self.__m_items) > 10 or lev > 5): 
            return False
        i = 0
        while i < len(self.__m_items): 
            it = self.get_item(i)
            if (it is not None and not it.is_simple(lev + 1)): 
                return False
            i += 1
        return True
    
    def _add(self, obj : 'PdfObject') -> None:
        self.__m_items.append(obj)
    
    def to_string_ex(self, lev : int) -> str:
        if (lev > 10): 
            return "[...{0}]".format(self.items_count)
        res = io.StringIO()
        print("[", end="", file=res)
        i = 0
        i = 0
        first_pass638 = True
        while True:
            if first_pass638: first_pass638 = False
            else: i += 1
            if (not (i < len(self.__m_items))): break
            if (i > 0): 
                print(", ", end="", file=res)
            if (res.tell() > 100): 
                break
            it = self.get_item(i)
            if (it is None): 
                print("NULL", end="", file=res)
            elif (not it.is_simple(lev + 1)): 
                break
            else: 
                str0_ = it.to_string_ex(lev + 1)
                if (len(str0_) < 20): 
                    print(str0_, end="", file=res)
                    continue
                else: 
                    break
        if (i < len(self.__m_items)): 
            print("... {0}".format(len(self.__m_items)), end="", file=res, flush=True)
        print("]", end="", file=res)
        return Utils.toStringStringIO(res)
    
    def _post_parse(self, stream : 'PdfStream') -> None:
        self.__m_items.clear()
        p0 = stream.position
        ch = stream.read_byte()
        if ((chr(ch)) != '['): 
            return
        while True:
            i = stream.peek_solid_byte()
            if (i < 0): 
                break
            ch = (i)
            if ((chr(ch)) == ']'): 
                stream.position = stream.position + 1
                return
            obj = stream.parse_object(self.source_file, False)
            if (obj is None): 
                break
            self.__m_items.append(obj)
    
    def get_double(self) -> float:
        if (len(self.__m_items) < 1): 
            return 0
        it = self.get_item(0)
        if (it is None): 
            return 0
        return it.get_double()