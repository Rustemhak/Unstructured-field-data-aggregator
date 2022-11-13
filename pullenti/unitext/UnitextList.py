# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Xml import XmlWriter

from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextNewline import UnitextNewline
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak

class UnitextList(UnitextItem):
    """ Список """
    
    def __init__(self) -> None:
        super().__init__()
        self.items = list()
        self.unorder_prefix = None;
        self.level = 0
    
    def optimize(self, is_content : bool, pars : 'CreateDocumentParam') -> 'UnitextItem':
        from pullenti.unitext.UnitextListitem import UnitextListitem
        from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
        for it in self.items: 
            it.parent = (self)
            it.optimize(False, pars)
            if ((isinstance(it.content, UnitextList)) and it.sublist is None and it.content.level == (self.level + 1)): 
                it.sublist = (Utils.asObjectOrNull(it.content, UnitextList))
                it.content = (None)
                continue
            if (it.sublist is not None): 
                continue
            cnt = Utils.asObjectOrNull(it.content, UnitextContainer)
            if (cnt is not None and (isinstance(cnt.children[len(cnt.children) - 1], UnitextList)) and cnt.children[len(cnt.children) - 1].level == (self.level + 1)): 
                it.sublist = (Utils.asObjectOrNull(cnt.children[len(cnt.children) - 1], UnitextList))
                del cnt.children[len(cnt.children) - 1]
                it.content = it.content.optimize(True, pars)
        if (len(self.items) == 0): 
            return None
        if (self.unorder_prefix is None): 
            pre = None
            ok = True
            for it in self.items: 
                if (it.prefix is not None): 
                    if (pre is None): 
                        pre = UnitextHelper.get_plaintext(it.prefix, None)
                    elif (pre != UnitextHelper.get_plaintext(it.prefix, None)): 
                        ok = False
                        break
            if ((ok and pre is not None and len(pre) == 1) and not str.isalnum(pre[0])): 
                self.unorder_prefix = pre
                for it in self.items: 
                    it.prefix = (None)
        else: 
            for it in self.items: 
                it.prefix = (None)
        if (len(self.items) == 1 and ((self.level == 0 or not (isinstance(self.parent, UnitextListitem))))): 
            if (self.__is_all_list_items_single()): 
                ccc = UnitextContainer()
                ccc.id0_ = self.id0_
                li = self
                while li is not None: 
                    if (len(ccc.children) > 0): 
                        ccc.children.append(UnitextNewline())
                    it = li.items[0]
                    if (ccc.id0_ is None): 
                        ccc.id0_ = it.id0_
                    if (it.prefix is not None and it.content is not None): 
                        ccc.children.append(it.prefix)
                        ccc.children.append(UnitextPlaintext._new564(" ", it.prefix.end_char, it.prefix.end_char))
                        ccc.children.append(it.content)
                    elif (it.prefix is not None): 
                        ccc.children.append(it.prefix)
                    elif (it.content is not None): 
                        ccc.children.append(it.content)
                    li = li.items[0].sublist
                if (isinstance(self.parent, UnitextContainer)): 
                    par = Utils.asObjectOrNull(self.parent, UnitextContainer)
                    i = par.get_child_index_of(self)
                    if (i >= 0): 
                        if (((i + 1) < len(par.children)) and (((isinstance(par.children[i + 1], UnitextNewline)) or (isinstance(par.children[i + 1], UnitextPagebreak))))): 
                            pass
                        else: 
                            ccc.children.append(UnitextNewline())
                for ch in ccc.children: 
                    ch.parent = (ccc)
                return ccc.optimize(True, pars)
        return self
    
    def __is_all_list_items_single(self) -> bool:
        if (len(self.items) > 1): 
            return False
        it = self.items[0]
        if (it.sublist is None): 
            return True
        return it.sublist.__is_all_list_items_single()
    
    def __str__(self) -> str:
        return "{0}List ({1} items, {2} level)".format(("" if self.unorder_prefix is None else "Unordered ({0})".format(self.unorder_prefix)), len(self.items), self.level)
    
    def clone(self) -> 'UnitextItem':
        from pullenti.unitext.UnitextListitem import UnitextListitem
        res = UnitextList()
        res._clone_from(self)
        for it in self.items: 
            res.items.append(Utils.asObjectOrNull(it.clone(), UnitextListitem))
        res.unorder_prefix = self.unorder_prefix
        res.level = self.level
        return res
    
    def get_all_items(self, res : typing.List['UnitextItem'], lev : int) -> None:
        if (res is not None): 
            res.append(self)
        for it in self.items: 
            it.parent = (self)
            it.get_all_items(res, lev + 1)
    
    @property
    def is_inline(self) -> bool:
        return False
    
    @property
    def _inner_tag(self) -> str:
        return "lst"
    
    def find_by_id(self, id0__ : str) -> 'UnitextItem':
        if (self.id0_ == id0__): 
            return self
        for it in self.items: 
            res = it.find_by_id(id0__)
            if (res is not None): 
                return res
        return None
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam'=None) -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
        for it in self.items: 
            ii = 0
            while ii < self.level: 
                print('\t', end="", file=res)
                ii += 1
            if (it == self.items[0] and pars is not None and pars.set_positions): 
                self.begin_char = res.tell()
            if (self.unorder_prefix is not None): 
                print("{0} ".format(self.unorder_prefix), end="", file=res, flush=True)
            it.get_plaintext(res, pars)
        if (pars is not None and pars.set_positions): 
            self.end_char = (res.tell() - 1)
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (not par.call_before(self, res)): 
            return
        if ((isinstance(self.parent, UnitextContainer)) and self.parent.typ == UnitextContainerType.HEAD and len(self.items) == 1): 
            it = self.items[0]
            if (it.prefix is not None): 
                it.prefix.get_html(res, par)
                print("&nbsp;", end="", file=res)
            if (it.content is not None): 
                it.content.get_html(res, par)
            if (it.sublist is not None): 
                it.sublist.get_html(res, par)
        else: 
            print("\r\n<UL", end="", file=res)
            if (self.id0_ is not None): 
                print(" id=\"{0}\"".format(self.id0_), end="", file=res, flush=True)
                if (par is not None and self.id0_ in par.styles): 
                    print(" style=\"{0}\"".format(par.styles[self.id0_]), end="", file=res, flush=True)
            print(">", end="", file=res)
            for it in self.items: 
                it.get_html(res, par)
            print("\r\n</UL>", end="", file=res)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("list")
        self._write_xml_attrs(xml0_)
        if (self.unorder_prefix is not None): 
            xml0_.write_attribute_string("pref", MiscHelper.correct_xml_value(self.unorder_prefix))
        if (self.level > 0): 
            xml0_.write_attribute_string("level", str(self.level))
        for it in self.items: 
            it.get_xml(xml0_)
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        from pullenti.unitext.UnitextListitem import UnitextListitem
        from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
        super().from_xml(xml0_)
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "pref"): 
                    self.unorder_prefix = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "level"): 
                    n = 0
                    wrapn565 = RefOutArgWrapper(0)
                    inoutres566 = Utils.tryParseInt(a[1], wrapn565)
                    n = wrapn565.value
                    if (inoutres566): 
                        self.level = n
        for x in xml0_: 
            it = UnitextHelper.create_item(x)
            if (isinstance(it, UnitextListitem)): 
                self.items.append(Utils.asObjectOrNull(it, UnitextListitem))
    
    def _add_plain_text_pos(self, d : int) -> None:
        super()._add_plain_text_pos(d)
        for it in self.items: 
            it._add_plain_text_pos(d)
    
    def _correct(self, typ : 'LocCorrTyp', data : object) -> None:
        for it in self.items: 
            it._correct(typ, data)
    
    def _set_default_text_pos(self, cp : int, res : io.StringIO) -> None:
        self.begin_char = cp.value
        for it in self.items: 
            it._set_default_text_pos(cp, res)
            it.parent = (self)
        self.end_char = (cp.value - 1)
    
    @staticmethod
    def _new57(_arg1 : int) -> 'UnitextList':
        res = UnitextList()
        res.level = _arg1
        return res
    
    @staticmethod
    def _new351(_arg1 : int, _arg2 : object) -> 'UnitextList':
        res = UnitextList()
        res.level = _arg1
        res.tag = _arg2
        return res
    
    @staticmethod
    def _new352(_arg1 : int, _arg2 : object, _arg3 : str) -> 'UnitextList':
        res = UnitextList()
        res.level = _arg1
        res.tag = _arg2
        res.page_section_id = _arg3
        return res