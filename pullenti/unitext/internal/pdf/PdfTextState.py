# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import math

from pullenti.unitext.internal.pdf.PdfName import PdfName
from pullenti.unitext.internal.pdf.Matrix import Matrix

class PdfTextState:
    
    def __init__(self) -> None:
        self.ctm_stack = None;
        self.box_height = 0
        self.font_size = 0
        self.font = None;
        self.char_space = 0
        self.word_space = 0
        self.wscale = 100
        self.leading = 0
        self.rise = 0
        self.render = 0
        self.tlm = Matrix()
        self.tm = Matrix()
        self.ctm_stack = list()
        self.ctm_stack.append(Matrix())
    
    def parse_one(self, lex : typing.List['PdfObject'], i : int) -> bool:
        nam = lex[i].name
        if (nam == "Tc"): 
            self.char_space = lex[i - 1].get_double()
            return True
        if (nam == "Tw"): 
            self.word_space = lex[i - 1].get_double()
            return True
        if (nam == "Tz"): 
            self.wscale = lex[i - 1].get_double()
            return True
        if (nam == "Ts"): 
            self.rise = lex[i - 1].get_double()
            return True
        if (nam == "Tr"): 
            self.render = (math.floor(lex[i - 1].get_double()))
            return True
        if (nam == "TL"): 
            self.leading = lex[i - 1].get_double()
            return True
        if (nam == "Td" or nam == "TD"): 
            x = lex[i - 2].get_double()
            y = lex[i - 1].get_double()
            if (nam == "TD"): 
                self.leading = (- y)
            self.tlm.translate(x, y)
            self.tm.copy_from(self.tlm)
            return True
        if (nam == "T*"): 
            self.newline()
            return True
        if (nam == "Tm"): 
            self.tlm.set0_(lex[i - 6].get_double(), lex[i - 5].get_double(), lex[i - 4].get_double(), lex[i - 3].get_double(), lex[i - 2].get_double(), lex[i - 1].get_double())
            self.tm.copy_from(self.tlm)
            return True
        if (nam == "cm"): 
            mmm = Matrix()
            mmm.set0_(lex[i - 6].get_double(), lex[i - 5].get_double(), lex[i - 4].get_double(), lex[i - 3].get_double(), lex[i - 2].get_double(), lex[i - 1].get_double())
            if (len(self.ctm_stack) > 0): 
                mmm.multiply(self.ctm_stack[0])
                self.ctm_stack[0] = mmm
            else: 
                self.ctm_stack.insert(0, mmm)
            return True
        if (nam == "q"): 
            mmm = Matrix()
            if (len(self.ctm_stack) > 0): 
                mmm.copy_from(self.ctm_stack[0])
            self.ctm_stack.insert(0, mmm)
            return True
        if (nam == "Q"): 
            if (len(self.ctm_stack) > 0): 
                del self.ctm_stack[0]
        return False
    
    def newline(self) -> None:
        self.tlm.translate(0, - self.leading)
        self.tm.copy_from(self.tlm)