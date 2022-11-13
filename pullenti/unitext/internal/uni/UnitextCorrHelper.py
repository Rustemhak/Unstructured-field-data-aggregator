# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.internal.uni.CorrLine import CorrLine
from pullenti.unitext.UnitextTable import UnitextTable
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.unitext.internal.uni.CorrFootnoteTyps import CorrFootnoteTyps
from pullenti.unitext.internal.uni.CorrFootnoteContainer import CorrFootnoteContainer
from pullenti.unitext.internal.uni.CorrTable import CorrTable
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak
from pullenti.unitext.internal.uni.LocCorrTyp import LocCorrTyp
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextNewline import UnitextNewline
from pullenti.unitext.internal.uni.CorrPageText import CorrPageText
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextHyperlink import UnitextHyperlink
from pullenti.unitext.GetPlaintextParam import GetPlaintextParam

class UnitextCorrHelper:
    
    @staticmethod
    def remove_page_break_numeration(doc : 'UnitextDocument') -> None:
        cnt = Utils.asObjectOrNull(doc.content, UnitextContainer)
        if (cnt is None): 
            return
        tmp = io.StringIO()
        tmp_cnt = UnitextContainer()
        corr = False
        k = 0
        first_pass676 = True
        while True:
            if first_pass676: first_pass676 = False
            else: k += 1
            if (not (k < 2)): break
            pages = list()
            i = 0
            first_pass677 = True
            while True:
                if first_pass677: first_pass677 = False
                else: i += 1
                if (not (i < len(cnt.children))): break
                i0 = 0
                i1 = 0
                tmp_cnt.children.clear()
                if (k == 0): 
                    if (i == 0): 
                        pass
                    elif ((isinstance(cnt.children[i - 1], UnitextPagebreak)) and (isinstance(cnt.children[i], UnitextPlaintext))): 
                        pass
                    else: 
                        continue
                    i0 = i
                    i1 = i0
                    while i1 < len(cnt.children): 
                        chh = cnt.children[i1]
                        if (isinstance(chh, UnitextPlaintext)): 
                            pass
                        elif (isinstance(chh, UnitextHyperlink)): 
                            pass
                        else: 
                            break
                        tmp_cnt.children.append(chh)
                        i1 += 1
                    i1 -= 1
                else: 
                    if (i == (len(cnt.children) - 1)): 
                        i1 = i
                    elif (isinstance(cnt.children[i], UnitextPagebreak)): 
                        i1 = (i - 1)
                    else: 
                        continue
                    for i0 in range(i1, -1, -1):
                        chh = cnt.children[i0]
                        if (isinstance(chh, UnitextPlaintext)): 
                            pass
                        elif (isinstance(chh, UnitextHyperlink)): 
                            pass
                        else: 
                            break
                        tmp_cnt.children.append(chh)
                    else: i0 = -1
                    i0 += 1
                if (len(tmp_cnt.children) == 0): 
                    continue
                Utils.setLengthStringIO(tmp, 0)
                tmp_cnt.get_plaintext(tmp, GetPlaintextParam._new339(False))
                if (tmp.tell() == 0): 
                    continue
                page = CorrPageText._new340(Utils.toStringStringIO(tmp), k == 0, i0, i1)
                pages.append(page)
            if (len(pages) < 2): 
                continue
            tittext = CorrPageText.process(pages)
            k1 = k
            for i in range(len(pages) - 1, -1, -1):
                if (pages[i].corr): 
                    if (i == 0): 
                        pass
                    j = pages[i].i0
                    while j <= pages[i].i1: 
                        pl = Utils.asObjectOrNull(cnt.children[j], UnitextPlaintext)
                        if (pl is not None and pl.layout is not None): 
                            jj = 0
                            while jj < len(pl.layout): 
                                if (pl.layout[jj] is not None): 
                                    pl.layout[jj].ignored = True
                                jj += 1
                        j += 1
                    del cnt.children[pages[i].i0:pages[i].i0+(pages[i].i1 + 1) - pages[i].i0]
                    corr = True
                    k1 = (k - 1)
            if (tittext is not None): 
                pass
            k = k1
        for i in range(len(cnt.children) - 1, -1, -1):
            if (i >= len(cnt.children)): 
                continue
            pt = Utils.asObjectOrNull(cnt.children[i], UnitextPlaintext)
            if (pt is None): 
                continue
            n = 0
            wrapn341 = RefOutArgWrapper(0)
            inoutres342 = Utils.tryParseInt(pt.text.strip(), wrapn341)
            n = wrapn341.value
            if (not inoutres342): 
                continue
            if (i == 0 or (isinstance(cnt.children[i - 1], UnitextPagebreak)) or ((i > 1 and (isinstance(cnt.children[i - 1], UnitextNewline)) and (isinstance(cnt.children[i - 2], UnitextPagebreak))))): 
                if (((i + 1) < len(cnt.children)) and (isinstance(cnt.children[i + 1], UnitextNewline))): 
                    if (pt.layout is not None): 
                        for la in pt.layout: 
                            if (la is not None): 
                                la.ignored = True
                                la.page.top_number = n
                    del cnt.children[i:i+2]
                    continue
            elif ((i + 1) == len(cnt.children) or (isinstance(cnt.children[i + 1], UnitextPagebreak)) or ((((i + 2) < len(cnt.children)) and (isinstance(cnt.children[i + 1], UnitextNewline)) and (isinstance(cnt.children[i + 2], UnitextPagebreak))))): 
                if (i > 0 and (isinstance(cnt.children[i - 1], UnitextNewline))): 
                    if (pt.layout is not None): 
                        for la in pt.layout: 
                            if (la is not None): 
                                la.ignored = True
                                la.page.bottom_number = n
                    del cnt.children[i - 1:i - 1+2]
                    continue
        if (corr): 
            doc.optimize(False, None)
    
    __min_line_len = 50
    
    __max_line_len = 100
    
    @staticmethod
    def remove_false_new_lines(doc : 'UnitextDocument', replace_nbsp : bool) -> None:
        if (doc is None or doc.content is None): 
            return
        cnt = Utils.asObjectOrNull(doc.content, UnitextContainer)
        if (cnt is None): 
            return
        cr1 = 0
        cr2 = 0
        cra = 0
        for v in cnt.children: 
            if (isinstance(v, UnitextNewline)): 
                co = v.count
                if (co == 1): 
                    cr1 += 1
                elif (co == 2): 
                    cr2 += 1
                else: 
                    cra += 1
        if (cr2 > (((cr1 + cra)) * 3)): 
            cnt._correct(LocCorrTyp.MERGENEWLINES, None)
        lines = CorrLine.parse_list(cnt)
        cou = 0
        len0_ = 0
        nbsp_count = 0
        sp_count = 0
        for l_ in lines: 
            if (l_.is_pure_text): 
                for ch in l_.text: 
                    if (ch == ' '): 
                        sp_count += 1
                    elif (ch == (chr(0xA0))): 
                        nbsp_count += 1
            if ((l_.is_pure_text and l_.new_lines == 1) or l_.page_break_after): 
                cou += 1
                len0_ += l_.length
        if (replace_nbsp and nbsp_count > 100 and nbsp_count > (sp_count * 2)): 
            doc.content._correct(LocCorrTyp.NPSP2SP, None)
            for s in doc.sections: 
                for it in s.items: 
                    if (it.content is not None): 
                        it.content._correct(LocCorrTyp.NPSP2SP, None)
        if (cou == 0): 
            return
        len0_ = math.floor(len0_ / cou)
        if (cou < 3): 
            return
        if ((len0_ < UnitextCorrHelper.__min_line_len) or len0_ > UnitextCorrHelper.__max_line_len): 
            return
        min_len = math.floor((0.80 * (len0_)))
        max_len = math.floor((1.20 * (len0_)))
        i = 0
        first_pass678 = True
        while True:
            if first_pass678: first_pass678 = False
            else: i += 1
            if (not (i < (len(lines) - 1))): break
            l1 = lines[i]
            l2 = lines[i + 1]
            if (not l1.is_pure_text or not l2.is_pure_text): 
                continue
            if (l1.length < min_len): 
                continue
            if (l1.can_followed(l2)): 
                l2.merge = True
        changed = False
        for i in range(len(lines) - 1, 0, -1):
            if (lines[i].merge): 
                if (lines[i - 1].page_break_after): 
                    continue
                i0 = lines[i - 1].last_ind + 1
                i1 = lines[i].first_ind - 1
                if (i0 <= i1): 
                    changed = True
                    if (i0 < i1): 
                        del cnt.children[i0 + 1:i0 + 1+i1 - i0]
                    cnt.children[i0] = (UnitextPlaintext._new51(" "))
        if (changed): 
            doc.optimize(False, None)
    
    @staticmethod
    def restore_text_footnotes(doc : 'UnitextDocument') -> None:
        if (doc is None or doc.content is None): 
            return
        if (isinstance(doc.content, UnitextTable)): 
            UnitextCorrHelper.__restore_text_footnotes_in_table(Utils.asObjectOrNull(doc.content, UnitextTable))
            return
        cnt = Utils.asObjectOrNull(doc.content, UnitextContainer)
        if (cnt is None): 
            return
        fcl = list()
        num_start = 1
        i = 0
        first_pass679 = True
        while True:
            if first_pass679: first_pass679 = False
            else: i += 1
            if (not (i < len(cnt.children))): break
            if (isinstance(cnt.children[i], UnitextTable)): 
                UnitextCorrHelper.__restore_text_footnotes_in_table(Utils.asObjectOrNull(cnt.children[i], UnitextTable))
                continue
            fc = CorrFootnoteContainer.try_parse(cnt.children, i, num_start)
            if (fc is None): 
                continue
            fcl.append(fc)
            if (len(fcl) == 19): 
                pass
            i = fc.end_ind
            num_start += len(fc.items)
        if (len(fcl) == 0): 
            return
        is_changed = False
        for i in range(len(fcl) - 1, -1, -1):
            ind0 = 0
            ind1 = fcl[i].begin_ind - 1
            if (i > 0): 
                ind0 = (fcl[i - 1].end_ind + 1)
            if (i == 8): 
                pass
            corr = False
            for k in range(2):
                j = ind0
                while j <= ind1: 
                    it = fcl[i].correct_item(cnt.children[j], k == 1)
                    if (it is not None): 
                        cnt.children[j] = it
                        corr = True
                    j += 1
                if (corr or fcl[i].typ != CorrFootnoteTyps.STARS): 
                    break
            if (corr): 
                is_changed = True
                del cnt.children[fcl[i].begin_ind:fcl[i].begin_ind+(fcl[i].end_ind + 1) - fcl[i].begin_ind]
                if (((fcl[i].begin_ind < len(cnt.children)) and (isinstance(cnt.children[fcl[i].begin_ind], UnitextNewline)) and fcl[i].begin_ind > 0) and (isinstance(cnt.children[fcl[i].begin_ind - 1], UnitextNewline))): 
                    del cnt.children[fcl[i].begin_ind]
        if (is_changed): 
            doc.optimize(False, None)
    
    @staticmethod
    def __restore_text_footnotes_in_table(tab : 'UnitextTable') -> None:
        is_changed = False
        r = 0
        while r < tab.rows_count: 
            c = 0
            first_pass680 = True
            while True:
                if first_pass680: first_pass680 = False
                else: c += 1
                if (not (c < tab.cols_count)): break
                cel = tab.get_cell(r, c)
                if (cel is None): 
                    continue
                if (cel.col_begin != c or cel.row_begin != r): 
                    continue
                if (cel.content is None): 
                    continue
                fn = CorrFootnoteContainer.try_parse1(cel.content)
                if (fn is None): 
                    continue
                cc = cel.col_begin
                first_pass681 = True
                while True:
                    if first_pass681: first_pass681 = False
                    else: cc += 1
                    if (not (cc <= cel.col_end)): break
                    cel0 = tab.get_cell(r - 1, cc)
                    if (cel0 is None): 
                        continue
                    if (cel0.content is None): 
                        continue
                    re = fn.correct_item(cel0.content, False)
                    if (re is None): 
                        continue
                    cel0.content = re
                    cel.content = (None)
                    is_changed = True
            r += 1
        if (is_changed): 
            tab.optimize(False, None)
    
    @staticmethod
    def restore_tables(doc : 'UnitextDocument') -> bool:
        cnt = Utils.asObjectOrNull(doc.content, UnitextContainer)
        if (cnt is not None): 
            return UnitextCorrHelper.__restore_tables(cnt)
        return False
    
    @staticmethod
    def __restore_tables(cnt : 'UnitextContainer') -> bool:
        if (cnt is None): 
            return False
        ret = False
        for ch in cnt.children: 
            if (isinstance(ch, UnitextContainer)): 
                if (UnitextCorrHelper.__restore_tables(Utils.asObjectOrNull(ch, UnitextContainer))): 
                    ret = True
        lines = CorrLine.parse_list(cnt)
        tabs = list()
        i = 0
        while i < len(lines): 
            ii = 0
            wrapii344 = RefOutArgWrapper(0)
            tab = CorrTable.try_parse(lines, i, wrapii344)
            ii = wrapii344.value
            if (tab is not None): 
                tabs.append(tab)
                i = tab.end_ind
            else: 
                i = ii
            i += 1
        if (len(tabs) == 0): 
            return ret
        for i in range(len(tabs) - 1, -1, -1):
            i0 = lines[tabs[i].begin_ind].first_ind
            i1 = lines[tabs[i].end_ind].last_ind
            if (i0 < i1): 
                del cnt.children[i0 + 1:i0 + 1+i1 - i0]
                cnt.children[i0] = (tabs[i].result)
        if (cnt.typ == UnitextContainerType.MONOSPACE): 
            cnt.typ = UnitextContainerType.UNDEFINED
        return True
    
    @staticmethod
    def _corr_nbsp(text : str) -> str:
        if (text.find(chr(0xA0)) < 0): 
            return text
        return text.replace(chr(0xA0), ' ')