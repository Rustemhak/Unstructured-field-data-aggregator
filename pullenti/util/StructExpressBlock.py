# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.StructExpressLine import StructExpressLine

class StructExpressBlock:
    
    def __init__(self) -> None:
        self.lines = list()
        self.is_app = False
        self.has_structure = False
    
    @property
    def begin_char(self) -> int:
        if (len(self.lines) > 0): 
            return self.lines[0].begin_char
        return 0
    
    @property
    def end_char(self) -> int:
        if (len(self.lines) > 0): 
            return self.lines[len(self.lines) - 1].end_char
        return 0
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("[{0}..{1}]".format(self.begin_char, self.end_char), end="", file=res, flush=True)
        if (self.is_app): 
            print(" Appendix", end="", file=res)
        if (self.has_structure): 
            print(" Structured", end="", file=res)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def parse(text : str) -> typing.List['StructExpressBlock']:
        lines_ = list()
        i = 0
        while i < len(text): 
            wrapi609 = RefOutArgWrapper(i)
            li = StructExpressLine.try_parse(text, wrapi609)
            i = wrapi609.value
            if (li is None): 
                break
            lines_.append(li)
        if (len(lines_) == 0): 
            return None
        i = 0
        while i < len(lines_): 
            if (lines_[i].is_start_of_app and lines_[i + 1].is_start_of_app): 
                while i < len(lines_): 
                    if (lines_[i].is_start_of_app): 
                        lines_[i].is_start_of_app = False
                    else: 
                        break
                    i += 1
            i += 1
        res = list()
        cur = StructExpressBlock()
        res.append(cur)
        i = 0
        while i < len(lines_): 
            li = lines_[i]
            if (li.is_start_of_app): 
                if (len(cur.lines) > 0): 
                    cur = StructExpressBlock()
                    res.append(cur)
                cur.is_app = True
            cur.lines.append(li)
            i += 1
        for b in res: 
            b.__analyze()
        return res
    
    def __analyze(self) -> None:
        clauses = 0
        numbered = 0
        illegals = 0
        for li in self.lines: 
            if (li.keyword == "СТАТЬЯ" or li.keyword == "СТАТТЯ"): 
                clauses += 1
            if (li.number is not None): 
                numbered += 1
            if (li.illegal_chars >= 2): 
                illegals += 1
        if (clauses > 1): 
            self.has_structure = True
        elif (clauses == 1 and numbered > 3): 
            self.has_structure = True
        elif (numbered > 5 and numbered > (math.floor(len(self.lines) / 2)) and (illegals < 2)): 
            self.has_structure = True