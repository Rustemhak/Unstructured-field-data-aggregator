# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
import io
import xml.etree
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextStyledFragmentType import UnitextStyledFragmentType
from pullenti.unitext.internal.uni.LocCorrTyp import LocCorrTyp
from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.unitext.UnitextItem import UnitextItem

class UnitextContainer(UnitextItem):
    """ Контейнер других элементов
    
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.children = list()
        self.typ = UnitextContainerType.UNDEFINED
        self.data = None;
        self.user_data = None;
        self.html_style = None;
        self.__m_is_inline = -1
    
    @staticmethod
    def __get_box_chars(it : 'UnitextItem') -> int:
        from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
        pl = Utils.asObjectOrNull(it, UnitextPlaintext)
        if (pl is None): 
            return 0
        co = 0
        for ch in pl.text: 
            if ((ord(ch)) >= 0x2500 and (ord(ch)) <= 0x257F): 
                co += 1
        return co
    
    @staticmethod
    def __get_underline_chars(it : 'UnitextItem') -> int:
        from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
        pl = Utils.asObjectOrNull(it, UnitextPlaintext)
        if (pl is None): 
            return 0
        co = 0
        for ch in pl.text: 
            if (ch == '_' or ch == '_'): 
                co += 1
        return co
    
    def optimize(self, is_container : bool, pars : 'CreateDocumentParam') -> 'UnitextItem':
        from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
        from pullenti.unitext.UnitextDocblock import UnitextDocblock
        from pullenti.unitext.UnitextFootnote import UnitextFootnote
        from pullenti.unitext.UnitextNewline import UnitextNewline
        from pullenti.unitext.UnitextPagebreak import UnitextPagebreak
        from pullenti.unitext.UnitextTable import UnitextTable
        if (self.children is None or len(self.children) == 0): 
            if (self.typ == UnitextContainerType.SHAPE): 
                return self
            return None
        i = 0
        while i < len(self.children): 
            self.children[i].parent = (self)
            ch = self.children[i].optimize(False, pars)
            if (ch is None): 
                del self.children[i]
                i -= 1
            else: 
                self.children[i] = ch
            i += 1
        if (len(self.children) >= 30): 
            pass
        for i in range(len(self.children) - 1, -1, -1):
            cnt = Utils.asObjectOrNull(self.children[i], UnitextContainer)
            if (cnt is None): 
                continue
            if (i == 0): 
                pass
            if (cnt.typ != UnitextContainerType.UNDEFINED): 
                continue
            if (cnt.page_section_id is not None and self.page_section_id is not None and cnt.page_section_id != self.page_section_id): 
                continue
            del self.children[i]
            for chh in cnt.children: 
                if (chh.page_section_id is None): 
                    chh.page_section_id = cnt.page_section_id
            self.children[i:i] = cnt.children
        i = 0
        first_pass704 = True
        while True:
            if first_pass704: first_pass704 = False
            else: i += 1
            if (not (i < (len(self.children) - 1))): break
            ch = self.children[i]
            ch1 = self.children[i + 1]
            if ((isinstance(ch, UnitextPagebreak)) and (isinstance(ch1, UnitextPagebreak))): 
                del self.children[i + 1]
                i -= 1
                continue
            if (isinstance(ch, UnitextNewline)): 
                if (isinstance(ch1, UnitextNewline)): 
                    ii = 0
                    ii = (i + 1)
                    while ii < len(self.children): 
                        if (not (isinstance(self.children[ii], UnitextNewline))): 
                            break
                        else: 
                            ch.count += self.children[ii].count
                        ii += 1
                    del self.children[i + 1:i + 1+ii - i - 1]
                    i -= 1
                elif (isinstance(ch1, UnitextPagebreak)): 
                    del self.children[i]
                    i -= 1
                continue
            if ((isinstance(ch, UnitextTable)) and not (isinstance(ch1, UnitextNewline)) and not (isinstance(ch1, UnitextPagebreak))): 
                self.children.insert(i + 1, UnitextNewline())
                continue
            if ((isinstance(ch, UnitextPlaintext)) and ch.is_whitespaces): 
                if ((isinstance(ch1, UnitextNewline)) or (isinstance(ch1, UnitextPagebreak))): 
                    del self.children[i]
                    i -= 1
                    if (i >= 0): 
                        i -= 1
                    continue
            if ((isinstance(ch, UnitextContainer)) and not ch.is_inline and (isinstance(ch1, UnitextNewline))): 
                ch.children.append(ch1)
                del self.children[i + 1]
                i -= 1
                continue
            if ((isinstance(ch, UnitextContainer)) and (isinstance(ch1, UnitextContainer))): 
                cnt = Utils.asObjectOrNull(ch, UnitextContainer)
                cnt1 = Utils.asObjectOrNull(ch1, UnitextContainer)
                if (cnt.typ == cnt1.typ and cnt.page_section_id == cnt1.page_section_id): 
                    for chh in cnt1.children: 
                        if (chh.page_section_id is None): 
                            chh.page_section_id = cnt1.page_section_id
                    cnt.children.extend(cnt1.children)
                    del self.children[i + 1]
                    i -= 1
                    continue
            if ((isinstance(ch, UnitextPlaintext)) and (isinstance(ch1, UnitextPlaintext))): 
                if (ch.typ == ch1.typ): 
                    if (ch.page_section != ch1.page_section): 
                        continue
                    ch._merge_with(Utils.asObjectOrNull(ch1, UnitextPlaintext))
                    del self.children[i + 1]
                    i -= 1
                    continue
            if ((isinstance(ch, UnitextTable)) and (isinstance(ch1, UnitextTable)) and ch.page_section_id == ch1.page_section_id): 
                if (ch._try_append(Utils.asObjectOrNull(ch1, UnitextTable))): 
                    del self.children[i + 1]
                    i -= 1
                    continue
            if (((((i + 2) < len(self.children)) and (isinstance(ch, UnitextTable)) and (isinstance(self.children[i + 2], UnitextTable))) and (isinstance(ch1, UnitextNewline)) and (ch1.count < 3)) and ch._try_append(Utils.asObjectOrNull(self.children[i + 2], UnitextTable))): 
                del self.children[i + 1]
                del self.children[i + 1]
                i -= 1
                continue
            if ((isinstance(ch, UnitextPlaintext)) and (((isinstance(ch1, UnitextNewline)) or (isinstance(ch1, UnitextPagebreak)) or (isinstance(ch1, UnitextFootnote))))): 
                ch._correct(LocCorrTyp.TRIMEND, None)
        i = 0
        while i < (len(self.children) - 1): 
            if ((isinstance(self.children[i], UnitextDocblock)) and (((isinstance(self.children[i + 1], UnitextPagebreak)) or (isinstance(self.children[i + 1], UnitextNewline))))): 
                if (self.children[i]._append_child(self.children[i + 1])): 
                    del self.children[i + 1]
                    self.children[i].optimize(False, pars)
                    i -= 1
            i += 1
        if (is_container): 
            for i in range(len(self.children) - 1, -1, -1):
                if (self.children[i].is_whitespaces): 
                    del self.children[i]
                else: 
                    break
            i = 0
            while i < len(self.children): 
                if (self.children[i].is_whitespaces): 
                    del self.children[i]
                    i -= 1
                else: 
                    break
                i += 1
        i = 0
        first_pass705 = True
        while True:
            if first_pass705: first_pass705 = False
            else: i += 1
            if (not (i < len(self.children))): break
            co = UnitextContainer.__get_box_chars(self.children[i])
            if (co == 0): 
                continue
            i1 = i
            no = 1
            cou = 1
            j = i + 1
            first_pass706 = True
            while True:
                if first_pass706: first_pass706 = False
                else: j += 1
                if (not (j < len(self.children))): break
                if (self.children[j].is_whitespaces): 
                    continue
                co = UnitextContainer.__get_box_chars(self.children[j])
                if (co > 0): 
                    no = 1
                    i1 = j
                    cou += 1
                    if (cou > 3): 
                        no += 1
                    if (cou > 10): 
                        no += 1
                else: 
                    co = UnitextContainer.__get_underline_chars(self.children[j])
                    if (co > 10): 
                        no = 1
                        i1 = j
                        cou += 1
                        if (cou > 3): 
                            no += 1
                        if (cou > 10): 
                            no += 1
                    if (co > 3): 
                        cou += 1
                    else: 
                        no -= 1
                        if (no == 0): 
                            break
            while (i1 + 1) < len(self.children): 
                if (not self.children[i1 + 1].is_whitespaces and (UnitextContainer.__get_underline_chars(self.children[i1 + 1]) < 3)): 
                    break
                i1 += 1
            for j in range(i - 1, -1, -1):
                if (self.children[j].is_whitespaces): 
                    continue
                if (UnitextContainer.__get_underline_chars(self.children[j]) < 3): 
                    break
                i = j
            if (i == 0 and i1 == (len(self.children) - 1) and self.typ == UnitextContainerType.UNDEFINED): 
                self.typ = UnitextContainerType.MONOSPACE
                break
            cnt = UnitextContainer._new543(UnitextContainerType.MONOSPACE, self)
            j = i
            while j <= i1: 
                cnt.children.append(self.children[j])
                self.children[j].parent = (cnt)
                j += 1
            del self.children[i:i+(i1 - i) + 1]
            self.children.insert(i, cnt)
        if (len(self.children) == 0): 
            return None
        if (len(self.children) == 1): 
            if (not self.is_inline and self.children[0].is_inline): 
                return self
            if (isinstance(self.children[0], UnitextContainer)): 
                ch = Utils.asObjectOrNull(self.children[0], UnitextContainer)
                if (ch.typ == self.typ): 
                    if (self.children[0].page_section_id is None): 
                        self.children[0].page_section_id = self.page_section_id
                    if (self.id0_ is not None and self.children[0].id0_ is None): 
                        self.children[0].id0_ = self.id0_
                    return self.children[0]
                if (self.typ == UnitextContainerType.HEAD or self.typ == UnitextContainerType.TAIL): 
                    if (ch.typ == UnitextContainerType.UNDEFINED): 
                        if (self.page_section_id is None): 
                            self.page_section_id = self.children[0].page_section_id
                        self.children.clear()
                        self.children.extend(ch.children)
                    return self
            if (self.typ == UnitextContainerType.UNDEFINED): 
                if (self.children[0].page_section_id is None): 
                    self.children[0].page_section_id = self.page_section_id
                if (self.id0_ is not None and self.children[0].id0_ is None): 
                    self.children[0].id0_ = self.id0_
                return self.children[0]
        return self
    
    @property
    def _inner_tag(self) -> str:
        return "cnt"
    
    def clone(self) -> 'UnitextItem':
        res = UnitextContainer()
        res.__clone_from2(self)
        return res
    
    def __clone_from2(self, src : 'UnitextContainer') -> None:
        self._clone_from(src)
        self.typ = src.typ
        self.html_style = src.html_style
        self.data = src.data
        self.user_data = src.user_data
        self.__m_is_inline = src.__m_is_inline
        for ch in src.children: 
            self.children.append(ch.clone())
    
    def find_by_id(self, id0__ : str) -> 'UnitextItem':
        if (self.id0_ == id0__): 
            return self
        for ch in self.children: 
            res = ch.find_by_id(id0__)
            if (res is not None): 
                return res
        return None
    
    def get_child_index_of(self, it : 'UnitextItem') -> int:
        """ Получить индекс дочернего элемента из списка Children (работает быстро)
        
        Args:
            it(UnitextItem): исколмый элемент
        
        Returns:
            int: индекс или -1
        """
        if ((it.begin_char > 0 and len(self.children) > 20 and self.begin_char <= it.begin_char) and it.end_char <= self.end_char): 
            i = math.floor(len(self.children) / 2)
            d = math.floor(len(self.children) / 4)
            if (d == 0): 
                d = 1
            k = d + 2
            while k > 0:
                if (i >= len(self.children) or (i < 0)): 
                    break
                if (self.children[i] == it): 
                    return i
                if (self.children[i].begin_char < it.begin_char): 
                    i += d
                elif (self.children[i].end_char > it.begin_char): 
                    i -= d
                else: 
                    i += d
                d = math.floor(d / 2)
                if (d == 0): 
                    d = 1
                    k -= 1
        return Utils.indexOfList(self.children, it, 0)
    
    def __str__(self) -> str:
        res = "{0} {1} items".format(("Container" if self.typ == UnitextContainerType.UNDEFINED else Utils.enumToString(self.typ)), (0 if self.children is None else len(self.children)))
        if (self.html_title is not None): 
            res = "{0} {1}".format(res, self.html_title)
        return res
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
        if (self.children is None or len(self.children) == 0): 
            pass
        elif (self.typ == UnitextContainerType.SHAPE and pars is not None and pars.ignore_shapes): 
            pass
        else: 
            if (self.typ == UnitextContainerType.SHAPE and pars is not None and res.tell() > 0): 
                ch = Utils.getCharAtStringIO(res, res.tell() - 1)
                if (str.isalnum(ch)): 
                    print(pars.new_line, end="", file=res)
            for ch in self.children: 
                ch.get_plaintext(res, Utils.ifNotNull(pars, UnitextItem._m_def_params))
                if (pars is not None and pars.max_text_length > 0 and res.tell() > pars.max_text_length): 
                    break
            if (self.typ == UnitextContainerType.SHAPE and pars is not None): 
                print(pars.new_line, end="", file=res)
        if (pars is not None and pars.set_positions): 
            self.end_char = (res.tell() - 1)
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        from pullenti.unitext.UnitextDocblock import UnitextDocblock
        from pullenti.unitext.UnitextNewline import UnitextNewline
        from pullenti.unitext.UnitextDocument import UnitextDocument
        if (par.hide_editions_and_comments): 
            if (self.typ == UnitextContainerType.EDITION or self.typ == UnitextContainerType.COMMENT): 
                return
        if (not par.call_before(self, res)): 
            return
        id0__ = ""
        if (self.id0_ is not None): 
            id0__ = " id=\"{0}\"".format(self.id0_)
        if (par is not None and par.out_begin_end_chars and self.begin_char <= self.end_char): 
            id0__ = "{0} bc=\"{1}\" ec=\"{2}\"".format(id0__, self.begin_char, self.end_char)
        if (((self.children is None or len(self.children) == 0)) and self.typ != UnitextContainerType.SHAPE): 
            par.call_after(self, res)
            return
        is_div = False
        is_span = False
        is_pre = False
        tit = ("" if self.typ == UnitextContainerType.UNDEFINED else Utils.enumToString(self.typ).lower())
        if (self.html_title is not None): 
            tmp = io.StringIO()
            MiscHelper.correct_html_value(tmp, self.html_title, True, False)
            tit = Utils.toStringStringIO(tmp)
        else: 
            p = self.parent
            while p is not None: 
                if (p.html_title is not None): 
                    tit = ""
                    break
                p = p.parent
        if (not Utils.isNullOrEmpty(tit)): 
            tit = " title=\"{0}\"".format(tit)
        style = None
        if (par is not None and self.id0_ is not None and self.id0_ in par.styles): 
            style = par.styles[self.id0_]
        if (style is None): 
            style = self.html_style
        if (style is not None): 
            is_div = not self.is_inline
            is_span = not is_div
            if (is_div): 
                print("\r\n", end="", file=res)
            print("<{2} style=\"{3}\" {1}{0}>".format(tit, id0__, ("div" if is_div else "span"), style), end="", file=res, flush=True)
        elif (self.typ == UnitextContainerType.SHAPE): 
            print("\r\n<div style=\"border-width:2pt;border-color:green;border-style:dotted;margin:10pt;padding:5pt\" {1}{0}>".format(tit, id0__), end="", file=res, flush=True)
            is_div = True
        elif (self.typ == UnitextContainerType.MONOSPACE): 
            print("\r\n<div style=\"font-family:monospace\" {1}{0}>".format(tit, id0__), end="", file=res, flush=True)
            print("<pre>", end="", file=res)
            is_div = True
            is_pre = True
        elif (self.typ == UnitextContainerType.CONTENTCONTROL): 
            is_div = not self.is_inline
            is_span = not is_div
            if (is_div): 
                print("\r\n", end="", file=res)
            print("<{2} style=\"background-color:lightyellow;border:1pt solid black\" {1}{0}>".format(tit, id0__, ("div" if is_div else "span")), end="", file=res, flush=True)
        elif (self.typ == UnitextContainerType.RIGHTALIGN): 
            print("\r\n<div style=\"font-weight:normal;font-style:italic;text-align:right\" {1}{0}>".format(tit, id0__), end="", file=res, flush=True)
            is_div = True
        elif (self.typ == UnitextContainerType.EDITION or self.typ == UnitextContainerType.COMMENT): 
            if (self.typ == UnitextContainerType.COMMENT and self.is_inline): 
                is_span = True
            else: 
                is_div = True
                print("\r\n", end="", file=res)
            print("<{0} {2} style=\"font-weight: normal;font-style: italic;{3}\"{1}>".format(("span" if is_span else "div"), tit, id0__, "font-size: smaller;color: gray"), end="", file=res, flush=True)
        elif (((self.typ == UnitextContainerType.HEAD or ((self.typ == UnitextContainerType.NAME and (isinstance(self.parent, UnitextDocblock)))))) and not self.is_inline): 
            ali = "center"
            marg = 10
            db = Utils.asObjectOrNull(self.parent, UnitextDocblock)
            if (db is not None and db.typname is not None): 
                if (((Utils.compareStrings(db.typname, "Clause", True) == 0 or Utils.compareStrings(db.typname, "Mail", True) == 0 or Utils.compareStrings(db.typname, "Chapter", True) == 0) or Utils.compareStrings(db.typname, "Paragraph", True) == 0 or Utils.compareStrings(db.typname, "SubParagraph", True) == 0) or Utils.compareStrings(db.typname, "Section", True) == 0 or Utils.compareStrings(db.typname, "Subsection", True) == 0): 
                    ali = "left"
                    marg = 10
            print("\r\n<div style=\"text-align:{2};margin-bottom:{3}pt\" {1}{0}>".format(tit, id0__, ali, marg), end="", file=res, flush=True)
            is_div = True
        elif (self.typ == UnitextContainerType.DIRECTIVE): 
            print("\r\n<div style=\"text-align:center;text-decoration:underline\" {1}{0}>".format(tit, id0__), end="", file=res, flush=True)
            is_div = True
        elif (self.typ == UnitextContainerType.TAIL): 
            print("\r\n<div style=\"text-align:right\" {1}{0}>".format(tit, id0__), end="", file=res, flush=True)
            is_div = True
        elif (self.typ == UnitextContainerType.HIGHLIGHTING): 
            print("<span style=\"background-color:yellow\" {1}{0}>".format(tit, id0__), end="", file=res, flush=True)
            is_span = True
        elif (self.typ != UnitextContainerType.UNDEFINED): 
            if (self.parent is not None and (isinstance(self.parent.parent, UnitextDocblock)) and Utils.compareStrings(Utils.ifNotNull(self.parent.parent.typname, ""), "INDEXITEM", True) == 0): 
                print("<span{0}>".format(id0__), end="", file=res, flush=True)
                is_span = True
            else: 
                print("<b {1}{0}>".format(tit, id0__), end="", file=res, flush=True)
        elif (((isinstance(self.parent, UnitextDocument)) and par is not None and par.out_styles) and self._m_styled_frag is not None and self._m_styled_frag.style is not None): 
            print("\r\n<div{0} style=\"".format(id0__), end="", file=res, flush=True)
            self._m_styled_frag.style.get_html(res)
            print("\">", end="", file=res)
            is_div = True
        elif (not Utils.isNullOrEmpty(id0__)): 
            print("<span{0}>".format(id0__), end="", file=res, flush=True)
            is_span = True
        out_styles = False
        if (par is not None and par.out_styles and not self.is_inline): 
            if (self.get_styled_fragment(-1) is not None): 
                out_styles = True
        cur_st_fr = None
        i = 0
        first_pass707 = True
        while True:
            if first_pass707: first_pass707 = False
            else: i += 1
            if (not (i < len(self.children))): break
            ch = self.children[i]
            if (i == 29): 
                pass
            if (isinstance(ch, UnitextNewline)): 
                if (ch.count == 1): 
                    if (((i + 1) < len(self.children)) and not self.children[i + 1].is_inline): 
                        continue
                    if ((i + 1) == len(self.children) and self.parent is not None and not self.parent.is_inline): 
                        continue
            if (out_styles): 
                fr = ch.get_styled_fragment(-1)
                if (fr is not None and fr.typ == UnitextStyledFragmentType.INLINE): 
                    fr = fr.parent
                if (fr is None): 
                    if (cur_st_fr is not None): 
                        cur_st_fr = (None)
                        print("</div>", end="", file=res)
                elif (fr != cur_st_fr): 
                    if (cur_st_fr is not None): 
                        print("</div>", end="", file=res)
                    cur_st_fr = (None)
                    if (fr.style_id > 0 and fr.style is not None): 
                        cur_st_fr = fr
                        print("\r\n<div style=\"", end="", file=res)
                        fr.style.get_html(res)
                        print("\">", end="", file=res)
            ch.get_html(res, par)
            if (par is not None and res.tell() > par.max_html_size): 
                break
        if (cur_st_fr is not None): 
            print("</div>", end="", file=res)
        if (is_pre): 
            print("</pre>", end="", file=res)
        if (is_div): 
            print("</div>\r\n", end="", file=res)
            if (par is not None): 
                par._out_footnotes(res)
        elif (is_span): 
            print("</span>", end="", file=res)
        elif (self.typ != UnitextContainerType.UNDEFINED): 
            print("</b>", end="", file=res)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("container")
        self._write_xml_attrs(xml0_)
        if (self.typ != UnitextContainerType.UNDEFINED): 
            xml0_.write_attribute_string("type", Utils.enumToString(self.typ).lower())
        if (self.data is not None): 
            xml0_.write_attribute_string("data", MiscHelper.correct_xml_value(self.data))
        if (not Utils.isNullOrEmpty(self.html_style)): 
            xml0_.write_attribute_string("style", MiscHelper.correct_xml_value(self.html_style))
        if (self.__m_is_inline >= 0): 
            xml0_.write_attribute_string("inline", ("true" if self.__m_is_inline > 0 else "false"))
        for ch in self.children: 
            ch.get_xml(xml0_)
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
        super().from_xml(xml0_)
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "type"): 
                    try: 
                        self.typ = (Utils.valToEnum(a[1], UnitextContainerType))
                    except Exception as ex544: 
                        pass
                elif (Utils.getXmlAttrLocalName(a) == "data"): 
                    self.data = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "style"): 
                    self.html_style = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "inline"): 
                    self.__m_is_inline = (1 if a[1] == "true" else 0)
        for x in xml0_: 
            it = UnitextHelper.create_item(x)
            if (it is not None): 
                self.children.append(it)
    
    @property
    def is_whitespaces(self) -> bool:
        for ch in self.children: 
            if (not ch.is_whitespaces): 
                return False
        return True
    
    @property
    def is_inline(self) -> bool:
        from pullenti.unitext.UnitextDocument import UnitextDocument
        if (self.__m_is_inline >= 0): 
            return self.__m_is_inline > 0
        if (self.children is not None): 
            for ch in self.children: 
                if (not ch.is_inline): 
                    return False
        if (self.parent is None or (isinstance(self.parent, UnitextDocument))): 
            return False
        return True
    @is_inline.setter
    def is_inline(self, value) -> bool:
        self.__m_is_inline = (1 if value else 0)
        return value
    
    def get_all_items(self, res : typing.List['UnitextItem'], lev : int) -> None:
        if (lev > 20): 
            pass
        if (res is not None): 
            res.append(self)
        if (self.children is not None): 
            for ch in self.children: 
                ch.parent = (self)
                ch.get_all_items(res, lev + 1)
    
    def _add_plain_text_pos(self, d : int) -> None:
        super()._add_plain_text_pos(d)
        for ch in self.children: 
            ch._add_plain_text_pos(d)
    
    def _correct(self, typ_ : 'LocCorrTyp', data_ : object) -> None:
        for ch in self.children: 
            ch._correct(typ_, data_)
    
    def _replace_child(self, old : 'UnitextItem', ne : 'UnitextItem') -> bool:
        i = self.get_child_index_of(old)
        if (i < 0): 
            return False
        self.children[i] = ne
        ne.parent = (self)
        return True
    
    def _set_default_text_pos(self, cp : int, res : io.StringIO) -> None:
        self.begin_char = cp.value
        for ch in self.children: 
            ch._set_default_text_pos(cp, res)
            ch.parent = (self)
        self.end_char = (cp.value - 1)
    
    @staticmethod
    def _new92(_arg1 : 'UnitextContainerType') -> 'UnitextContainer':
        res = UnitextContainer()
        res.typ = _arg1
        return res
    
    @staticmethod
    def _new372(_arg1 : int) -> 'UnitextContainer':
        res = UnitextContainer()
        res.end_char = _arg1
        return res
    
    @staticmethod
    def _new377(_arg1 : 'UnitextItem', _arg2 : int, _arg3 : int, _arg4 : str) -> 'UnitextContainer':
        res = UnitextContainer()
        res.parent = _arg1
        res.begin_char = _arg2
        res.end_char = _arg3
        res.id0_ = _arg4
        return res
    
    @staticmethod
    def _new427(_arg1 : 'UnitextContainerType', _arg2 : 'UnitextStyledFragment') -> 'UnitextContainer':
        res = UnitextContainer()
        res.typ = _arg1
        res._m_styled_frag = _arg2
        return res
    
    @staticmethod
    def _new543(_arg1 : 'UnitextContainerType', _arg2 : 'UnitextItem') -> 'UnitextContainer':
        res = UnitextContainer()
        res.typ = _arg1
        res.parent = _arg2
        return res
    
    @staticmethod
    def _new546(_arg1 : int) -> 'UnitextContainer':
        res = UnitextContainer()
        res.begin_char = _arg1
        return res