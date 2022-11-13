# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextDocblockType import UnitextDocblockType
from pullenti.unitext.UnitextItem import UnitextItem

class UnitextDocblock(UnitextItem):
    """ Cтруктурирующий блок из заголовочной части, тела, окончания и приложений.
    Выделяется только для некоторых форматов, если задать LoadDocumentStructure = true в параметрах создания.
    Но этот элемент активно используется на других этапах анализа, когда структура документа восстанавливается
    по плоскому тексту, а затем их иерархия оформляется этими элементами. Например, для нормативных актов
    это главы, статьи, части, пункты и подпункты.
    Структурирующий блок с заголовком
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.head = None;
        self.body = None;
        self.tail = None;
        self.appendix = None;
        self.typname = None;
        self.number = None;
        self.typ = UnitextDocblockType.UNDEFINED
        self.expired = False
        self.ext_block_id = None;
        self.__m_is_inline = False
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.typname is not None): 
            print("{0} ".format(self.typname), end="", file=res, flush=True)
        if (self.number is not None): 
            print("{0} ".format(self.number), end="", file=res, flush=True)
        if (self.typ != UnitextDocblockType.UNDEFINED): 
            print("Typ:{0} ".format(Utils.enumToString(self.typ)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    def clone(self) -> 'UnitextItem':
        res = UnitextDocblock()
        res._clone_from(self)
        if (self.head is not None): 
            res.head = (Utils.asObjectOrNull(self.head.clone(), UnitextContainer))
        if (self.body is not None): 
            res.body = self.body.clone()
        if (self.tail is not None): 
            res.tail = (Utils.asObjectOrNull(self.tail.clone(), UnitextContainer))
        if (self.appendix is not None): 
            res.appendix = self.appendix.clone()
        res.ext_block_id = self.ext_block_id
        res.typ = self.typ
        res.typname = self.typname
        res.number = self.number
        res.expired = self.expired
        return res
    
    @property
    def is_inline(self) -> bool:
        return self.__m_is_inline
    @is_inline.setter
    def is_inline(self, value) -> bool:
        self.__m_is_inline = value
        return value
    
    @property
    def _inner_tag(self) -> str:
        return "docblk"
    
    def find_by_id(self, id0__ : str) -> 'UnitextItem':
        if (self.id0_ == id0__): 
            return self
        res = None
        if (self.head is not None): 
            res = self.head.find_by_id(id0__)
            if ((res) is not None): 
                return res
        if (self.tail is not None): 
            res = self.tail.find_by_id(id0__)
            if ((res) is not None): 
                return res
        if (self.body is not None): 
            res = self.body.find_by_id(id0__)
            if ((res) is not None): 
                return res
        if (self.appendix is not None): 
            res = self.appendix.find_by_id(id0__)
            if ((res) is not None): 
                return res
        return None
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
        if (self.head is not None): 
            self.head.get_plaintext(res, pars)
        if (self.body is not None): 
            self.body.get_plaintext(res, pars)
        if (self.tail is not None): 
            self.tail.get_plaintext(res, pars)
        if (self.appendix is not None): 
            self.appendix.get_plaintext(res, pars)
        if (pars is not None and pars.set_positions): 
            self.end_char = (res.tell() - 1)
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (not par.call_before(self, res)): 
            return
        if (Utils.compareStrings(Utils.ifNotNull(self.typname, ""), "Footnote", True) == 0): 
            return
        tag_ = "div"
        if (self.is_inline): 
            tag_ = "span"
        elif (Utils.compareStrings(Utils.ifNotNull(self.typname, ""), "Indention", True) == 0 and (isinstance(self.parent, UnitextContainer)) and self.parent.children[0] == self): 
            blk = Utils.asObjectOrNull(self.parent.parent, UnitextDocblock)
            if (blk is not None and blk.head is not None and blk.head.is_inline): 
                tag_ = "span"
        if (Utils.compareStrings(Utils.ifNotNull(self.typname, ""), "Part", True) == 0 and self.head is None and self.number != "1"): 
            print("\r\n<BR/>", end="", file=res)
        print("\r\n<{0}".format(tag_), end="", file=res, flush=True)
        if (self.html_title is not None): 
            print(" title=\"", end="", file=res)
            MiscHelper.correct_html_value(res, self.html_title, True, False)
            print("\"", end="", file=res)
        margleft = 0
        if (self.typname == "ITEM" or self.typname == "SUBITEM"): 
            p = self.parent
            while p is not None: 
                if (isinstance(p, UnitextDocblock)): 
                    pb = Utils.asObjectOrNull(p, UnitextDocblock)
                    if (pb.typname == "ITEM" or pb.typname == "SUBITEM" or pb.typname == "CLAUSEPART"): 
                        margleft += 10
                p = p.parent
        if (Utils.compareStrings(Utils.ifNotNull(self.typname, ""), "Footnote", True) == 0): 
            print(" style=\"margin-left:{0}pt;margin-top:10pt;margin-bottom:10pt;font-size:smaller;text-align:left;font-weight:normal\"".format(30 + margleft), end="", file=res, flush=True)
        elif (Utils.compareStrings(Utils.ifNotNull(self.typname, ""), "Index", True) == 0): 
            print(" style=\"border:1pt solid black; background:lightgray; text-align:left;font-weight:normal;font-style:italic\"", end="", file=res)
        elif (self.typname is not None): 
            margtop = 0
            if (Utils.compareStrings(self.typname, "Chapter", True) == 0 or Utils.compareStrings(self.typname, "Section", True) == 0): 
                margtop = 20
            elif (Utils.compareStrings(self.typname, "Paragraph", True) == 0 or Utils.compareStrings(self.typname, "Subparagraph", True) == 0): 
                margtop = 15
            elif (Utils.compareStrings(self.typname, "Clause", True) == 0 or Utils.compareStrings(self.typname, "Subsection", True) == 0): 
                margtop = 10
            if (margtop > 0 or self.expired or margleft > 0): 
                print(" style=\"".format(), end="", file=res, flush=True)
                if (margtop > 0): 
                    print("margin-top:{0}pt;".format(margtop), end="", file=res, flush=True)
                if (margleft > 0): 
                    print("margin-left:{0}pt;".format(margleft), end="", file=res, flush=True)
                if (self.expired): 
                    print("background-color:lightgray;".format(), end="", file=res, flush=True)
                print("\"", end="", file=res)
        if (self.id0_ is not None): 
            print(" id=\"{0}\"".format(self.id0_), end="", file=res, flush=True)
        print(">", end="", file=res)
        if (self.head is not None): 
            if (Utils.compareStrings(Utils.ifNotNull(self.typname, ""), "Appendix", True) == 0): 
                i = 0
                i = 0
                while i < len(self.head.children): 
                    if ((isinstance(self.head.children[i], UnitextContainer)) and self.head.children[i].typ == UnitextContainerType.NAME): 
                        break
                    i += 1
                if (i > 0): 
                    print("\r\n<div style=\"text-align:right;font-style:italic\">", end="", file=res)
                    j = 0
                    while j < i: 
                        self.head.children[j].get_html(res, par)
                        j += 1
                    print("</div>", end="", file=res)
                if (i < len(self.head.children)): 
                    print("\r\n<div style=\"text-align:center;font-weight:bold;font-style:normal\">", end="", file=res)
                    while i < len(self.head.children): 
                        self.head.children[i].get_html(res, par)
                        i += 1
                    print("</div>", end="", file=res)
                print("<div style=\"margin-bottom:20pt\" />", end="", file=res)
            else: 
                if (Utils.compareStrings(Utils.ifNotNull(self.typname, ""), "Mail", True) != 0): 
                    print("<b>", end="", file=res)
                else: 
                    print("<i>", end="", file=res)
                self.head.get_html(res, par)
                if (Utils.compareStrings(Utils.ifNotNull(self.typname, ""), "Mail", True) != 0): 
                    print("</b>", end="", file=res)
                else: 
                    print("</i>", end="", file=res)
            if (par is not None): 
                par._out_footnotes(res)
        if (self.body is not None): 
            self.body.get_html(res, par)
            if (par is not None): 
                par._out_footnotes(res)
        if (self.tail is not None): 
            print("<i>", end="", file=res)
            self.tail.get_html(res, par)
            print("</i>", end="", file=res)
            if (par is not None): 
                par._out_footnotes(res)
        if (self.appendix is not None): 
            self.appendix.get_html(res, par)
            if (par is not None): 
                par._out_footnotes(res)
        print("</{0}>".format(tag_), end="", file=res, flush=True)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("docblock")
        self._write_xml_attrs(xml0_)
        if (self.typname is not None): 
            xml0_.write_attribute_string("typname", self.typname)
        if (self.number is not None): 
            xml0_.write_attribute_string("num", MiscHelper.correct_xml_value(self.number))
        if (self.typ != UnitextDocblockType.UNDEFINED): 
            xml0_.write_attribute_string("typ", Utils.enumToString(self.typ).lower())
        if (self.__m_is_inline): 
            xml0_.write_attribute_string("inline", "true")
        if (self.ext_block_id is not None): 
            xml0_.write_attribute_string("extblockid", self.ext_block_id)
        if (self.expired): 
            xml0_.write_attribute_string("expired", "true")
        if (self.head is not None): 
            xml0_.write_start_element("head")
            self.head.get_xml(xml0_)
            xml0_.write_end_element()
        if (self.body is not None): 
            xml0_.write_start_element("body")
            self.body.get_xml(xml0_)
            xml0_.write_end_element()
        if (self.tail is not None): 
            xml0_.write_start_element("tail")
            self.tail.get_xml(xml0_)
            xml0_.write_end_element()
        if (self.appendix is not None): 
            xml0_.write_start_element("appendix")
            self.appendix.get_xml(xml0_)
            xml0_.write_end_element()
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
        super().from_xml(xml0_)
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "typname"): 
                    self.typname = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "num"): 
                    self.number = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "extblockid"): 
                    self.ext_block_id = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "expired"): 
                    self.expired = a[1] == "true"
                elif (Utils.getXmlAttrLocalName(a) == "inline"): 
                    self.__m_is_inline = a[1] == "true"
                elif (Utils.getXmlAttrLocalName(a) == "typ"): 
                    try: 
                        self.typ = (Utils.valToEnum(a[1], UnitextDocblockType))
                    except Exception as ex545: 
                        pass
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "head"): 
                for xx in x: 
                    self.head = (Utils.asObjectOrNull(UnitextHelper.create_item(xx), UnitextContainer))
                    if (self.head is not None): 
                        self.head.typ = UnitextContainerType.HEAD
                    break
            elif (Utils.getXmlLocalName(x) == "body"): 
                for xx in x: 
                    self.body = UnitextHelper.create_item(xx)
                    break
            elif (Utils.getXmlLocalName(x) == "appendix"): 
                for xx in x: 
                    self.appendix = UnitextHelper.create_item(xx)
                    break
            elif (Utils.getXmlLocalName(x) == "tail"): 
                for xx in x: 
                    self.tail = (Utils.asObjectOrNull(UnitextHelper.create_item(xx), UnitextContainer))
                    if (self.tail is not None): 
                        self.tail.typ = UnitextContainerType.TAIL
                    break
    
    @property
    def is_whitespaces(self) -> bool:
        return False
    
    def get_all_items(self, res : typing.List['UnitextItem'], lev : int) -> None:
        if (res is not None): 
            res.append(self)
        if (self.head is not None): 
            if (self.head in self.head.children): 
                pass
            elif (self in self.head.children): 
                pass
            else: 
                self.head.parent = (self)
                self.head.get_all_items(res, lev + 1)
        if (self.body is not None): 
            self.body.parent = (self)
            self.body.get_all_items(res, lev + 1)
        if (self.tail is not None): 
            self.tail.parent = (self)
            self.tail.get_all_items(res, lev + 1)
        if (self.appendix is not None): 
            self.appendix.parent = (self)
            self.appendix.get_all_items(res, lev + 1)
    
    def _add_plain_text_pos(self, d : int) -> None:
        super()._add_plain_text_pos(d)
        if (self.head is not None): 
            self.head._add_plain_text_pos(d)
        if (self.body is not None): 
            self.body._add_plain_text_pos(d)
        if (self.tail is not None): 
            self.tail._add_plain_text_pos(d)
        if (self.appendix is not None): 
            self.appendix._add_plain_text_pos(d)
    
    def _correct(self, typ_ : 'LocCorrTyp', data : object) -> None:
        if (self.head is not None): 
            self.head._correct(typ_, data)
        if (self.body is not None): 
            self.body._correct(typ_, data)
        if (self.tail is not None): 
            self.tail._correct(typ_, data)
        if (self.appendix is not None): 
            self.appendix._correct(typ_, data)
    
    def _set_default_text_pos(self, cp : int, res : io.StringIO) -> None:
        self.begin_char = cp.value
        if (self.head is not None): 
            self.head._set_default_text_pos(cp, res)
            self.head.parent = (self)
        if (self.body is not None): 
            self.body._set_default_text_pos(cp, res)
            self.body.parent = (self)
        if (self.tail is not None): 
            self.tail._set_default_text_pos(cp, res)
            self.tail.parent = (self)
        if (self.appendix is not None): 
            self.appendix._set_default_text_pos(cp, res)
            self.appendix.parent = (self)
        self.end_char = (cp.value - 1)
    
    def optimize(self, is_content : bool, pars : 'CreateDocumentParam') -> 'UnitextItem':
        if (self.head is not None): 
            if (self.head in self.head.children): 
                pass
            self.head = (Utils.asObjectOrNull(self.head.optimize(False, pars), UnitextContainer))
        if (self.body is not None): 
            self.body = self.body.optimize(True, pars)
        if (self.tail is not None): 
            self.tail = (Utils.asObjectOrNull(self.tail.optimize(False, pars), UnitextContainer))
        if (self.appendix is not None): 
            self.appendix = self.appendix.optimize(True, pars)
        return self
    
    def _append_child(self, it : 'UnitextItem') -> bool:
        if (self.appendix is not None): 
            cnt = Utils.asObjectOrNull(self.appendix, UnitextContainer)
            if (cnt is None): 
                cnt = UnitextContainer._new546(self.body.begin_char)
                cnt.children.append(self.body)
                self.appendix = (cnt)
            cnt.children.append(it)
            self.body.end_char = it.end_char
            self.end_char = self.body.end_char
            return True
        if (self.tail is not None): 
            self.tail.children.append(it)
            self.tail.end_char = it.end_char
            self.end_char = self.tail.end_char
            return True
        if (self.body is not None): 
            cnt = Utils.asObjectOrNull(self.body, UnitextContainer)
            if (cnt is None): 
                cnt = UnitextContainer._new546(self.body.begin_char)
                cnt.children.append(self.body)
                self.body = (cnt)
            cnt.children.append(it)
            self.body.end_char = it.end_char
            self.end_char = self.body.end_char
            return True
        if (self.head is not None): 
            self.head.children.append(it)
            self.head.end_char = it.end_char
            self.end_char = self.head.end_char
            return True
        return False
    
    @staticmethod
    def _new32(_arg1 : str) -> 'UnitextDocblock':
        res = UnitextDocblock()
        res.typname = _arg1
        return res
    
    @staticmethod
    def _new378(_arg1 : int, _arg2 : int) -> 'UnitextDocblock':
        res = UnitextDocblock()
        res.begin_char = _arg1
        res.end_char = _arg2
        return res