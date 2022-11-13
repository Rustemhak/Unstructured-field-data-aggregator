# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextTable import UnitextTable
from pullenti.unitext.internal.uni.CorrLine import CorrLine

class CorrTable:
    
    def __init__(self) -> None:
        self.begin_ind = 0
        self.end_ind = 0
        self.result = None;
    
    @staticmethod
    def try_parse(lines : typing.List['CorrLine'], i : int, nexti : int) -> 'CorrTable':
        nexti.value = i
        if (i >= len(lines)): 
            return None
        if (not lines[i].can_be_empty_line_of_table): 
            return None
        width = len(lines[i].text)
        j = 0
        j = (i + 1)
        while j < len(lines): 
            if (not lines[j].is_pure_text): 
                break
            elif (lines[j].length != lines[i].length or len(lines[j].text) != width): 
                break
            j += 1
        height = j - i
        nexti.value = (j - 1)
        if ((width < 30) or (height < 4)): 
            return None
        verts = list()
        j = 0
        while j < width: 
            r = 0
            r = 0
            first_pass668 = True
            while True:
                if first_pass668: first_pass668 = False
                else: r += 1
                if (not (r < height)): break
                if (lines[i + r].can_has_hor_line_of_table): 
                    continue
                if (j >= len(lines[i + r].text)): 
                    continue
                ch = lines[i + r].text[j]
                if (CorrLine.is_table_char(ch) and not CorrLine.is_hiphen(ch)): 
                    verts.append(j)
                    break
            j += 1
        if (len(verts) < 3): 
            return None
        col_begs = list()
        col_ends = list()
        j = 0
        while j < len(verts): 
            b = 0
            if (j > 0): 
                b = (verts[j - 1] + 1)
            if ((verts[j] - 1) >= b): 
                col_begs.append(b)
                col_ends.append(verts[j] - 1)
            j += 1
        if (len(col_begs) < 2): 
            return None
        rnums = list()
        rnum = 0
        j = 0
        while j < height: 
            rnums.append(rnum)
            w = 0
            w = 0
            first_pass669 = True
            while True:
                if first_pass669: first_pass669 = False
                else: w += 1
                if (not (w < width)): break
                if (not w in verts): 
                    if (w >= len(lines[i + j].text)): 
                        continue
                    ch = lines[i + j].text[w]
                    if (CorrLine.is_table_char(ch)): 
                        if (CorrLine.is_hiphen(ch)): 
                            if (w > 0 and lines[i + j].text[w - 1] == ch): 
                                pass
                            elif (((w + 1) < width) and lines[i + j].text[w + 1] == ch): 
                                pass
                            else: 
                                continue
                        rnum += 1
                        break
            j += 1
        if (rnum < 3): 
            return None
        tab = CorrTable._new328(i, (i + height) - 1)
        tab.result = UnitextTable()
        tmp = io.StringIO()
        h = 0
        while h < len(rnums): 
            c = 0
            first_pass670 = True
            while True:
                if first_pass670: first_pass670 = False
                else: c += 1
                if (not (c < len(col_begs))): break
                w0 = col_begs[c]
                w1 = col_ends[c]
                h0 = h
                ww = 0
                while h0 < len(rnums): 
                    ww = w0
                    while ww <= w1: 
                        ch = lines[i + h0].text[ww]
                        if (not CorrLine.is_table_char(ch)): 
                            break
                        ww += 1
                    if (ww < w1): 
                        break
                    h0 += 1
                if (h0 >= len(rnums)): 
                    continue
                cel0 = tab.result.get_cell(rnums[h0], c)
                if (cel0 is not None): 
                    continue
                cc = 0
                cc = (c + 1)
                while cc < len(col_begs): 
                    ww = col_ends[cc - 1]
                    while ww <= col_ends[cc]: 
                        ch = lines[i + h0].text[ww]
                        if (CorrLine.is_table_char(ch) and not CorrLine.is_hiphen(ch)): 
                            break
                        ww += 1
                    if (ww < col_ends[cc]): 
                        break
                    w1 = col_ends[cc]
                    cc += 1
                cc -= 1
                h1 = 0
                h1 = (h0 + 1)
                while h1 < len(rnums): 
                    ww = w0
                    while ww <= w1: 
                        ch = lines[i + h1].text[ww]
                        if (CorrLine.is_table_char(ch)): 
                            if (CorrLine.is_hiphen(ch)): 
                                if (ww > 0 and lines[i + h1].text[ww - 1] == ch): 
                                    break
                                if (((ww + 1) < width) and lines[i + h1].text[ww + 1] == ch): 
                                    break
                            else: 
                                break
                        ww += 1
                    if (ww < w1): 
                        break
                    h1 += 1
                h1 -= 1
                Utils.setLengthStringIO(tmp, 0)
                hh = h0
                while hh <= h1: 
                    ww = (w0 - 1)
                    first_pass671 = True
                    while True:
                        if first_pass671: first_pass671 = False
                        else: ww += 1
                        if (not (ww <= w1)): break
                        if (ww < 0): 
                            continue
                        ch = lines[i + hh].text[ww]
                        if (CorrLine.is_table_char(ch)): 
                            if (not CorrLine.is_hiphen(ch)): 
                                continue
                        if (Utils.isWhitespace(ch)): 
                            if (tmp.tell() > 0 and Utils.getCharAtStringIO(tmp, tmp.tell() - 1) == ' '): 
                                continue
                            ch = ' '
                        print(ch, end="", file=tmp)
                    if ((hh < h1) and tmp.tell() > 0): 
                        print(' ', end="", file=tmp)
                    for jj in range(tmp.tell() - 1, -1, -1):
                        if (Utils.getCharAtStringIO(tmp, jj) != ' '): 
                            if (CorrLine.is_hiphen(Utils.getCharAtStringIO(tmp, jj))): 
                                Utils.setLengthStringIO(tmp, jj)
                            break
                    hh += 1
                cel = tab.result.add_cell(rnums[h0], rnums[h1], c, cc, UnitextPlaintext._new51(Utils.toStringStringIO(tmp).strip()))
                c = cc
            h += 1
        tab.result.optimize(False, None)
        return tab
    
    @staticmethod
    def _new328(_arg1 : int, _arg2 : int) -> 'CorrTable':
        res = CorrTable()
        res.begin_ind = _arg1
        res.end_ind = _arg2
        return res