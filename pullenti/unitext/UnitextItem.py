# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.unitext.GetPlaintextParam import GetPlaintextParam
from pullenti.util.MiscHelper import MiscHelper

class UnitextItem:
    """ Базовый класс для всех элементов Unitext:
    UnitextPlaintext, UnitextContainer, UnitextTable, UnitextTablecell, UnitextList, UnitextListitem,
    UnitextNewline, UnitextPagebreak, UnitextFootnote, UnitextImage, UnitextHyperlink, UnitextComment,
    UnitextDocblock и UnitextMisc.
    Базовый класс элементов Unitext
    
    """
    
    def __init__(self) -> None:
        self.tag = None;
        self.begin_char = 0
        self.end_char = 0
        self.parent = None;
        self.page_section_id = None;
        self.source_info = None
        self.id0_ = None;
        self.html_title = None;
        self.ext_data = None;
        self._m_styled_frag = None;
    
    def _get_plaintext_ns_pos(self, txt : str) -> int:
        # Получить первую непробельную позицию
        if (txt is not None): 
            p = self.begin_char
            while p <= self.end_char and (p < len(txt)): 
                if (not Utils.isWhitespace(txt[p])): 
                    if (txt[p] != (chr(7)) and txt[p] != (chr(0x1E)) and txt[p] != (chr(0x1F))): 
                        return p
                p += 1
        return self.begin_char
    
    def _get_plaintext_ns_pos1(self, txt : str) -> int:
        # Получить последнюю непробельную позицию
        if (txt is not None): 
            p = self.end_char
            while p >= 0 and (p < len(txt)): 
                if (not Utils.isWhitespace(txt[p])): 
                    if (txt[p] != (chr(7)) and txt[p] != (chr(0x1E)) and txt[p] != (chr(0x1F))): 
                        return p
                p -= 1
        return self.end_char
    
    @property
    def page_section(self) -> 'UnitextPagesection':
        """ Страничная секция (параметры страницы и колонтитулы) """
        from pullenti.unitext.UnitextDocument import UnitextDocument
        from pullenti.unitext.UnitextPagesection import UnitextPagesection
        id0__ = None
        it = self
        while it is not None: 
            if (it.page_section_id is not None and id0__ is None): 
                id0__ = it.page_section_id
            if (isinstance(it, UnitextPagesection)): 
                return Utils.asObjectOrNull(it, UnitextPagesection)
            doc = Utils.asObjectOrNull(it, UnitextDocument)
            if (doc is not None): 
                for s in doc.sections: 
                    if (s.id0_ == id0__): 
                        return s
            it = it.parent
        return None
    
    def clone(self) -> 'UnitextItem':
        return None
    
    def _clone_from(self, it : 'UnitextItem') -> None:
        self.begin_char = it.begin_char
        self.end_char = it.end_char
        self.source_info = it.source_info
        self.html_title = it.html_title
        self.id0_ = it.id0_
        self.ext_data = it.ext_data
        self.page_section_id = it.page_section_id
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        """ Сгенерировать плоский текст
        
        Args:
            res(io.StringIO): результат запишет сюда
            pars(GetPlaintextParam): параметры
        """
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
    
    def get_plaintext_string(self, pars : 'GetPlaintextParam'=None) -> str:
        """ Сгенерировать плоский текст текущего элемента и всех его подэлементов
        
        Args:
            pars(GetPlaintextParam): параметры генерации
        
        Returns:
            str: результат
        """
        from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
        return UnitextHelper.get_plaintext(self, pars)
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        """ Сгенерировать HTML
        
        Args:
            res(io.StringIO): результат
            par(GetHtmlParam): параметры генерации
        """
        pass
    
    def get_html_string(self, par : 'GetHtmlParam'=None) -> str:
        """ Сгенерировать HTML
        
        Args:
            par(GetHtmlParam): параметры генерации
        
        Returns:
            str: результат
        """
        res = io.StringIO()
        self.get_html(res, par)
        return Utils.toStringStringIO(res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("unknown")
        xml0_.write_end_element()
    
    def _write_xml_attrs(self, xml0_ : XmlWriter) -> None:
        if (self.id0_ is not None): 
            xml0_.write_attribute_string("id", MiscHelper.correct_xml_value(self.id0_))
        if (self.begin_char > 0 or self.end_char > 0): 
            xml0_.write_attribute_string("b", str(self.begin_char))
            xml0_.write_attribute_string("e", str(self.end_char))
        if (self.html_title is not None): 
            xml0_.write_attribute_string("title", MiscHelper.correct_xml_value(self.html_title))
        if (self.page_section_id is not None): 
            xml0_.write_attribute_string("section", self.page_section_id)
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "id"): 
                    self.id0_ = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "b"): 
                    self.begin_char = int(a[1])
                elif (Utils.getXmlAttrLocalName(a) == "e"): 
                    self.end_char = int(a[1])
                elif (Utils.getXmlAttrLocalName(a) == "l"): 
                    self.end_char = ((self.begin_char + int(a[1])) - 1)
                elif (Utils.getXmlAttrLocalName(a) == "t" or Utils.getXmlAttrLocalName(a) == "title"): 
                    self.html_title = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "section"): 
                    self.page_section_id = a[1]
    
    def optimize(self, is_content : bool, pars : 'CreateDocumentParam') -> 'UnitextItem':
        return self
    
    def get_all_items(self, res : typing.List['UnitextItem'], lev : int) -> None:
        """ Получить список всех элементов (этот и все нижележащий)
        
        Args:
            res(typing.List[UnitextItem]): 
        """
        if (lev > 40): 
            pass
        if (res is not None): 
            res.append(self)
    
    @property
    def is_whitespaces(self) -> bool:
        """ Только из "пустых" символов и переходов на новую строку """
        return False
    
    @property
    def is_inline(self) -> bool:
        """ Объект не содержит блочных объектов и разрывов строк """
        return True
    @is_inline.setter
    def is_inline(self, value) -> bool:
        return value
    
    _m_def_params = None
    
    def _add_plain_text_pos(self, d : int) -> None:
        self.begin_char += d
        self.end_char += d
    
    def _correct(self, typ : 'LocCorrTyp', data : object) -> None:
        pass
    
    @property
    def _inner_tag(self) -> str:
        # Используется внутренним образом
        return None
    
    def find_by_id(self, id0__ : str) -> 'UnitextItem':
        """ Поиск среди текущего элемента и его внутренних элементов
        
        Args:
            id0__(str): идентификатор для поиска
        
        Returns:
            UnitextItem: результат
        """
        if (self.id0_ == id0__): 
            return self
        return None
    
    def _replace_child(self, old : 'UnitextItem', ne : 'UnitextItem') -> bool:
        return False
    
    def _set_default_text_pos(self, cp : int, res : io.StringIO) -> None:
        self.begin_char = cp.value
        self.end_char = (cp.value - 1)
    
    def get_styled_fragment(self, text_pos : int=-1) -> 'UnitextStyledFragment':
        """ Получить ссылку на стилевой фрагмент для указанной текстовой позиции.
        Отметим, что для элемента BeginChar..EndChar может покрывать или пересекаться
        с несколькими стилевыми фрагментами.
        
        Args:
            text_pos(int): позиция текста в системе BeginChar..EndChar (-1 - для первой позиции текущего элемента)
        
        Returns:
            UnitextStyledFragment: фрагмент, наиболее удалённый в иерархии фрагментов и содержащий указанную позицию
        """
        if ((text_pos < 0) and self._m_styled_frag is not None): 
            return self._m_styled_frag
        if (text_pos < 0): 
            text_pos = self.begin_char
        it = self
        while it is not None: 
            if (it._m_styled_frag is not None): 
                res = it._m_styled_frag.find_by_char_position(text_pos)
                if (res is not None): 
                    if (self._m_styled_frag is None): 
                        self._m_styled_frag = res
                    return res
            it = it.parent
        return None
    
    # static constructor for class UnitextItem
    @staticmethod
    def _static_ctor():
        UnitextItem._m_def_params = GetPlaintextParam()

UnitextItem._static_ctor()