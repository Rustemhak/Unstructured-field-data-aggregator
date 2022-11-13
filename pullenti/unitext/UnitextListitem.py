# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.unitext.GetPlaintextParam import GetPlaintextParam
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextList import UnitextList

class UnitextListitem(UnitextItem):
    """ Элемент списка """
    
    def __init__(self) -> None:
        super().__init__()
        self.prefix = None;
        self.content = None;
        self.sublist = None;
    
    __m_pars = None
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.prefix is not None): 
            print("{0}: ".format(str(self.prefix)), end="", file=res, flush=True)
        if (self.content is not None): 
            print(str(self.content), end="", file=res)
        if (self.sublist is not None): 
            print(" + {0}".format(str(self.sublist)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def clone(self) -> 'UnitextItem':
        res = UnitextListitem()
        res._clone_from(self)
        if (self.prefix is not None): 
            res.prefix = self.prefix.clone()
        if (self.content is not None): 
            res.content = self.content.clone()
        if (self.sublist is not None): 
            res.sublist = (Utils.asObjectOrNull(self.sublist.clone(), UnitextList))
        return res
    
    @property
    def is_inline(self) -> bool:
        return False
    
    @property
    def _inner_tag(self) -> str:
        return "litm"
    
    def find_by_id(self, id0__ : str) -> 'UnitextItem':
        if (self.id0_ == id0__): 
            return self
        res = None
        if (self.prefix is not None): 
            res = self.prefix.find_by_id(id0__)
            if ((res) is not None): 
                return res
        if (self.content is not None): 
            res = self.content.find_by_id(id0__)
            if ((res) is not None): 
                return res
        if (self.sublist is not None): 
            res = self.sublist.find_by_id(id0__)
            if ((res) is not None): 
                return res
        return None
    
    def get_all_items(self, res : typing.List['UnitextItem'], lev : int) -> None:
        if (res is not None): 
            res.append(self)
        if (self.prefix is not None): 
            self.prefix.parent = (self)
            self.prefix.get_all_items(res, lev + 1)
        if (self.content is not None): 
            self.content.parent = (self)
            self.content.get_all_items(res, lev + 1)
        if (self.sublist is not None): 
            self.sublist.parent = (self)
            self.sublist.get_all_items(res, lev + 1)
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
        if (pars is None): 
            pars = UnitextItem._m_def_params
        if (self.prefix is not None): 
            self.prefix.get_plaintext(res, pars)
            print(' ', end="", file=res)
        if (self.content is not None): 
            self.content.get_plaintext(res, pars)
        print(Utils.ifNotNull(pars.new_line, ""), end="", file=res)
        if (self.sublist is not None): 
            self.sublist.get_plaintext(res, pars)
        if (pars is not None and pars.set_positions): 
            self.end_char = (res.tell() - 1)
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (not par.call_before(self, res)): 
            return
        print("\r\n<LI", end="", file=res)
        if (self.id0_ is not None): 
            print(" id=\"{0}\"".format(self.id0_), end="", file=res, flush=True)
            if (par is not None and self.id0_ in par.styles): 
                print(" style=\"{0}\"".format(par.styles[self.id0_]), end="", file=res, flush=True)
        print(">", end="", file=res)
        if (self.prefix is not None): 
            self.prefix.get_html(res, par)
            print(' ', end="", file=res)
        if (self.content is not None): 
            self.content.get_html(res, par)
        if (self.sublist is not None): 
            self.sublist.get_html(res, par)
        print("</LI>", end="", file=res)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("listitem")
        self._write_xml_attrs(xml0_)
        if (self.prefix is not None): 
            xml0_.write_start_element("prefix")
            self.prefix.get_xml(xml0_)
            xml0_.write_end_element()
        if (self.content is not None): 
            self.content.get_xml(xml0_)
        if (self.sublist is not None): 
            self.sublist.get_xml(xml0_)
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
        super().from_xml(xml0_)
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "prefix"): 
                for xx in x: 
                    self.prefix = UnitextHelper.create_item(xx)
                    break
            else: 
                it = UnitextHelper.create_item(x)
                if (isinstance(it, UnitextList)): 
                    self.sublist = (Utils.asObjectOrNull(it, UnitextList))
                elif (it is not None): 
                    self.content = it
    
    def optimize(self, is_content : bool, pars : 'CreateDocumentParam') -> 'UnitextItem':
        if (self.prefix is not None): 
            self.prefix = self.prefix.optimize(True, pars)
        if (self.content is not None): 
            self.content = self.content.optimize(True, pars)
        if (self.content is not None and self.content.is_whitespaces): 
            self.content = (None)
        if (self.sublist is not None): 
            self.sublist = (Utils.asObjectOrNull(self.sublist.optimize(False, pars), UnitextList))
        return self
    
    def _add_plain_text_pos(self, d : int) -> None:
        super()._add_plain_text_pos(d)
        if (self.prefix is not None): 
            self.prefix._add_plain_text_pos(d)
        if (self.content is not None): 
            self.content._add_plain_text_pos(d)
        if (self.sublist is not None): 
            self.sublist._add_plain_text_pos(d)
    
    def _correct(self, typ : 'LocCorrTyp', data : object) -> None:
        if (self.prefix is not None): 
            self.prefix._correct(typ, data)
        if (self.content is not None): 
            self.content._correct(typ, data)
        if (self.sublist is not None): 
            self.sublist._correct(typ, data)
    
    def _replace_child(self, old : 'UnitextItem', ne : 'UnitextItem') -> bool:
        if (self.content != old): 
            return False
        self.content = ne
        ne.parent = (self)
        return True
    
    def _set_default_text_pos(self, cp : int, res : io.StringIO) -> None:
        self.begin_char = cp.value
        if (self.prefix is not None): 
            self.prefix._set_default_text_pos(cp, res)
            self.prefix.parent = (self)
        if (self.content is not None): 
            self.content._set_default_text_pos(cp, res)
            self.content.parent = (self)
        cp.value += 1
        if (res is not None): 
            print('\n', end="", file=res)
        if (self.sublist is not None): 
            self.sublist._set_default_text_pos(cp, res)
            self.sublist.parent = (self)
        self.end_char = (cp.value - 1)
    
    @staticmethod
    def _new349(_arg1 : 'UnitextItem') -> 'UnitextListitem':
        res = UnitextListitem()
        res.content = _arg1
        return res
    
    # static constructor for class UnitextListitem
    @staticmethod
    def _static_ctor():
        UnitextListitem.__m_pars = GetPlaintextParam()

UnitextListitem._static_ctor()