# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.unitext.UnitextStyledFragmentType import UnitextStyledFragmentType
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextList import UnitextList
from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper

class UnitextTablecell(UnitextItem):
    """ Ячейка таблицы """
    
    def __init__(self) -> None:
        super().__init__()
        self.__colbegin = 0
        self.__colend = 0
        self.__rowbegin = 0
        self.__rowend = 0
        self.content = None;
        self.is_psevdo = False
    
    @property
    def col_begin(self) -> int:
        """ Начальный столбец ячейки """
        return self.__colbegin
    @col_begin.setter
    def col_begin(self, value) -> int:
        self.__colbegin = value
        return self.__colbegin
    
    @property
    def col_end(self) -> int:
        """ Конечный столбец ячейки """
        return self.__colend
    @col_end.setter
    def col_end(self, value) -> int:
        self.__colend = value
        return self.__colend
    
    @property
    def row_begin(self) -> int:
        """ Начальная строка ячейки """
        return self.__rowbegin
    @row_begin.setter
    def row_begin(self, value) -> int:
        self.__rowbegin = value
        return self.__rowbegin
    
    @property
    def row_end(self) -> int:
        """ Конечная строка ячейки """
        return self.__rowend
    @row_end.setter
    def row_end(self, value) -> int:
        self.__rowend = value
        return self.__rowend
    
    def clone(self) -> 'UnitextItem':
        res = UnitextTablecell()
        res._clone_from(self)
        res.col_begin = self.col_begin
        res.col_end = self.col_end
        res.row_begin = self.row_begin
        res.row_end = self.row_end
        if (self.content is not None): 
            res.content = self.content.clone()
        res.is_psevdo = self.is_psevdo
        return res
    
    @property
    def is_inline(self) -> bool:
        return False
    
    @property
    def _inner_tag(self) -> str:
        return "tcell"
    
    def find_by_id(self, id0__ : str) -> 'UnitextItem':
        if (self.id0_ == id0__): 
            return self
        res = None
        if (self.content is not None): 
            res = self.content.find_by_id(id0__)
            if ((res) is not None): 
                return res
        return None
    
    def optimize(self, is_content : bool, pars : 'CreateDocumentParam') -> 'UnitextItem':
        if (self.content is not None): 
            self.content = self.content.optimize(True, pars)
        if (self.content is not None and self.content.is_whitespaces): 
            self.content = (None)
        li = Utils.asObjectOrNull(self.content, UnitextList)
        if ((li is not None and len(li.items) == 1 and li.items[0].content is None) and li.items[0].prefix is not None): 
            self.content = li.items[0].prefix
        return self
    
    def __str__(self) -> str:
        return "Cell{0} {1}{2} {3} {4}".format(("?" if self.is_psevdo else ""), self.col_begin, ("-{0}".format(self.col_end) if self.col_begin < self.col_end else ""), (" (rows {0}-{1})".format(self.row_begin, self.row_end) if self.row_begin < self.row_end else ""), ("" if self.content is None else str(self.content)))
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
        if (pars is None): 
            pars = UnitextItem._m_def_params
        if (self.content is not None): 
            i0 = res.tell()
            self.content.get_plaintext(res, pars)
            for i in range(res.tell() - 1, i0 - 1, -1):
                if ((Utils.isWhitespace(Utils.getCharAtStringIO(res, i)) or Utils.getCharAtStringIO(res, i) == (chr(7)) or Utils.getCharAtStringIO(res, i) == '\t') or Utils.getCharAtStringIO(res, i) == '\f'): 
                    Utils.setLengthStringIO(res, i)
                else: 
                    break
        if (Utils.isNullOrEmpty(pars.table_cell_end)): 
            print(Utils.ifNotNull(pars.new_line, ""), end="", file=res)
        else: 
            if (self.col_begin < self.col_end): 
                i = 0
                while i < ((self.col_end - self.col_begin)): 
                    print('\t', end="", file=res)
                    i += 1
            if (self.row_begin < self.row_end): 
                i = 0
                while i < ((self.row_end - self.row_begin)): 
                    print('\f', end="", file=res)
                    i += 1
            if (pars is None): 
                print(chr(7), end="", file=res)
            else: 
                print(Utils.ifNotNull(pars.table_cell_end, ""), end="", file=res)
        if (pars is not None and pars.set_positions): 
            self.end_char = (res.tell() - 1)
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (not par.call_before(self, res)): 
            return
        print("<td valign=\"top\"", end="", file=res)
        if (self.row_end > self.row_begin): 
            print(" rowspan=\"{0}\"".format((self.row_end - self.row_begin) + 1), end="", file=res, flush=True)
        if (self.col_end > self.col_begin): 
            print(" colspan=\"{0}\"".format((self.col_end - self.col_begin) + 1), end="", file=res, flush=True)
        if (self.id0_ is not None): 
            print(" id=\"{0}\"".format(self.id0_), end="", file=res, flush=True)
            if (par is not None and self.id0_ in par.styles): 
                print(" style=\"{0}\"".format(par.styles[self.id0_]), end="", file=res, flush=True)
            elif (par is not None and par.out_styles and self.get_styled_fragment(-1) is not None): 
                fr = self.get_styled_fragment(-1)
                if (fr is not None and fr.typ != UnitextStyledFragmentType.TABLECELL): 
                    fr = fr.parent
                if ((fr is not None and fr.typ == UnitextStyledFragmentType.TABLECELL and fr.style_id > 0) and fr.style is not None): 
                    print(" style=\"", end="", file=res)
                    fr.style.get_html(res)
                    print("\"", end="", file=res)
        print(">", end="", file=res)
        if (self.content is None): 
            print("&nbsp;", end="", file=res)
        else: 
            self.content.get_html(res, par)
        print("</td>", end="", file=res)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("cell")
        self._write_xml_attrs(xml0_)
        if (self.is_psevdo): 
            xml0_.write_attribute_string("psevdo", "true")
        xml0_.write_attribute_string("row", str(self.row_begin))
        if (self.row_end > self.row_begin): 
            xml0_.write_attribute_string("rowspan", str(((self.row_end - self.row_begin) + 1)))
        xml0_.write_attribute_string("col", str(self.col_begin))
        if (self.col_end > self.col_begin): 
            xml0_.write_attribute_string("colspan", str(((self.col_end - self.col_begin) + 1)))
        if (self.content is not None): 
            self.content.get_xml(xml0_)
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        super().from_xml(xml0_)
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "row"): 
                    self.row_begin = self.row_end = int(a[1])
                elif (Utils.getXmlAttrLocalName(a) == "col"): 
                    self.col_begin = self.col_end = int(a[1])
                elif (Utils.getXmlAttrLocalName(a) == "rowspan"): 
                    self.row_end = (self.row_begin + int(a[1])) - 1
                elif (Utils.getXmlAttrLocalName(a) == "colspan"): 
                    self.col_end = (self.col_begin + int(a[1])) - 1
                elif (Utils.getXmlAttrLocalName(a) == "psevdo"): 
                    self.is_psevdo = True
        for x in xml0_: 
            self.content = UnitextHelper.create_item(x)
            if (self.content is not None): 
                break
    
    def get_all_items(self, res : typing.List['UnitextItem'], lev : int) -> None:
        if (res is not None): 
            res.append(self)
        if (self.content is not None): 
            self.content.parent = (self)
            self.content.get_all_items(res, lev + 1)
    
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
        if (self.content is not None): 
            self.content._set_default_text_pos(cp, res)
            self.content.parent = (self)
        self.end_char = cp.value
        cp.value += 1
        if (res is not None): 
            print("{0}".format(chr(7)), end="", file=res, flush=True)
    
    @staticmethod
    def _new75(_arg1 : int, _arg2 : int, _arg3 : int, _arg4 : int, _arg5 : object) -> 'UnitextTablecell':
        res = UnitextTablecell()
        res.col_begin = _arg1
        res.col_end = _arg2
        res.row_begin = _arg3
        res.row_end = _arg4
        res.tag = _arg5
        return res
    
    @staticmethod
    def _new580(_arg1 : bool, _arg2 : int, _arg3 : int, _arg4 : int, _arg5 : int) -> 'UnitextTablecell':
        res = UnitextTablecell()
        res.is_psevdo = _arg1
        res.col_begin = _arg2
        res.col_end = _arg3
        res.row_begin = _arg4
        res.row_end = _arg5
        return res
    
    @staticmethod
    def _new581(_arg1 : 'UnitextItem', _arg2 : int, _arg3 : int, _arg4 : int, _arg5 : int) -> 'UnitextTablecell':
        res = UnitextTablecell()
        res.content = _arg1
        res.col_begin = _arg2
        res.col_end = _arg3
        res.row_begin = _arg4
        res.row_end = _arg5
        return res