# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextFootnote import UnitextFootnote
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext

class UnitextHyperlink(UnitextItem):
    """ Гиперссылка """
    
    def __init__(self) -> None:
        super().__init__()
        self.href = None;
        self.content = None;
        self.is_internal = False
        self.data = None;
    
    def __str__(self) -> str:
        return "Hyperlink {0}".format(Utils.ifNotNull(self.href, ""))
    
    def clone(self) -> 'UnitextItem':
        res = UnitextHyperlink()
        res._clone_from(self)
        res.href = self.href
        res.data = self.data
        res.is_internal = self.is_internal
        if (self.content is not None): 
            res.content = self.content.clone()
        return res
    
    @property
    def _inner_tag(self) -> str:
        return "hyplnk"
    
    @property
    def is_inline(self) -> bool:
        if (self.content is None): 
            return True
        return self.content.is_inline
    
    def get_all_items(self, res : typing.List['UnitextItem'], lev : int) -> None:
        if (res is not None): 
            res.append(self)
        if (self.content is not None): 
            self.content.parent = (self)
            self.content.get_all_items(res, lev + 1)
    
    def find_by_id(self, id0__ : str) -> 'UnitextItem':
        if (self.id0_ == id0__): 
            return self
        res = None
        if (self.content is not None): 
            res = self.content.find_by_id(id0__)
            if ((res) is not None): 
                return res
        return None
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
        if (self.content is not None): 
            self.content.get_plaintext(res, pars)
        if (pars is None): 
            pars = UnitextItem._m_def_params
        if (not Utils.isNullOrEmpty(pars.hyperlinks_template) and self.href is not None and not self.is_internal): 
            tmp = io.StringIO()
            i = self.begin_char
            while i < res.tell(): 
                print(Utils.getCharAtStringIO(res, i), end="", file=tmp)
                i += 1
            txt = Utils.toStringStringIO(tmp)
            if (tmp.tell() == 0): 
                print(self.href, end="", file=res)
            elif (Utils.compareStrings(self.href, txt, True) != 0): 
                print(pars.hyperlinks_template.replace("%1", self.href), end="", file=res)
        if (pars is not None and pars.set_positions): 
            self.end_char = (res.tell() - 1)
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (not par.call_before(self, res)): 
            return
        tit = None
        if (self.html_title is not None or self.href is not None): 
            tmp = io.StringIO()
            MiscHelper.correct_html_value(tmp, Utils.ifNotNull(self.html_title, self.href), True, False)
            tit = Utils.toStringStringIO(tmp)
        if (self.is_internal): 
            print("<i>", end="", file=res)
        if (self.href is not None): 
            print("<a href=\"", end="", file=res)
            if (self.is_internal): 
                print('#', end="", file=res)
            MiscHelper.correct_html_value(res, self.href, True, False)
            print("\" title=\"{0}\"{1}".format(Utils.ifNotNull(tit, ""), ((" target=\"_blank\"" if par.hyperlinks_target_blank or self.href.startswith("http") else ""))), end="", file=res, flush=True)
        else: 
            print("<span style=\"text-decoration:underline\" title=\"{0}\"".format(Utils.ifNotNull(tit, "")), end="", file=res, flush=True)
        if (self.id0_ is not None): 
            print(" id=\"{0}\"".format(self.id0_), end="", file=res, flush=True)
        print(">", end="", file=res)
        if (self.content is not None): 
            self.content.get_html(res, par)
        if (self.href is not None): 
            print("</a>", end="", file=res)
        else: 
            print("</span>", end="", file=res)
        if (self.is_internal): 
            print("</i>", end="", file=res)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("hyperlink")
        self._write_xml_attrs(xml0_)
        if (self.href is not None): 
            xml0_.write_attribute_string("href", MiscHelper.correct_xml_value(self.href))
            if (self.is_internal): 
                xml0_.write_attribute_string("internal", "true")
        if (self.data is not None): 
            xml0_.write_attribute_string("data", MiscHelper.correct_xml_value(self.data))
        if (self.content is not None): 
            self.content.get_xml(xml0_)
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
        super().from_xml(xml0_)
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "href"): 
                    self.href = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "internal"): 
                    self.is_internal = a[1] == "true"
                elif (Utils.getXmlAttrLocalName(a) == "data"): 
                    self.data = a[1]
        for x in xml0_: 
            self.content = UnitextHelper.create_item(x)
            break
    
    def _add_plain_text_pos(self, d : int) -> None:
        super()._add_plain_text_pos(d)
        if (self.content is not None): 
            self.content._add_plain_text_pos(d)
    
    def _correct(self, typ : 'LocCorrTyp', data_ : object) -> None:
        if (self.content is not None): 
            self.content._correct(typ, data_)
    
    def optimize(self, is_content : bool, pars : 'CreateDocumentParam') -> 'UnitextItem':
        if (self.content is not None): 
            self.content = self.content.optimize(True, pars)
        if (pars is not None and self.href is not None): 
            if (((len(self.href) > 2 and self.href[0] == '<' and self.href[2] == '>')) or ((len(self.href) > 3 and self.href[0] == '<' and self.href[3] == '>'))): 
                tag_ = self.href[0:0+(3 if self.href[2] == '>' else 4)]
                pt = Utils.asObjectOrNull(self.content, UnitextPlaintext)
                if (pt is not None and pt.text.startswith(tag_)): 
                    foot = UnitextFootnote()
                    if (self.href[2] == '>'): 
                        foot.custom_mark = self.href[1:1+1]
                    else: 
                        foot.custom_mark = self.href[1:1+2]
                    txt = self.href[len(tag_):].strip()
                    if ("\\\"" in txt): 
                        txt = txt.replace("\\\"", "\"")
                    foot.content = (UnitextPlaintext._new51(txt))
                    return foot
                if (isinstance(self.content, UnitextFootnote)): 
                    return self.content
        return self
    
    def _replace_child(self, old : 'UnitextItem', ne : 'UnitextItem') -> bool:
        if (self.content != old): 
            return False
        self.content = ne
        ne.parent = (self)
        return True
    
    def _set_default_text_pos(self, cp : int, res : io.StringIO) -> None:
        self.begin_char = cp.value
        if (self.content is not None): 
            self.content._set_default_text_pos(cp, res)
            self.content.parent = (self)
        self.end_char = (cp.value - 1)
    
    @staticmethod
    def _new53(_arg1 : str) -> 'UnitextHyperlink':
        res = UnitextHyperlink()
        res.href = _arg1
        return res
    
    @staticmethod
    def _new466(_arg1 : bool, _arg2 : str) -> 'UnitextHyperlink':
        res = UnitextHyperlink()
        res.is_internal = _arg1
        res.href = _arg2
        return res