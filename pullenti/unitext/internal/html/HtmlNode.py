# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
from pullenti.unitext.internal.html.HtmlTag import HtmlTag

class HtmlNode:
    
    def __init__(self) -> None:
        self.tag_name = None;
        self.attrs = None;
        self.text = None;
        self.whitespace_preserve = False
        self.parent = None;
        self.children = list()
        self.source_html_position = 0
        self.source_html_length = 0
        self.source_html_end_position = 0
        self.misc = None;
        self.plain_text_begin = 0
        self.plain_text_end = 0
    
    @property
    def total_children(self) -> int:
        res = len(self.children)
        for ch in self.children: 
            res += ch.total_children
        return res
    
    def get_html(self, res : io.StringIO) -> None:
        tag = HtmlTag.find_tag(self.tag_name)
        if (tag is not None and ((tag.is_block or tag.is_table)) and res.tell() > 0): 
            print("\r\n", end="", file=res)
        if (self.tag_name is not None): 
            print("<{0}".format(self.tag_name.lower()), end="", file=res, flush=True)
            if (self.attrs is not None): 
                for kp in self.attrs.items(): 
                    print(" {0}=\"".format(kp[0].lower()), end="", file=res, flush=True)
                    MiscHelper.correct_html_value(res, kp[1], True, False)
                    print("\"", end="", file=res)
            if (Utils.isNullOrEmpty(self.text) and len(self.children) == 0): 
                print("/>", end="", file=res)
                return
            print(">", end="", file=res)
        if (len(self.children) > 0): 
            for ch in self.children: 
                ch.get_html(res)
        elif (not Utils.isNullOrEmpty(self.text)): 
            MiscHelper.correct_html_value(res, self.text, False, False)
        if (self.tag_name is not None): 
            print("</{0}>".format(self.tag_name.lower()), end="", file=res, flush=True)
    
    def get_plaintext(self, pars : 'GetPlaintextParam') -> str:
        res = io.StringIO()
        self._get_full_text(res, pars, None)
        return Utils.toStringStringIO(res)
    
    def _get_full_text(self, res : io.StringIO, pars : 'GetPlaintextParam', li_num_str : str=None) -> None:
        self.plain_text_begin = res.tell()
        self.plain_text_end = (self.plain_text_begin - 1)
        if ((self.tag_name == "SCRIPT" or self.tag_name == "STYLE" or self.tag_name == "META") or self.tag_name == "TITLE"): 
            return
        tag = HtmlTag.find_tag(self.tag_name)
        is_block = False
        if (tag is not None and ((tag.is_block or tag.is_table))): 
            is_block = True
        is_tab = tag is not None and tag.name == "TABLE"
        is_td = tag is not None and ((tag.name == "TD" or tag.name == "TH"))
        is_tr = tag is not None and tag.name == "TR"
        is_li = tag is not None and tag.name == "LI"
        is_ol = tag is not None and tag.name == "OL"
        if (tag is not None and tag.name == "BR"): 
            if (self.whitespace_preserve): 
                print(' ', end="", file=res)
                self.plain_text_end = (res.tell() - 1)
                return
            print(("\r\n" if pars is None else pars.new_line), end="", file=res)
            self.plain_text_end = (res.tell() - 1)
            return
        if (is_tab and pars is not None): 
            if (pars.table_start is not None): 
                print(pars.table_start, end="", file=res)
        if ((is_block and not is_td and not is_tr) and res.tell() > 0): 
            print(("\r\n" if pars is None else pars.new_line), end="", file=res)
        if (is_li): 
            if (li_num_str is not None): 
                print(li_num_str, end="", file=res)
            else: 
                print('', end="", file=res)
        li_num = 0
        li_typ = None
        if (is_ol): 
            wrapli_num3 = RefOutArgWrapper(0)
            inoutres4 = Utils.tryParseInt(Utils.ifNotNull(self.get_attribute("START"), ""), wrapli_num3)
            li_num = wrapli_num3.value
            if (not inoutres4): 
                li_num = 1
            li_typ = (Utils.ifNotNull(self.get_attribute("TYPE"), "1"))
        if (not Utils.isNullOrEmpty(self.text)): 
            print(self.text, end="", file=res)
        elif (len(self.children) == 1): 
            self.children[0]._get_full_text(res, pars, HtmlNode._get_li_num(li_num, li_typ))
        else: 
            first = True
            i = 0
            while i < len(self.children): 
                ch = self.children[i]
                hn = Utils.asObjectOrNull(ch, HtmlNode)
                if (first): 
                    first = False
                elif (not ch.whitespace_preserve and not is_tr): 
                    if (ch.tag_name is None or Utils.compareStrings(Utils.ifNotNull(ch.tag_name, ""), "SPAN", True) == 0): 
                        pass
                    elif (i > 0 and ((self.children[i - 1].tag_name is None or Utils.compareStrings(Utils.ifNotNull(self.children[i - 1].tag_name, ""), "SPAN", True) == 0))): 
                        pass
                    else: 
                        print(' ', end="", file=res)
                hn._get_full_text(res, pars, HtmlNode._get_li_num(li_num, li_typ))
                if (li_num > 0 and hn.tag_name == "LI"): 
                    li_num += 1
                i += 1
        if (is_td): 
            if (self.get_attribute("ROWSPAN") is not None): 
                span = 0
                wrapspan5 = RefOutArgWrapper(0)
                inoutres6 = Utils.tryParseInt(self.get_attribute("ROWSPAN"), wrapspan5)
                span = wrapspan5.value
                if (inoutres6): 
                    while span > 1: 
                        print(pars.page_break, end="", file=res)
                        span -= 1
            if (self.get_attribute("COLSPAN") is not None): 
                span = 0
                wrapspan7 = RefOutArgWrapper(0)
                inoutres8 = Utils.tryParseInt(self.get_attribute("COLSPAN"), wrapspan7)
                span = wrapspan7.value
                if (inoutres8): 
                    while span > 1: 
                        print(pars.tab, end="", file=res)
                        span -= 1
            print(pars.table_cell_end, end="", file=res)
        elif (is_tr): 
            print(Utils.ifNotNull(pars.table_row_end, pars.new_line), end="", file=res)
        elif (is_tab): 
            pass
        if (is_tab and pars is not None): 
            if (pars.table_end is not None): 
                print(pars.table_end, end="", file=res)
        self.plain_text_end = (res.tell() - 1)
    
    @staticmethod
    def __trim_tab_text(txt : str) -> str:
        if (Utils.isNullOrEmpty(txt)): 
            return ""
        i = 0
        for i in range(len(txt) - 1, -1, -1):
            if (txt[i] == ' ' or (ord(txt[i])) == 0xD or (ord(txt[i])) == 0xA): 
                pass
            else: 
                break
        else: i = -1
        if (i < 0): 
            return ""
        if (i < (len(txt) - 1)): 
            txt = txt[0:0+i + 1]
        i = 0
        while i < len(txt): 
            if (txt[i] == ' ' or (ord(txt[i])) == 0xD or (ord(txt[i])) == 0xA): 
                pass
            else: 
                break
            i += 1
        if (i > 0): 
            txt = txt[i:]
        return txt
    
    @staticmethod
    def _get_li_num(num : int, typ : str) -> str:
        if (num <= 0): 
            return None
        ty = ('1' if Utils.isNullOrEmpty(typ) else typ[0])
        if (ty == '1'): 
            return "{0}. ".format(num)
        if (ty == 'A'): 
            return "{0}) ".format(chr(((ord('A')) + ((num - 1)))))
        if (ty == 'a'): 
            return "{0}) ".format(chr(((ord('a')) + ((num - 1)))))
        if (ty == 'i' and ((num - 1) < len(UnitextHelper._m_romans))): 
            return "{0}. ".format(UnitextHelper._m_romans[num - 1].lower())
        if (ty == 'I' and ((num - 1) < len(UnitextHelper._m_romans))): 
            return "{0}. ".format(UnitextHelper._m_romans[num - 1])
        return "{0}. ".format(num)
    
    def _correct_rus_texts(self, corr : int=0) -> None:
        attr = self.get_attribute("STYLE")
        if (attr is not None): 
            if ("small-caps" in attr): 
                corr = 1
        for ch in self.children: 
            ch._correct_rus_texts(corr)
        if (corr > 0 and not Utils.isNullOrEmpty(self.text)): 
            self.text = self.text.upper()
    
    def get_attribute(self, name : str) -> str:
        if (self.attrs is None): 
            return None
        if (name in self.attrs): 
            return self.attrs[name]
        return None
    
    def get_style_value(self, name : str) -> str:
        if (self.attrs is None or name is None): 
            return None
        val = None
        wrapval9 = RefOutArgWrapper(None)
        inoutres10 = Utils.tryGetValue(self.attrs, "STYLE", wrapval9)
        val = wrapval9.value
        if (not inoutres10): 
            return None
        for vv in Utils.splitString(val, ';', False): 
            vvv = vv.strip()
            ii = vvv.find(':')
            if (ii < 0): 
                continue
            if (Utils.compareStrings(name, vvv[0:0+ii].strip(), True) == 0): 
                return vv[ii + 1:].strip()
        return None
    
    def __str__(self) -> str:
        if (self.tag_name is None): 
            if (self.text is None): 
                return ""
            return self.text
        tmp = io.StringIO()
        print("<{0}".format(self.tag_name), end="", file=tmp, flush=True)
        if (self.attrs is not None): 
            for kp in self.attrs.items(): 
                print(" {0}='{1}'".format(kp[0], Utils.ifNotNull(kp[1], "")), end="", file=tmp, flush=True)
        if (self.text is not None): 
            print(">{0}</{1}>".format(self.text, self.tag_name), end="", file=tmp, flush=True)
        elif (len(self.children) > 0): 
            print(">...</{0}>".format(self.tag_name), end="", file=tmp, flush=True)
        else: 
            print("/>", end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    
    @property
    def has_text(self) -> bool:
        if (self.text is not None): 
            i = 0
            while i < len(self.text): 
                if (not Utils.isWhitespace(self.text[i])): 
                    return True
                i += 1
        j = 0
        while j < len(self.children): 
            if (self.children[j].has_text): 
                return True
            j += 1
        return False
    
    def has_tag(self, tag : str) -> bool:
        if (self.tag_name is not None and Utils.compareStrings(self.tag_name, tag, True) == 0): 
            return True
        for ch in self.children: 
            if (ch.has_tag(tag)): 
                return True
        return False
    
    def has_block_tag(self) -> bool:
        if (self.tag_name is not None): 
            ti = HtmlTag.find_tag(self.tag_name)
            if (ti is not None and ti.is_block): 
                return True
        for ch in self.children: 
            if (ch.has_block_tag()): 
                return True
        return False
    
    def remove(self) -> None:
        if (self.parent is None): 
            return
        i = Utils.indexOfList(self.parent.children, self, 0)
        if (i < 0): 
            return
        self.parent.children.remove(self)
        if (len(self.children) > 0): 
            self.parent.children[i:i] = self.children
            self.children.clear()
        self.parent = (None)
    
    def find_subnode(self, tag_name_ : str, attr_name : str, attr_value : str) -> 'HtmlNode':
        if (attr_name is not None): 
            attr_name = attr_name.upper()
        if (tag_name_ is not None): 
            tag_name_ = tag_name_.upper()
        return self.__find_subnode(tag_name_, attr_name, attr_value)
    
    def __find_subnode(self, tag_name_ : str, attr_name : str, attr_value : str) -> 'HtmlNode':
        if (tag_name_ is not None and self.tag_name == tag_name_): 
            if (attr_name is not None): 
                val = self.get_attribute(attr_name)
                if (val is not None): 
                    if (attr_value is None): 
                        return self
                    if (Utils.compareStrings(attr_value, val, True) == 0): 
                        return self
            else: 
                return self
        for ch in self.children: 
            res = ch.__find_subnode(tag_name_, attr_name, attr_value)
            if (res is not None): 
                return res
        return None
    
    def implantate_node(self, begin_char : int, end_char : int, tag_name_ : str) -> 'HtmlNode':
        if (begin_char >= self.plain_text_end or (end_char < self.plain_text_begin)): 
            return None
        ind = -1
        if (self.parent is not None): 
            ind = Utils.indexOfList(self.parent.children, self, 0)
        if (len(self.children) == 0): 
            if (Utils.isNullOrEmpty(self.text)): 
                return None
            if (begin_char < self.plain_text_begin): 
                begin_char = self.plain_text_begin
            if (end_char > self.plain_text_end): 
                end_char = self.plain_text_end
            if (begin_char == self.plain_text_begin and end_char == self.plain_text_end): 
                res = HtmlNode._new11(tag_name_, begin_char, end_char)
                if (ind >= 0): 
                    self.parent.children[ind] = res
                    res.parent = self.parent
                    res.children.append(self)
                    self.parent = res
                    return res
                else: 
                    txt = HtmlNode._new12(begin_char, end_char)
                    txt.text = self.text
                    self.text = (None)
                    res.children.append(txt)
                    txt.parent = res
                    self.children.append(res)
                    res.parent = self
                    return res
            res1 = HtmlNode._new11(tag_name_, begin_char, end_char)
            if (begin_char > self.plain_text_begin): 
                d = begin_char - self.plain_text_begin
                txt = HtmlNode._new14(begin_char - 1)
                txt.plain_text_begin = self.plain_text_begin
                txt.text = self.text[0:0+d]
                self.children.append(txt)
                txt.parent = self
                self.text = self.text[d:]
            if (begin_char <= end_char): 
                txt = HtmlNode._new12(begin_char, end_char)
                txt.text = self.text
                if (end_char < self.plain_text_end): 
                    txt.text = self.text[0:0+(end_char - begin_char) + 1]
                    self.text = self.text[(end_char - begin_char) + 1:]
                else: 
                    self.text = ""
                self.children.append(res1)
                res1.parent = self
                res1.children.append(txt)
                txt.parent = res1
            if (end_char < self.plain_text_end): 
                txt = HtmlNode._new16(end_char + 1)
                txt.plain_text_end = self.plain_text_end
                txt.text = self.text
                self.children.append(txt)
                txt.parent = self
                self.text = ""
            self.text = (None)
            return res1
        if (len(self.children) == 0): 
            return None
        i = 0
        while i < len(self.children): 
            if (self.children[i].plain_text_begin <= begin_char and begin_char <= self.children[i].plain_text_end): 
                j = i
                while j < len(self.children): 
                    tag = self.children[j].tag_name
                    if ((tag == "TD" or tag == "TR" or tag == "TH") or ((self.children[j].plain_text_begin <= end_char and end_char <= self.children[j].plain_text_end))): 
                        if (i == j): 
                            res1 = self.children[i].implantate_node(begin_char, end_char, tag_name_)
                            if (res1 is not None): 
                                return res1
                        head = None
                        tail = None
                        ch = self.children[i]
                        if (begin_char > ch.plain_text_begin and ch.text is not None): 
                            head = HtmlNode._new11(ch.tag_name, ch.plain_text_begin, begin_char - 1)
                            head.parent = self.parent
                            head.text = ch.text[0:0+begin_char - ch.plain_text_begin]
                            ch.text = ch.text[begin_char - ch.plain_text_begin:]
                            ch.plain_text_begin = begin_char
                        if ((end_char < self.children[j].plain_text_end) and self.children[j].text is not None): 
                            ch1 = self.children[j]
                            tail = HtmlNode._new11(ch1.tag_name, end_char + 1, ch1.plain_text_end)
                            tail.parent = self.parent
                            tail.text = ch1.text[end_char - ch1.plain_text_begin:]
                            ch1.text = ch1.text[0:0+end_char - ch1.plain_text_begin]
                            ch1.plain_text_end = end_char
                        begin_char = ch.plain_text_begin
                        end_char = self.children[j].plain_text_end
                        res = HtmlNode._new11(tag_name_, begin_char, end_char)
                        if (((tag == "TD" or tag == "TR" or tag == "TH")) and i == j): 
                            for chh in ch.children: 
                                res.children.append(chh)
                                ch.parent = res
                            self.children[i].children.clear()
                            self.children[i].children.append(res)
                            res.parent = self.children[i]
                            return res
                        k = i
                        while k <= j: 
                            res.children.append(self.children[k])
                            self.children[k].parent = res
                            k += 1
                        del self.children[i:i+(j + 1) - i]
                        if (tail is not None): 
                            self.children.insert(i, tail)
                        self.children.insert(i, res)
                        res.parent = self
                        if (head is not None): 
                            self.children.insert(i, head)
                        return res
                    j += 1
            i += 1
        return None
    
    @staticmethod
    def _new1(_arg1 : str) -> 'HtmlNode':
        res = HtmlNode()
        res.tag_name = _arg1
        return res
    
    @staticmethod
    def _new11(_arg1 : str, _arg2 : int, _arg3 : int) -> 'HtmlNode':
        res = HtmlNode()
        res.tag_name = _arg1
        res.plain_text_begin = _arg2
        res.plain_text_end = _arg3
        return res
    
    @staticmethod
    def _new12(_arg1 : int, _arg2 : int) -> 'HtmlNode':
        res = HtmlNode()
        res.plain_text_begin = _arg1
        res.plain_text_end = _arg2
        return res
    
    @staticmethod
    def _new14(_arg1 : int) -> 'HtmlNode':
        res = HtmlNode()
        res.plain_text_end = _arg1
        return res
    
    @staticmethod
    def _new16(_arg1 : int) -> 'HtmlNode':
        res = HtmlNode()
        res.plain_text_begin = _arg1
        return res