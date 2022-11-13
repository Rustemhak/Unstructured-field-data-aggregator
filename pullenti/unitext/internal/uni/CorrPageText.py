# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

class CorrPageText:
    
    def remove_head_text(self) -> None:
        if (Utils.isNullOrEmpty(self.head_text)): 
            return
        if (self.__m_top): 
            self.text = (self.head_text + "\r\n" + ((Utils.ifNotNull(self.text, ""))))
        else: 
            self.text = (((Utils.ifNotNull(self.text, ""))) + "\r\n" + self.head_text)
    
    def __str__(self) -> str:
        return "N={0} '{1}'".format(self.number, Utils.ifNotNull(self.head_text, ""))
    
    def is_number_dist1(self, next0_ : 'CorrPageText') -> bool:
        if (next0_.number == 0 or self.number == 0): 
            return False
        if (next0_.number == (self.number + 1)): 
            return True
        if (self.number2 > 0 and next0_.number == (self.number2 + 1)): 
            return True
        if (next0_.number2 > 0 and next0_.number2 == (self.number + 1)): 
            return True
        if (next0_.number2 > 0 and self.number2 > 0 and next0_.number2 == (self.number2 + 1)): 
            return True
        return False
    
    def __init__(self, txt : str, top : bool) -> None:
        self.number = 0
        self.number2 = 0
        self.head_text = None;
        self.text = None;
        self.i0 = 0
        self.i1 = 0
        self.corr = False
        self.__m_top = False
        self.__m_top = top
        if (txt is None): 
            txt = ""
        i0_ = 0
        i1_ = 0
        i = 0
        if (top): 
            i0_ = 0
            i1_ = i0_
            while i1_ < len(txt): 
                if ((ord(txt[i1_])) == 0xD or (ord(txt[i1_])) == 0xA): 
                    break
                i1_ += 1
            if (i1_ > i0_): 
                self.head_text = txt[0:0+i1_].strip()
                if (i1_ < len(txt)): 
                    self.text = txt[i1_:].strip()
                else: 
                    self.text = ""
            else: 
                self.text = txt
        else: 
            txt = txt.strip()
            i1_ = (len(txt) - 1)
            for i0_ in range(i1_, -1, -1):
                if ((ord(txt[i0_])) == 0xD or (ord(txt[i0_])) == 0xA): 
                    break
            else: i0_ = -1
            if (i1_ > i0_): 
                if (i0_ < 0): 
                    self.head_text = txt
                    self.text = ""
                else: 
                    self.head_text = txt[i0_ + 1:].strip()
                    self.text = txt[0:0+i0_].strip()
            else: 
                self.text = txt
        if (not Utils.isNullOrEmpty(self.head_text) and str.isdigit(self.head_text[0])): 
            i = 0
            while i < len(self.head_text): 
                if (not str.isdigit(self.head_text[i])): 
                    break
                i += 1
            if (i == len(self.head_text) or self.head_text[i] == ' '): 
                num = 0
                wrapnum320 = RefOutArgWrapper(0)
                inoutres321 = Utils.tryParseInt(self.head_text[0:0+i], wrapnum320)
                num = wrapnum320.value
                if (inoutres321): 
                    self.number = num
                    self.head_text = self.head_text[i:].strip()
        if (not Utils.isNullOrEmpty(self.head_text) and str.isdigit(self.head_text[len(self.head_text) - 1])): 
            while True:
                for i in range(len(self.head_text) - 1, -1, -1):
                    if (not str.isdigit(self.head_text[i])): 
                        break
                else: i = -1
                if ((i < 0) or self.head_text[i] == ' '): 
                    num = 0
                    wrapnum322 = RefOutArgWrapper(0)
                    inoutres323 = Utils.tryParseInt(self.head_text[i + 1:], wrapnum322)
                    num = wrapnum322.value
                    if (inoutres323): 
                        if (self.number > 0): 
                            self.number2 = num
                        else: 
                            self.number = num
                        self.head_text = self.head_text[0:0+i + 1].strip()
                        if (Utils.endsWithString(self.head_text, "СТР", True)): 
                            self.head_text = self.head_text[0:0+len(self.head_text) - 3].strip()
                        if (Utils.endsWithString(self.head_text, "СТР.", True)): 
                            self.head_text = self.head_text[0:0+len(self.head_text) - 4].strip()
                        from0_ = None
                        if (Utils.endsWithString(self.head_text, "ИЗ", True)): 
                            from0_ = self.head_text[0:0+len(self.head_text) - 2].strip()
                        elif (self.head_text.endswith("/") or self.head_text.endswith("\\")): 
                            from0_ = self.head_text[0:0+len(self.head_text) - 1].strip()
                        if (from0_ is not None and len(from0_) > 0 and str.isdigit(from0_[len(from0_) - 1])): 
                            self.head_text = from0_
                            self.number = 0
                            continue
                break
        if (top and not Utils.isNullOrEmpty(self.text) and str.isdigit(self.text[0])): 
            i = 0
            while i < len(self.text): 
                if (not str.isdigit(self.text[i])): 
                    break
                i += 1
            if (i >= len(self.text) or self.text[i] == '\r' or self.text[i] == '\n'): 
                num = 0
                wrapnum324 = RefOutArgWrapper(0)
                inoutres325 = Utils.tryParseInt(self.text[0:0+i], wrapnum324)
                num = wrapnum324.value
                if (inoutres325): 
                    self.number = num
                    if (i >= len(self.text)): 
                        self.text = ""
                    else: 
                        self.text = self.text[i:].strip()
        if (not top and not Utils.isNullOrEmpty(self.text) and str.isdigit(self.text[len(self.text) - 1])): 
            for i in range(len(self.text) - 1, -1, -1):
                if (not str.isdigit(self.text[i])): 
                    break
            else: i = -1
            if ((i < 0) or self.text[i] == '\r' or self.text[i] == '\n'): 
                num = 0
                wrapnum326 = RefOutArgWrapper(0)
                inoutres327 = Utils.tryParseInt(self.text[i + 1:], wrapnum326)
                num = wrapnum326.value
                if (inoutres327): 
                    self.number = num
                    if (i <= 0): 
                        self.text = ""
                    else: 
                        self.text = self.text[0:0+i].strip()
        if (Utils.isNullOrEmpty(self.head_text)): 
            self.head_text = (None)
    
    @staticmethod
    def process(pts : typing.List['CorrPageText']) -> str:
        cou = 0
        i = 0
        for p in pts: 
            p.corr = False
        res = io.StringIO()
        i = 1
        while i < (len(pts) - 1): 
            if (pts[i - 1].number > 0 and ((pts[i].number == 0 or pts[i].number != (pts[i - 1].number + 1)))): 
                j = 0
                ok1 = False
                ok2 = False
                err = 0
                j = (i + 1)
                while j < len(pts): 
                    if (pts[j].number > 0): 
                        if (pts[j].number == (pts[i - 1].number + (((j - i) + 1)))): 
                            ok1 = True
                            break
                        if (((j + 2) < len(pts)) and pts[j + 1].number == (pts[j].number + 1) and pts[j + 2].number == (pts[j].number + 2)): 
                            ok2 = True
                            break
                        err += 1
                        if (err > 10): 
                            break
                    j += 1
                if (ok1 or ok2): 
                    k = i
                    while k < j: 
                        pts[k].number = 0
                        k += 1
            i += 1
        no_corr_first = False
        if (len(pts) > 0 and pts[0].number > 1900): 
            pts[0].number = 0
            no_corr_first = True
        if (len(pts) > 2): 
            if (pts[0].number != 1 and pts[1].number > 0 and pts[2].number == (pts[1].number + 1)): 
                if (pts[0].number != (pts[1].number - 1)): 
                    pts[0].number = (pts[1].number - 1)
                    no_corr_first = True
        first_page = 0
        if (len(pts) > 4 and pts[0].number == 0): 
            i = 0
            while i < (len(pts) - 5): 
                if (pts[i].number != 0): 
                    ok1 = True
                    j = i + 1
                    while (j < len(pts)) and (j < (i + 4)): 
                        if (not pts[j].is_number_dist1(pts[j + 1])): 
                            ok1 = False
                            break
                        j += 1
                    if (ok1): 
                        first_page = i
                        i -= 1
                        while i >= 0: 
                            pts[i].number = (pts[i + 1].number - 1)
                            i -= 1
                    break
                i += 1
        errcou = 0
        i = 0
        first_pass666 = True
        while True:
            if first_pass666: first_pass666 = False
            else: i += 1
            if (not (i < (len(pts) - 1))): break
            if (pts[i + 1].number <= 0): 
                if ((i + 1) < len(pts)): 
                    continue
                errcou += 1
                continue
            if (pts[i].number <= 0): 
                if (i <= first_page): 
                    continue
                errcou += 1
                continue
            if (pts[i].is_number_dist1(pts[i + 1])): 
                cou += 1
            elif (i == 0): 
                pass
            else: 
                errcou += 1
        ok = False
        if (cou == 0): 
            if ((len(pts) == 3 and pts[1].number == 2 and pts[0].number == 0) and pts[2].number == 0): 
                ok = True
            elif (len(pts) == 2 and pts[1].number == 2 and ((pts[0].number == 1 or pts[0].number == 0))): 
                ok = True
            else: 
                ok = False
        elif (errcou == 0): 
            ok = True
        colstat = dict()
        i = 1
        while i < len(pts): 
            if (pts[i].head_text is not None): 
                if (pts[i].head_text in colstat): 
                    colstat[pts[i].head_text] += 1
                else: 
                    colstat[pts[i].head_text] = 1
            i += 1
        lev = math.floor(len(pts) / 2)
        if (lev < 2): 
            lev = 2
        i = 1
        first_pass667 = True
        while True:
            if first_pass667: first_pass667 = False
            else: i += 1
            if (not (i < len(pts))): break
            h = pts[i].head_text
            if (h is None): 
                continue
            c = colstat[h]
            if (c >= lev): 
                pts[i].corr = True
            else: 
                pts[i].remove_head_text()
        for kp in colstat.items(): 
            if (kp[1] >= lev and len(kp[0]) > 5): 
                if (res.tell() > 0): 
                    print("\r\n", end="", file=res)
                print(kp[0], end="", file=res)
        if (cou > (errcou * 3)): 
            for p in pts: 
                if (p.number > 0): 
                    if (no_corr_first and p == pts[0]): 
                        continue
                    if (not p.corr): 
                        p.remove_head_text()
                    p.corr = True
        return (None if res.tell() == 0 else Utils.toStringStringIO(res))
    
    @staticmethod
    def _new340(_arg1 : str, _arg2 : bool, _arg3 : int, _arg4 : int) -> 'CorrPageText':
        res = CorrPageText(_arg1, _arg2)
        res.i0 = _arg3
        res.i1 = _arg4
        return res