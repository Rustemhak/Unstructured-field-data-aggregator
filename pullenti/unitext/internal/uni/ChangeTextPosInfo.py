# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

class ChangeTextPosInfo:
    # для корректировки beginchar и endchar у стилевых фрагментов
    
    def __init__(self, fr : 'UnitextStyledFragment', root : 'UnitextItem') -> None:
        self.__bmap = None
        self.__emap = None
        self.__m_root = None;
        self.__bpos = None;
        self.__epos = None;
        if (fr.end_char == 0): 
            return
        self.__bmap = Utils.newArray(fr.end_char + 1, None)
        self.__emap = Utils.newArray(fr.end_char + 1, None)
        its = list()
        root.get_all_items(its, 0)
        for it in its: 
            if (it.end_char > 0 and (it.end_char < len(self.__bmap))): 
                self.__bmap[it.begin_char] = it
                self.__emap[it.end_char] = it
        self.__m_root = fr
    
    def restore(self, new_len : int) -> None:
        if (self.__bmap is None): 
            return
        self.__bpos = Utils.newArray(len(self.__bmap), 0)
        self.__epos = Utils.newArray(len(self.__bmap), 0)
        p = 0
        i = 0
        while i < len(self.__bmap): 
            it = self.__bmap[i]
            if (it is not None): 
                if (it.begin_char < p): 
                    pass
                p = it.begin_char
            self.__bpos[i] = p
            p += 1
            i += 1
        p = (new_len - 1)
        for i in range(len(self.__emap) - 1, -1, -1):
            it = self.__emap[i]
            if (it is not None): 
                if (p > 0 and it.end_char > p): 
                    pass
                p = it.end_char
            self.__epos[i] = p
            p -= 1
        self.__restore(self.__m_root)
    
    def __restore(self, fr : 'UnitextStyledFragment') -> None:
        if (fr.begin_char >= 0 and (fr.begin_char < len(self.__bpos))): 
            if (self.__bpos[fr.begin_char] < 0): 
                pass
            fr.begin_char = self.__bpos[fr.begin_char]
        if (fr.end_char >= 0 and (fr.end_char < len(self.__epos))): 
            if (self.__epos[fr.end_char] < 0): 
                pass
            fr.end_char = self.__epos[fr.end_char]
        for ch in fr.children: 
            self.__restore(ch)