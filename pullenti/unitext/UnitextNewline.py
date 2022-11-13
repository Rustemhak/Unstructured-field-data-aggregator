# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.unitext.internal.uni.LocCorrTyp import LocCorrTyp
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextDocblock import UnitextDocblock

class UnitextNewline(UnitextItem):
    """ Переход на новую строку """
    
    def __init__(self) -> None:
        super().__init__()
        self.count = 1
    
    def __str__(self) -> str:
        return "NewLine ({0})".format(self.count)
    
    def clone(self) -> 'UnitextItem':
        res = UnitextNewline()
        res._clone_from(self)
        res.count = self.count
        return res
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
        i = 0
        while i < self.count: 
            print(Utils.ifNotNull((Utils.ifNotNull(pars, UnitextItem._m_def_params)).new_line, ""), end="", file=res)
            i += 1
        if (pars is not None and pars.set_positions): 
            self.end_char = (res.tell() - 1)
    
    @staticmethod
    def __is_all_upper(it : 'UnitextPlaintext') -> bool:
        if (it is None): 
            return False
        for ch in it.text: 
            if (str.isalpha(ch)): 
                if (not str.isupper(ch)): 
                    return False
        return True
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (not par.call_before(self, res)): 
            return
        is_dummy = False
        if (isinstance(self.parent, UnitextContainer)): 
            if (len(self.parent.children) < 1000): 
                ii = self.parent.get_child_index_of(self)
                if (ii > 0 and (ii < (len(self.parent.children) - 1))): 
                    cnt = Utils.asObjectOrNull(self.parent, UnitextContainer)
                    if (cnt.typ == UnitextContainerType.NAME): 
                        is_dummy = True
                        if ((ii == 1 and (isinstance(cnt.children[ii - 1], UnitextPlaintext)) and ((ii + 1) < len(cnt.children))) and (isinstance(cnt.children[ii + 1], UnitextPlaintext))): 
                            if (UnitextNewline.__is_all_upper(Utils.asObjectOrNull(cnt.children[ii - 1], UnitextPlaintext)) and not UnitextNewline.__is_all_upper(Utils.asObjectOrNull(cnt.children[ii + 1], UnitextPlaintext))): 
                                is_dummy = False
                    elif (isinstance(self.parent.parent, UnitextDocblock)): 
                        has_db = False
                        for ch in self.parent.children: 
                            if (isinstance(ch, UnitextDocblock)): 
                                has_db = True
                        if (not has_db): 
                            pass
        if (is_dummy): 
            print(" ", end="", file=res)
        else: 
            i = 0
            while i < self.count: 
                print("\r\n<BR/>", end="", file=res)
                i += 1
            if (par is not None): 
                par._out_footnotes(res)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("newline")
        self._write_xml_attrs(xml0_)
        if (self.count > 1): 
            xml0_.write_attribute_string("count", str(self.count))
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        super().from_xml(xml0_)
        if (xml0_.attrib is not None and Utils.getXmlAttrByName(xml0_.attrib, "count") is not None): 
            self.count = int(Utils.getXmlAttrByName(xml0_.attrib, "count")[1])
    
    @property
    def is_whitespaces(self) -> bool:
        return True
    
    @property
    def is_inline(self) -> bool:
        return False
    
    def _correct(self, typ : 'LocCorrTyp', data : object) -> None:
        if (typ == LocCorrTyp.MERGENEWLINES): 
            if (self.count == 2): 
                self.count = 1
    
    def _set_default_text_pos(self, cp : int, res : io.StringIO) -> None:
        self.begin_char = cp.value
        cp.value += self.count
        self.end_char = (cp.value - 1)
        if (res is not None): 
            i = 0
            while i < self.count: 
                print('\n', end="", file=res)
                i += 1
    
    @staticmethod
    def _new334(_arg1 : int, _arg2 : str) -> 'UnitextNewline':
        res = UnitextNewline()
        res.count = _arg1
        res.page_section_id = _arg2
        return res
    
    @staticmethod
    def _new346(_arg1 : str) -> 'UnitextNewline':
        res = UnitextNewline()
        res.page_section_id = _arg1
        return res
    
    @staticmethod
    def _new373(_arg1 : 'UnitextItem') -> 'UnitextNewline':
        res = UnitextNewline()
        res.parent = _arg1
        return res
    
    @staticmethod
    def _new578(_arg1 : object) -> 'UnitextNewline':
        res = UnitextNewline()
        res.tag = _arg1
        return res