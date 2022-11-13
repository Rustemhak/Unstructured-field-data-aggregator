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
from pullenti.unitext.GetHtmlParamFootnoteOutType import GetHtmlParamFootnoteOutType
from pullenti.unitext.GetPlaintextParam import GetPlaintextParam
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextDocblock import UnitextDocblock

class UnitextFootnote(UnitextItem):
    """ Сноска """
    
    def __init__(self) -> None:
        super().__init__()
        self.content = None;
        self.is_endnote = False
        self.custom_mark = None
        self.doc_block_id = None
    
    def __str__(self) -> str:
        if (self.doc_block_id is not None): 
            ttt = (Utils.ifNotNull(self.html_title, "")).replace('\r', ' ').replace('\n', ' ')
            if (len(ttt) > 100): 
                ttt = (ttt[0:0+100] + "...")
            return "<{0}> -> {1}".format(Utils.ifNotNull(self.custom_mark, ""), ttt)
        return "{0}: {1}".format(("Endnote" if self.is_endnote else "Footnote"), ("" if self.content is None else str(self.content)))
    
    def clone(self) -> 'UnitextItem':
        res = UnitextFootnote()
        res._clone_from(self)
        if (self.content is not None): 
            res.content = self.content.clone()
        res.is_endnote = self.is_endnote
        res.custom_mark = self.custom_mark
        res.doc_block_id = self.doc_block_id
        return res
    
    def optimize(self, is_content : bool, pars : 'CreateDocumentParam') -> 'UnitextItem':
        if (self.content is not None): 
            self.content = self.content.optimize(True, pars)
        if (self.content is None and self.html_title is None): 
            return None
        return self
    
    def get_all_items(self, res : typing.List['UnitextItem'], lev : int) -> None:
        if (res is not None): 
            res.append(self)
        if (self.content is not None): 
            self.content.parent = (self)
            self.content.get_all_items(res, lev + 1)
    
    @property
    def _inner_tag(self) -> str:
        return "footnote"
    
    def find_by_id(self, id0__ : str) -> 'UnitextItem':
        if (self.id0_ == id0__): 
            return self
        res = None
        if (self.content is not None): 
            res = self.content.find_by_id(id0__)
            if ((res) is not None): 
                return res
        return None
    
    __m_footnotes_param = None
    
    __m_footnotes_param1 = None
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
        if (pars is None): 
            pars = UnitextItem._m_def_params
        if (not Utils.isNullOrEmpty(pars.footnotes_template) and self.content is not None): 
            tmp = io.StringIO()
            self.content.get_plaintext(tmp, (UnitextFootnote.__m_footnotes_param if pars.set_positions else UnitextFootnote.__m_footnotes_param1))
            if (tmp.tell() > 0 and Utils.getCharAtStringIO(tmp, tmp.tell() - 1) == '.'): 
                Utils.setLengthStringIO(tmp, tmp.tell() - 1)
            txt = Utils.toStringStringIO(tmp)
            if ((self.custom_mark is not None and (len(self.custom_mark) < len(txt)) and txt.startswith(self.custom_mark)) and Utils.isWhitespace(txt[len(self.custom_mark)])): 
                Utils.removeStringIO(tmp, 0, len(self.custom_mark) + 1)
                txt = Utils.toStringStringIO(tmp)
            d = pars.footnotes_template.find("%1")
            if (d < 0): 
                if (pars.set_positions): 
                    self.content._add_plain_text_pos(res.tell())
                print(pars.footnotes_template, end="", file=res)
                if (pars.set_positions): 
                    self.content.end_char = ((self.content.begin_char + ((res.tell() - self.begin_char))) - 1)
            else: 
                if (pars.set_positions): 
                    self.content._add_plain_text_pos(res.tell() + (((0 if d < 0 else d))))
                if (len(txt) > 0): 
                    print(pars.footnotes_template.replace("%1", txt), end="", file=res)
        if (pars is not None and pars.set_positions): 
            self.end_char = ((self.begin_char + ((res.tell() - self.begin_char))) - 1)
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (self.content is None and self.doc_block_id is None): 
            return
        if (par.hide_editions_and_comments and (isinstance(self.content, UnitextContainer))): 
            if (self.content.typ == UnitextContainerType.EDITION or self.content.typ == UnitextContainerType.COMMENT): 
                return
        if (not par.call_before(self, res)): 
            return
        id0__ = ""
        if (self.id0_ is not None): 
            id0__ = " id=\"{0}\"".format(self.id0_)
        if (self.doc_block_id is not None): 
            aaa = False
            if (par is not None): 
                p = self.parent
                while p is not None: 
                    db = Utils.asObjectOrNull(p.find_by_id(self.doc_block_id), UnitextDocblock)
                    if (db is not None): 
                        if (not db in par._m_footnotes_db): 
                            par._m_footnotes_db.append(db)
                        aaa = True
                        break
                    p = p.parent
            if (not aaa): 
                pass
            print("<span title=\"".format(), end="", file=res, flush=True)
            MiscHelper.correct_html_value(res, Utils.ifNotNull(self.html_title, ""), True, False)
            print("\" style=\"color:red\"><sup>{0}</sup></span>".format(Utils.ifNotNull(self.custom_mark, "*")), end="", file=res, flush=True)
            par.call_after(self, res)
            return
        if (par is not None and par.footnotes == GetHtmlParamFootnoteOutType.ENDOFUNIT): 
            if (self.is_endnote): 
                par._m_endnotes.append(self)
            else: 
                par._m_footnotes.append(self)
            tmp = io.StringIO()
            self.content.get_plaintext(tmp, UnitextFootnote.__m_footnotes_param1)
            print("<span title=\"".format(), end="", file=res, flush=True)
            MiscHelper.correct_html_value(res, Utils.toStringStringIO(tmp), True, False)
            if (self.is_endnote): 
                print("\" style=\"color:red\"><sup>&lt;E{0}&gt;</sup></span>".format(len(par._m_endnotes)), end="", file=res, flush=True)
            elif ((isinstance(self.content, UnitextContainer)) and self.content.typ == UnitextContainerType.EDITION): 
                print("\" style=\"color:lightgray;font-size:smaller\"><sup>&lt;{0}&gt;</sup></span>".format(len(par._m_footnotes)), end="", file=res, flush=True)
            else: 
                print("\" style=\"color:red\"><sup>&lt;{0}&gt;</sup></span>".format(len(par._m_footnotes)), end="", file=res, flush=True)
            par.call_after(self, res)
            return
        if (par is not None and par.footnotes == GetHtmlParamFootnoteOutType.INBRACKETS): 
            print(" <i{0}><sub title=\"Сноска {1}\">(".format(id0__, Utils.ifNotNull(self.custom_mark, "")), end="", file=res, flush=True)
            self.content.get_html(res, par)
            print(")</sub></i>", end="", file=res)
        else: 
            tmp = io.StringIO()
            self.content.get_plaintext(tmp, UnitextFootnote.__m_footnotes_param1)
            txt = Utils.toStringStringIO(tmp).strip()
            print("<span title=\"".format(), end="", file=res, flush=True)
            MiscHelper.correct_html_value(res, txt, True, False)
            print("\" style=\"color:red\"{1}><sup>{0})</sup></span>".format(("**" if self.is_endnote else "*"), id0__), end="", file=res, flush=True)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("footnote")
        self._write_xml_attrs(xml0_)
        if (self.is_endnote): 
            xml0_.write_attribute_string("endnote", "true")
        if (self.custom_mark is not None): 
            xml0_.write_attribute_string("mark", MiscHelper.correct_xml_value(self.custom_mark))
        if (self.doc_block_id is not None): 
            xml0_.write_attribute_string("docblockid", self.doc_block_id)
        if (self.content is not None): 
            self.content.get_xml(xml0_)
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
        super().from_xml(xml0_)
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "endnote"): 
                    self.is_endnote = a[1] == "true"
                elif (Utils.getXmlAttrLocalName(a) == "mark"): 
                    self.custom_mark = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "docblockid"): 
                    self.doc_block_id = a[1]
        for x in xml0_: 
            self.content = UnitextHelper.create_item(x)
            break
    
    def _add_plain_text_pos(self, d : int) -> None:
        super()._add_plain_text_pos(d)
        if (self.content is not None): 
            self.content._add_plain_text_pos(d)
    
    def _correct(self, typ : 'LocCorrTyp', data : object) -> None:
        if (self.content is not None): 
            self.content._correct(typ, data)
    
    def _replace_child(self, old : 'UnitextItem', ne : 'UnitextItem') -> bool:
        if (self.content != old): 
            return False
        self.content = ne
        ne.parent = (self)
        return True
    
    def _set_default_text_pos(self, cp : int, res : io.StringIO) -> None:
        self.begin_char = cp.value
        cp.value += 1
        if (res is not None): 
            print('<', end="", file=res)
        if (self.content is not None): 
            self.content._set_default_text_pos(cp, res)
            self.content.parent = (self)
        cp.value += 1
        if (res is not None): 
            print('>', end="", file=res)
        self.end_char = (cp.value - 1)
    
    @staticmethod
    def _new98(_arg1 : str) -> 'UnitextFootnote':
        res = UnitextFootnote()
        res.custom_mark = _arg1
        return res
    
    @staticmethod
    def _new267(_arg1 : 'UnitextItem', _arg2 : bool) -> 'UnitextFootnote':
        res = UnitextFootnote()
        res.content = _arg1
        res.is_endnote = _arg2
        return res
    
    @staticmethod
    def _new312(_arg1 : 'UnitextItem') -> 'UnitextFootnote':
        res = UnitextFootnote()
        res.content = _arg1
        return res
    
    @staticmethod
    def _new469(_arg1 : 'UnitextItem', _arg2 : str) -> 'UnitextFootnote':
        res = UnitextFootnote()
        res.content = _arg1
        res.custom_mark = _arg2
        return res
    
    @staticmethod
    def _new471(_arg1 : bool, _arg2 : 'UnitextItem') -> 'UnitextFootnote':
        res = UnitextFootnote()
        res.is_endnote = _arg1
        res.content = _arg2
        return res
    
    # static constructor for class UnitextFootnote
    @staticmethod
    def _static_ctor():
        UnitextFootnote.__m_footnotes_param = GetPlaintextParam._new560(True, " ", " ", " ", " ", " ")
        UnitextFootnote.__m_footnotes_param1 = GetPlaintextParam._new560(False, " ", " ", " ", " ", " ")

UnitextFootnote._static_ctor()