# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Xml import XmlWriter

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextStyledFragmentType import UnitextStyledFragmentType
from pullenti.unitext.internal.uni.LocCorrTyp import LocCorrTyp
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextPlaintextType import UnitextPlaintextType
from pullenti.unitext.UnitextDocument import UnitextDocument

class UnitextPlaintext(UnitextItem):
    """ Фрагмент плоского текста.
    
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.text = None;
        self.typ = UnitextPlaintextType.SIMPLE
        self.layout = None;
    
    def clone(self) -> 'UnitextItem':
        res = UnitextPlaintext()
        res._clone_from(self)
        res.text = self.text
        res.typ = self.typ
        res.layout = self.layout
        return res
    
    @property
    def is_whitespaces(self) -> bool:
        if (self.text is None): 
            return True
        for ch in self.text: 
            if (not Utils.isWhitespace(ch)): 
                return False
        return True
    
    @property
    def _inner_tag(self) -> str:
        return "txt"
    
    def _merge_with(self, pt : 'UnitextPlaintext') -> None:
        if (pt.text is None or self.text is None): 
            return
        if (pt.layout is not None or self.layout is not None): 
            lay = Utils.newArray(len(pt.text) + len(self.text), None)
            if (self.layout is not None): 
                i = 0
                while i < len(self.layout): 
                    if (i < len(lay)): 
                        lay[i] = self.layout[i]
                    i += 1
            if (pt.layout is not None): 
                i = 0
                while i < len(pt.layout): 
                    if ((len(self.text) + i) < len(lay)): 
                        lay[len(self.text) + i] = pt.layout[i]
                    i += 1
            self.layout = lay
        self.text += pt.text
        if (pt.id0_ is not None and self.id0_ is None): 
            self.id0_ = pt.id0_
        if (pt.end_char > self.end_char): 
            self.end_char = pt.end_char
    
    def _remove_start(self, len0_ : int) -> 'UnitextPlaintext':
        if (len(self.text) <= len0_): 
            return None
        b = UnitextPlaintext()
        b.parent = self.parent
        b.begin_char = self.begin_char
        b.end_char = ((b.begin_char + len0_) - 1)
        b.text = self.text[0:0+(b.end_char - b.begin_char) + 1]
        b.typ = self.typ
        if (self.id0_ is not None): 
            b.id0_ = "{0}_{1}".format(self.id0_, self.end_char)
        if (self.layout is not None): 
            if (len(self.layout) <= len0_): 
                self.layout = (None)
            else: 
                b.layout = Utils.newArray(len0_, None)
                i = 0
                while (i < len0_) and (i < len(self.layout)): 
                    b.layout[i] = self.layout[i]
                    i += 1
                lay = Utils.newArray(len(self.layout) - len0_, None)
                i = 0
                while i < len(lay): 
                    lay[i] = self.layout[len0_ + i]
                    i += 1
                self.layout = lay
        le = (b.end_char - b.begin_char) + 1
        self.text = self.text[le:]
        self.begin_char += le
        return b
    
    def _remove_end(self, len0_ : int) -> 'UnitextPlaintext':
        e0_ = UnitextPlaintext()
        e0_.parent = self.parent
        e0_.begin_char = ((self.end_char + 1) - len0_)
        e0_.end_char = ((e0_.begin_char + len0_) - 1)
        dd = (((self.end_char - self.begin_char) + 1)) - (((e0_.end_char - e0_.begin_char) + 1))
        if (dd >= len(self.text)): 
            return None
        e0_.text = self.text[dd:]
        e0_.typ = self.typ
        if (self.id0_ is not None): 
            e0_.id0_ = "{0}_{1}".format(self.id0_, self.begin_char)
        if (self.layout is not None): 
            e0_.layout = Utils.newArray(len0_, None)
            i = 0
            while i < len0_: 
                j = (len(self.layout) - len0_) + i
                if (j >= 0 and (j < len(self.layout))): 
                    e0_.layout[i] = self.layout[j]
                i += 1
            if ((len(self.layout) - len0_) > 0): 
                lay = Utils.newArray(len(self.layout) - len0_, None)
                i = 0
                while i < len(lay): 
                    if (i < len(self.layout)): 
                        lay[i] = self.layout[i]
                    i += 1
                self.layout = lay
            else: 
                self.layout = (None)
        self.end_char -= len0_
        self.text = self.text[0:0+(self.end_char - self.begin_char) + 1]
        return e0_
    
    def __str__(self) -> str:
        ttt = Utils.trimStartString((Utils.ifNotNull(self.text, "")))
        if (len(ttt) > 100): 
            ttt = (ttt[0:0+100] + "...")
        if (self.typ == UnitextPlaintextType.SIMPLE): 
            return "'{0}'".format(ttt)
        elif (self.typ == UnitextPlaintextType.GENERATED): 
            return "[{0}]".format(ttt)
        else: 
            return "<{0}>".format(ttt)
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
            if (self.begin_char == 793): 
                pass
        if (pars is not None and pars.sup_template is not None and self.typ == UnitextPlaintextType.SUP): 
            txt = (Utils.ifNotNull(self.text, "")).strip()
            if (not Utils.isNullOrEmpty(txt)): 
                print(pars.sup_template.replace("%1", txt), end="", file=res)
        elif (pars is not None and pars.sub_template is not None and self.typ == UnitextPlaintextType.SUB): 
            txt = (Utils.ifNotNull(self.text, "")).strip()
            if (not Utils.isNullOrEmpty(txt)): 
                print(pars.sub_template.replace("%1", txt), end="", file=res)
        elif (self.text is not None): 
            txt = self.text
            if (pars is not None and pars.page_break is not None): 
                if (len(pars.page_break) == 1 and txt.find(pars.page_break[0]) >= 0): 
                    txt = txt.replace(pars.page_break[0], ' ')
            print(txt, end="", file=res)
        if (pars is not None and pars.set_positions): 
            self.end_char = (res.tell() - 1)
    
    def __find_style(self, id0__ : int) -> 'UnitextStyle':
        it = self.parent
        while it is not None: 
            doc = Utils.asObjectOrNull(it, UnitextDocument)
            if (doc is not None): 
                if (id0__ < len(doc.styles)): 
                    return doc.styles[id0__]
            it = it.parent
        return None
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (not par.call_before(self, res)): 
            return
        out_span = False
        if (par is not None and self.id0_ is not None and self.id0_ in par.styles): 
            print("<span style=\"{0}\" id=\"{1}\"".format(par.styles[self.id0_], self.id0_), end="", file=res, flush=True)
            out_span = True
        elif (self.id0_ is not None): 
            print("<span id=\"{0}\"".format(self.id0_), end="", file=res, flush=True)
            out_span = True
        if (par is not None and par.out_begin_end_chars and self.begin_char <= self.end_char): 
            if (not out_span): 
                print("<span", end="", file=res)
            out_span = True
            print(" bc=\"{0}\" ec=\"{1}\"".format(self.begin_char, self.end_char), end="", file=res, flush=True)
        if (out_span): 
            print('>', end="", file=res)
        if (self.typ == UnitextPlaintextType.SUB): 
            print("<SUB>", end="", file=res)
        elif (self.typ == UnitextPlaintextType.SUP): 
            print("<SUP>", end="", file=res)
        text_outed = False
        if ((par is not None and par.out_styles and self.get_styled_fragment(-1) is not None) and self.end_char >= self.begin_char): 
            map0_ = Utils.newArray((self.end_char + 1) - self.begin_char, None)
            has_inline = False
            i = self.begin_char
            first_pass708 = True
            while True:
                if first_pass708: first_pass708 = False
                else: i += 1
                if (not (i <= self.end_char)): break
                ff = self.get_styled_fragment(i)
                if (ff is None or (ff.style_id < 0) or ff.style is None): 
                    continue
                if (ff.typ == UnitextStyledFragmentType.INLINE): 
                    pass
                elif (ff.begin_char >= self.begin_char and ff.end_char <= self.end_char): 
                    if (self.parent is not None and self.parent.get_styled_fragment(i) == ff): 
                        continue
                else: 
                    continue
                has_inline = True
                map0_[i - self.begin_char] = ff
            if (has_inline): 
                text_outed = True
                cur = None
                i = 0
                while (i < len(map0_)) and (i < len(self.text)): 
                    if (map0_[i] is None): 
                        if (cur is not None): 
                            cur = (None)
                            print("</span>", end="", file=res)
                    elif (cur != map0_[i]): 
                        if (cur is not None): 
                            cur = (None)
                            print("</span>", end="", file=res)
                        cur = map0_[i]
                        print("<span style=\"", end="", file=res)
                        cur.style.get_html(res)
                        print("\">", end="", file=res)
                    MiscHelper.correct_html_char(res, self.text[i])
                    i += 1
                if (cur is not None): 
                    cur = (None)
                    print("</span>", end="", file=res)
        if (not text_outed): 
            MiscHelper.correct_html_value(res, self.text, False, False)
        if (self.typ == UnitextPlaintextType.SUB): 
            print("</SUB>", end="", file=res)
        elif (self.typ == UnitextPlaintextType.SUP): 
            print("</SUP>", end="", file=res)
        if (out_span): 
            print("</span>", end="", file=res)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("text")
        self._write_xml_attrs(xml0_)
        if (self.typ != UnitextPlaintextType.SIMPLE): 
            xml0_.write_attribute_string("type", Utils.enumToString(self.typ).lower())
        txt = MiscHelper.correct_xml_value(self.text)
        sp = 0
        for ch in txt: 
            if (ch != ' '): 
                break
            else: 
                sp += 1
        if (sp > 0 and sp == len(txt)): 
            xml0_.write_attribute_string("spaces", str(sp))
        try: 
            xml0_.write_string(MiscHelper.correct_xml_value(txt))
        except Exception as ex: 
            pass
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        super().from_xml(xml0_)
        sp = 0
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "type"): 
                    try: 
                        self.typ = (Utils.valToEnum(a[1], UnitextPlaintextType))
                    except Exception as ex571: 
                        pass
                elif (Utils.getXmlAttrLocalName(a) == "spaces"): 
                    wrapsp572 = RefOutArgWrapper(0)
                    Utils.tryParseInt(a[1], wrapsp572)
                    sp = wrapsp572.value
        self.text = Utils.getXmlInnerText(xml0_)
        if (sp == 1): 
            self.text = " "
        elif (sp == 2): 
            self.text = "  "
        elif (sp > 2): 
            tmp = io.StringIO()
            i = 0
            while i < sp: 
                print(' ', end="", file=tmp)
                i += 1
            self.text = Utils.toStringStringIO(tmp)
    
    def _correct(self, typ_ : 'LocCorrTyp', data : object) -> None:
        from pullenti.unitext.internal.uni.UnitextCorrHelper import UnitextCorrHelper
        if (typ_ == LocCorrTyp.NPSP2SP): 
            self.text = UnitextCorrHelper._corr_nbsp(self.text)
        elif (typ_ == LocCorrTyp.TRIMEND): 
            self.text = Utils.trimEndString(self.text)
            if (self.end_char > 0): 
                self.end_char = ((self.begin_char + len(self.text)) - 1)
    
    def _set_default_text_pos(self, cp : int, res : io.StringIO) -> None:
        self.begin_char = cp.value
        cp.value += len(self.text)
        self.end_char = (cp.value - 1)
        if (res is not None): 
            print(self.text, end="", file=res)
    
    @staticmethod
    def _new51(_arg1 : str) -> 'UnitextPlaintext':
        res = UnitextPlaintext()
        res.text = _arg1
        return res
    
    @staticmethod
    def _new52(_arg1 : str, _arg2 : 'UnitextPlaintextType') -> 'UnitextPlaintext':
        res = UnitextPlaintext()
        res.text = _arg1
        res.typ = _arg2
        return res
    
    @staticmethod
    def _new87(_arg1 : str, _arg2 : object) -> 'UnitextPlaintext':
        res = UnitextPlaintext()
        res.text = _arg1
        res.tag = _arg2
        return res
    
    @staticmethod
    def _new335(_arg1 : str, _arg2 : str) -> 'UnitextPlaintext':
        res = UnitextPlaintext()
        res.text = _arg1
        res.page_section_id = _arg2
        return res
    
    @staticmethod
    def _new348(_arg1 : str, _arg2 : 'UnitextPlaintextType', _arg3 : str) -> 'UnitextPlaintext':
        res = UnitextPlaintext()
        res.text = _arg1
        res.typ = _arg2
        res.page_section_id = _arg3
        return res
    
    @staticmethod
    def _new375(_arg1 : 'UnitextItem') -> 'UnitextPlaintext':
        res = UnitextPlaintext()
        res.parent = _arg1
        return res
    
    @staticmethod
    def _new564(_arg1 : str, _arg2 : int, _arg3 : int) -> 'UnitextPlaintext':
        res = UnitextPlaintext()
        res.text = _arg1
        res.begin_char = _arg2
        res.end_char = _arg3
        return res