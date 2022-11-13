# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing

from pullenti.unitext.internal.pdf.PdfRect import PdfRect
from pullenti.unitext.internal.pdf.PdfFig import PdfFig
from pullenti.unitext.internal.pdf.PdfName import PdfName

class PdfPathState:
    
    def __init__(self, p : 'PdfPage') -> None:
        self.__m_page = None;
        self.__m_x = None;
        self.__m_y = None;
        self.__m_page = p
        self.__m_x = list()
        self.__m_y = list()
    
    def parse_one(self, lex : typing.List['PdfObject'], i : int) -> bool:
        if (i >= len(lex)): 
            return False
        nam = lex[i].name
        if (nam == "m"): 
            self.__m_x.clear()
            self.__m_y.clear()
            self.__m_x.append(lex[i - 2].get_double())
            self.__m_y.append(self.__m_page.height - lex[i - 1].get_double())
            return True
        if (nam == "l"): 
            self.__m_x.append(lex[i - 2].get_double())
            self.__m_y.append(self.__m_page.height - lex[i - 1].get_double())
            return True
        if (nam == "h"): 
            if (len(self.__m_x) > 0): 
                self.__m_x.append(self.__m_x[0])
                self.__m_y.append(self.__m_y[0])
            return True
        if (nam == "re"): 
            x = lex[i - 4].get_double()
            y = self.__m_page.height - lex[i - 3].get_double()
            w = lex[i - 2].get_double()
            h = lex[i - 1].get_double()
            self.__m_x.append(x)
            self.__m_y.append(y)
            self.__m_x.append(x)
            self.__m_y.append(y - h)
            self.__m_x.append(x + w)
            self.__m_y.append(y - h)
            self.__m_x.append(x + w)
            self.__m_y.append(y)
            self.__m_x.append(x)
            self.__m_y.append(y)
            return True
        if (nam == "n"): 
            self.__m_x.clear()
            self.__m_y.clear()
            return True
        if (((((nam == "S" or nam == "s" or nam == "b") or nam == "B" or nam == "B*") or nam == "b*" or nam == "f") or nam == "F" or nam == "f*") or nam == "W" or nam == "W*"): 
            if (len(self.__m_x) == 5 and self.__m_x[0] == self.__m_x[4] and self.__m_y[0] == self.__m_y[4]): 
                re = None
                if (self.__m_x[1] == self.__m_x[0] and self.__m_y[1] == self.__m_y[2] and self.__m_x[2] == self.__m_x[3]): 
                    re = PdfFig()
                    re.x1 = self.__m_x[0]
                    re.x2 = self.__m_x[2]
                    re.y1 = self.__m_y[0]
                    re.y2 = self.__m_y[1]
                elif (self.__m_y[0] == self.__m_y[1] and self.__m_x[1] == self.__m_x[2] and self.__m_y[2] == self.__m_y[3]): 
                    re = PdfFig()
                    re.x1 = self.__m_x[0]
                    re.x2 = self.__m_x[1]
                    re.y1 = self.__m_y[0]
                    re.y2 = self.__m_y[2]
                if (re is not None): 
                    if (re.x1 > re.x2): 
                        d = re.x1
                        re.x1 = re.x2
                        re.x2 = d
                    if (re.y1 > re.y2): 
                        d = re.y1
                        re.y1 = re.y2
                        re.y2 = d
                    self.__m_page.items.append(re)
                    return True
            ii = 0
            while ii < (len(self.__m_x) - 1): 
                if (self.__m_x[ii] == self.__m_x[ii + 1] or self.__m_y[ii] == self.__m_y[ii + 1]): 
                    re = PdfFig()
                    re.x1 = self.__m_x[ii]
                    re.x2 = self.__m_x[ii + 1]
                    re.y1 = self.__m_y[ii]
                    re.y2 = self.__m_y[ii + 1]
                    if (re.x1 > re.x2): 
                        d = re.x1
                        re.x1 = re.x2
                        re.x2 = d
                    if (re.y1 > re.y2): 
                        d = re.y1
                        re.y1 = re.y2
                        re.y2 = d
                    self.__m_page.items.append(re)
                ii += 1
            return True
        return False