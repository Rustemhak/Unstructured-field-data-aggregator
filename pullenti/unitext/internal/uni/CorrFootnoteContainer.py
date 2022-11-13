# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.internal.uni.CorrLine import CorrLine
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextComment import UnitextComment
from pullenti.unitext.UnitextFootnote import UnitextFootnote
from pullenti.unitext.UnitextList import UnitextList
from pullenti.unitext.UnitextTable import UnitextTable
from pullenti.unitext.UnitextPlaintextType import UnitextPlaintextType
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.internal.uni.CorrFootnoteTyps import CorrFootnoteTyps
from pullenti.unitext.internal.uni.CorrFootnoteTag import CorrFootnoteTag
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextHyperlink import UnitextHyperlink
from pullenti.unitext.UnitextNewline import UnitextNewline
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak

class CorrFootnoteContainer:
    
    def __init__(self) -> None:
        self.typ = CorrFootnoteTyps.DIGIT
        self.start_number = 1
        self.begin_ind = 0
        self.end_ind = 0
        self.items = list()
    
    def __str__(self) -> str:
        res = io.StringIO()
        i = 0
        while i < len(self.items): 
            print("<{0}>{1} \r\n".format((str((self.start_number + i)) if self.typ == CorrFootnoteTyps.DIGIT or self.typ == CorrFootnoteTyps.SUPDIGIT else "*"), self.items[i]), end="", file=res, flush=True)
            i += 1
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def try_parse1(it : 'UnitextItem') -> 'CorrFootnoteContainer':
        if (isinstance(it, UnitextPlaintext)): 
            pl = Utils.asObjectOrNull(it, UnitextPlaintext)
            i = 0
            wrapi292 = RefOutArgWrapper(i)
            tag = CorrFootnoteTag.try_parse(pl.text, wrapi292, True, False)
            i = wrapi292.value
            if (tag is None or tag.number != 1): 
                return None
            res = CorrFootnoteContainer._new290(tag.typ)
            txt = pl.text[i + 1:].strip()
            i = 0
            first_pass658 = True
            while True:
                if first_pass658: first_pass658 = False
                else: i += 1
                if (not (i < len(txt))): break
                j = i
                wrapj291 = RefOutArgWrapper(j)
                tag1 = CorrFootnoteTag.try_parse(txt, wrapj291, True, False)
                j = wrapj291.value
                if (tag1 is None): 
                    continue
                if (tag1.typ != tag.typ): 
                    continue
                if (tag1.number != (len(res.items) + 2)): 
                    continue
                if (i > 0): 
                    res.items.append(txt[0:0+i].strip())
                txt = txt[j + 1:].strip()
                i = -1
            if (not Utils.isNullOrEmpty(txt)): 
                res.items.append(txt)
            return res
        if (isinstance(it, UnitextContainer)): 
            cnt = Utils.asObjectOrNull(it, UnitextContainer)
            res = CorrFootnoteContainer.try_parse(cnt.children, 0, -1)
            if (res is None): 
                return None
            if (res.end_ind != (len(cnt.children) - 1)): 
                return None
            return res
        return None
    
    @staticmethod
    def try_parse(items_ : typing.List['UnitextItem'], ind : int, num_start : int) -> 'CorrFootnoteContainer':
        if ((ind < 1) or (ind + 1) > len(items_)): 
            return None
        if (not (isinstance(items_[ind - 1], UnitextNewline)) and not (isinstance(items_[ind - 1], UnitextPagebreak))): 
            return None
        ind0 = ind
        it = Utils.asObjectOrNull(items_[ind], UnitextPlaintext)
        if (it is None or Utils.isNullOrEmpty(it.text)): 
            return None
        if (Utils.isNullOrEmpty(it.text.strip()) and ((ind + 1) < len(items_)) and (isinstance(items_[ind + 1], UnitextPlaintext))): 
            ind += 1
            it = (Utils.asObjectOrNull(items_[ind], UnitextPlaintext))
        i = 0
        wrapi306 = RefOutArgWrapper(i)
        tag = CorrFootnoteTag.try_parse(it.text, wrapi306, True, False)
        i = wrapi306.value
        if (tag is None): 
            nn = 0
            wrapnn294 = RefOutArgWrapper(0)
            inoutres295 = Utils.tryParseInt(it.text.strip(), wrapnn294)
            nn = wrapnn294.value
            if (it.typ == UnitextPlaintextType.SUP and inoutres295): 
                tag = CorrFootnoteTag._new293(nn, CorrFootnoteTyps.SUPDIGIT)
                if (ind != ind0): 
                    del items_[ind0]
                    ind = ind0
            else: 
                return None
        elif (tag.typ == CorrFootnoteTyps.VERYDOUBT): 
            if (tag.number == 24): 
                pass
            ok = False
            has_lines = False
            j = ind - 1
            first_pass659 = True
            while True:
                if first_pass659: first_pass659 = False
                else: j -= 1
                if (not (j >= 0 and ((j > (ind - 10))))): break
                itt = items_[j]
                if (itt.is_whitespaces): 
                    continue
                ttt = itt.get_plaintext_string(None)
                if (Utils.isNullOrEmpty(ttt)): 
                    continue
                if (ttt.startswith("-----")): 
                    has_lines = True
                    continue
                if (not has_lines): 
                    break
                ii = 0
                while ii < len(ttt): 
                    wrapii296 = RefOutArgWrapper(ii)
                    tag0 = CorrFootnoteTag.try_parse(ttt, wrapii296, False, False)
                    ii = wrapii296.value
                    if (tag0 is not None): 
                        if (tag0.number == tag.number and tag0.typ == CorrFootnoteTyps.DIGIT): 
                            ok = True
                            break
                    ii += 1
            if (not ok): 
                return None
            tag.typ = CorrFootnoteTyps.DIGIT
        res = CorrFootnoteContainer._new290(tag.typ)
        res.begin_ind = ind0
        res.end_ind = ind
        if (tag.typ == CorrFootnoteTyps.DIGIT or tag.typ == CorrFootnoteTyps.SUPDIGIT): 
            res.start_number = tag.number
        ind -= 1
        first_pass660 = True
        while True:
            if first_pass660: first_pass660 = False
            else: ind += 1
            if (not (ind < len(items_))): break
            if ((isinstance(items_[ind], UnitextNewline)) or (isinstance(items_[ind], UnitextPagebreak))): 
                continue
            if (not (isinstance(items_[ind - 1], UnitextNewline)) and not (isinstance(items_[ind - 1], UnitextPagebreak))): 
                break
            it = (Utils.asObjectOrNull(items_[ind], UnitextPlaintext))
            if (it is None): 
                break
            i = 0
            wrapi305 = RefOutArgWrapper(i)
            tag1 = CorrFootnoteTag.try_parse(it.text, wrapi305, True, False)
            i = wrapi305.value
            if (tag1 is None): 
                nn = 0
                wrapnn299 = RefOutArgWrapper(0)
                inoutres300 = Utils.tryParseInt(it.text.strip(), wrapnn299)
                nn = wrapnn299.value
                if (it.typ == UnitextPlaintextType.SUP and inoutres300): 
                    tag1 = CorrFootnoteTag._new293(nn, CorrFootnoteTyps.SUPDIGIT)
            if (tag1 is None): 
                break
            if (tag1.typ == CorrFootnoteTyps.VERYDOUBT): 
                if (ind == res.end_ind): 
                    tag1.typ = CorrFootnoteTyps.DIGIT
                else: 
                    break
            if (tag.typ != tag1.typ): 
                break
            if ((tag1.number - res.start_number) != len(res.items)): 
                break
            res.end_ind = ind
            txt = ("" if tag.typ == CorrFootnoteTyps.SUPDIGIT else it.text[i + 1:].strip())
            jj = ind + 1
            first_pass661 = True
            while True:
                if first_pass661: first_pass661 = False
                else: jj += 1
                if (not (jj < len(items_))): break
                if (isinstance(items_[jj], UnitextNewline)): 
                    if (items_[jj].count > 1): 
                        break
                    continue
                if (isinstance(items_[jj], UnitextComment)): 
                    continue
                txt1 = None
                pl = Utils.asObjectOrNull(items_[jj], UnitextPlaintext)
                if (pl is not None): 
                    txt1 = pl.text
                elif (isinstance(items_[jj], UnitextHyperlink)): 
                    txt1 = items_[jj].get_plaintext_string(None)
                if (txt1 is None): 
                    break
                if (Utils.startsWithString(txt1, "Текст ", True)): 
                    break
                i = 0
                wrapi303 = RefOutArgWrapper(i)
                inoutres304 = CorrFootnoteTag.try_parse(txt1, wrapi303, True, False)
                i = wrapi303.value
                if (inoutres304 is not None): 
                    break
                wrapi301 = RefOutArgWrapper(0)
                inoutres302 = Utils.tryParseInt(txt1.strip(), wrapi301)
                i = wrapi301.value
                if (it.typ == UnitextPlaintextType.SUP and inoutres302): 
                    break
                if (tag.typ == CorrFootnoteTyps.SUPDIGIT and jj == (ind + 1)): 
                    pass
                elif (len(txt) > (math.floor((1.2 * (len(it.text)))))): 
                    if (jj > 0 and (isinstance(items_[jj - 1], UnitextComment))): 
                        pass
                    else: 
                        break
                chs = 0
                hiphs = 0
                for ch in txt1: 
                    if (str.isalnum(ch)): 
                        chs += 1
                if (len(txt1) > 1 and chs == 0): 
                    ind = jj
                    res.end_ind = ind
                    break
                for ch in txt1: 
                    if (str.isalnum(ch)): 
                        break
                    elif (ch == '_' or ch == '-'): 
                        hiphs += 1
                if (hiphs > 10): 
                    ind = jj
                    res.end_ind = ind
                    break
                if (len(txt) == 0): 
                    txt = txt1.strip()
                else: 
                    txt = "{0} {1}".format(txt, txt1.strip())
                ind = jj
                res.end_ind = ind
            res.items.append(txt)
        delim_line = False
        ind = res.begin_ind
        if (ind >= 2 and (isinstance(items_[ind - 1], UnitextNewline))): 
            it = (Utils.asObjectOrNull(items_[ind - 2], UnitextPlaintext))
            if (it is not None): 
                cou = 0
                i = 0
                i = 0
                while i < len(it.text): 
                    if (CorrLine.is_hiphen(it.text[i]) or it.text[i] == '_'): 
                        cou += 1
                    elif (not Utils.isWhitespace(it.text[i])): 
                        break
                    i += 1
                if (cou > 0 and i >= len(it.text)): 
                    res.begin_ind -= 2
                    delim_line = True
        if (res.start_number != 1 and res.start_number != num_start): 
            if (not delim_line and (len(res.items) < 2)): 
                if (res.typ != CorrFootnoteTyps.SUPDIGIT): 
                    return None
        return res
    
    def correct_item(self, it : 'UnitextItem', robust : bool) -> 'UnitextItem':
        pl = Utils.asObjectOrNull(it, UnitextPlaintext)
        if (pl is not None): 
            if (self.typ == CorrFootnoteTyps.SUPDIGIT and pl.typ == UnitextPlaintextType.SUP): 
                num = 0
                wrapnum308 = RefOutArgWrapper(0)
                inoutres309 = Utils.tryParseInt(pl.text.strip(), wrapnum308)
                num = wrapnum308.value
                if (inoutres309): 
                    ii = num - self.start_number
                    if ((ii < 0) or ii >= len(self.items)): 
                        return pl
                    fn = UnitextFootnote()
                    fn.content = (UnitextPlaintext._new51(self.items[ii]))
                    fn.custom_mark = str(num)
                    return fn
            cnt = None
            txt = pl.text
            i = 0
            first_pass662 = True
            while True:
                if first_pass662: first_pass662 = False
                else: i += 1
                if (not (i < len(txt))): break
                if (Utils.isWhitespace(txt[i])): 
                    continue
                j = i
                wrapj313 = RefOutArgWrapper(j)
                tag = CorrFootnoteTag.try_parse(txt, wrapj313, False, robust)
                j = wrapj313.value
                if (tag is None): 
                    continue
                if (tag.typ != self.typ): 
                    continue
                ii = tag.number - self.start_number
                if ((ii < 0) or ii >= len(self.items)): 
                    continue
                if (cnt is None): 
                    cnt = UnitextContainer()
                if (i > 0): 
                    cnt.children.append(UnitextPlaintext._new51(txt[0:0+i]))
                cnt.children.append(UnitextFootnote._new312(UnitextPlaintext._new51(self.items[ii])))
                j += 1
                if (j >= len(txt)): 
                    txt = ""
                    break
                txt = txt[j:]
                i = -1
            if (not Utils.isNullOrEmpty(txt) and cnt is not None): 
                cnt.children.append(UnitextPlaintext._new51(txt))
            return cnt
        if (isinstance(it, UnitextContainer)): 
            cnt = Utils.asObjectOrNull(it, UnitextContainer)
            is_ch = False
            i = 0
            first_pass663 = True
            while True:
                if first_pass663: first_pass663 = False
                else: i += 1
                if (not (i < len(cnt.children))): break
                ch = self.correct_item(cnt.children[i], robust)
                if (ch is None): 
                    continue
                cnt.children[i] = ch
                is_ch = True
            return (cnt if is_ch else None)
        if (isinstance(it, UnitextTable)): 
            tab = Utils.asObjectOrNull(it, UnitextTable)
            is_ch = False
            r = 0
            while r < tab.rows_count: 
                c = 0
                first_pass664 = True
                while True:
                    if first_pass664: first_pass664 = False
                    else: c += 1
                    if (not (c < tab.cols_count)): break
                    cel = tab.get_cell(r, c)
                    if (cel is None): 
                        continue
                    if (cel.row_begin != r or cel.col_begin != c or cel.content is None): 
                        continue
                    cnt = self.correct_item(cel.content, robust)
                    if (cnt is not None): 
                        cel.content = cnt
                        is_ch = True
                r += 1
            return (tab if is_ch else None)
        if (isinstance(it, UnitextList)): 
            li = Utils.asObjectOrNull(it, UnitextList)
            is_ch = False
            for ii in li.items: 
                cnt = self.correct_item(ii.content, robust)
                if (cnt is not None): 
                    is_ch = True
                    ii.content = cnt
                sub = Utils.asObjectOrNull(self.correct_item(ii.sublist, robust), UnitextList)
                if (sub is not None): 
                    ii.sublist = sub
                    is_ch = True
            return (li if is_ch else None)
        return None
    
    @staticmethod
    def _new290(_arg1 : 'CorrFootnoteTyps') -> 'CorrFootnoteContainer':
        res = CorrFootnoteContainer()
        res.typ = _arg1
        return res