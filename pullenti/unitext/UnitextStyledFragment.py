# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextStyledFragmentType import UnitextStyledFragmentType

class UnitextStyledFragment:
    """ Фрагмент, с которым связаны стили UnitextStyle (если их выделение реализовано для входного формата).
    Представляет собой иерархию.
    Стилевой фрагмент
    """
    
    def __init__(self) -> None:
        self.parent = None;
        self.children = list()
        self.__m_doc = None;
        self.typ = UnitextStyledFragmentType.UNDEFINED
        self.style_id = -1
        self.__m_style = None;
        self.begin_char = -1
        self.end_char = -1
        self.text = None;
        self.tag = None;
    
    @property
    def doc(self) -> 'UnitextDocument':
        """ Ссылка на документ """
        if (self.__m_doc is not None): 
            return self.__m_doc
        if (self.parent is not None): 
            return self.parent.doc
        return None
    @doc.setter
    def doc(self, value) -> 'UnitextDocument':
        self.__m_doc = value
        return value
    
    @property
    def style(self) -> 'UnitextStyle':
        """ Стиль фрагмента (если явно не задан, то берётся от родителя) """
        if (self.__m_style is not None): 
            return self.__m_style
        doc_ = self.doc
        if (doc_ is None or doc_.styles is None): 
            return None
        if (self.style_id >= 0 and (self.style_id < len(doc_.styles))): 
            return doc_.styles[self.style_id]
        return None
    @style.setter
    def style(self, value) -> 'UnitextStyle':
        self.__m_style = value
        if (value is None): 
            self.style_id = -1
        else: 
            self.style_id = value.id0_
        return value
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.typ != UnitextStyledFragmentType.UNDEFINED): 
            print("{0} ".format(Utils.enumToString(self.typ)), end="", file=res, flush=True)
            print("[{0}..{1}] ".format(self.begin_char, self.end_char), end="", file=res, flush=True)
        if (self.style is not None): 
            print("{0}".format(self.style), end="", file=res, flush=True)
        if (self.text is not None): 
            txt = (self.text if len(self.text) < 100 else (self.text[0:0+100] + "..."))
            print(" \"{0}\"".format(txt.replace("\n", "\\n")), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def get_style_attr(self, name : str, defvalue : str=None) -> str:
        """ Найти значение атрибута стиля (от текущего вверх по иерархии, пока не найдём)
        
        Args:
            name(str): имя атрибута
            defvalue(str): значение, если не нашли
        
        Returns:
            str: значение
        """
        fr = self
        while fr is not None: 
            if (fr.style_id >= 0): 
                sty = fr.style
                if (sty is not None): 
                    res = sty.get_attr(name)
                    if (res is not None): 
                        return res
            fr = fr.parent
        return defvalue
    
    def clone(self) -> 'UnitextStyledFragment':
        res = UnitextStyledFragment()
        res.typ = self.typ
        res.style_id = self.style_id
        res.doc = self.doc
        res.parent = self.parent
        res.begin_char = self.begin_char
        res.end_char = self.end_char
        res.text = self.text
        for ch in self.children: 
            chh = ch.clone()
            chh.parent = res
            res.children.append(chh)
        return res
    
    def add_child(self, ch : 'UnitextStyledFragment') -> None:
        ch.parent = self
        if (len(self.children) > 0 and (ch.end_char < self.children[0].begin_char)): 
            self.children.insert(0, ch)
            return
        i = 0
        while i < (len(self.children) - 1): 
            if ((self.children[i].end_char < ch.begin_char) and (ch.end_char < self.children[i + 1].begin_char)): 
                self.children.insert(i + 1, ch)
                return
            i += 1
        self.children.append(ch)
    
    def get_xml(self, xml0_ : XmlWriter, tag_ : str=None, out_style_full : bool=False) -> None:
        xml0_.write_start_element(Utils.ifNotNull(tag_, "stylefrag"))
        if (self.typ != UnitextStyledFragmentType.UNDEFINED): 
            xml0_.write_attribute_string("typ", Utils.enumToString(self.typ).lower())
        if (self.style_id >= 0): 
            xml0_.write_attribute_string("style", str(self.style_id))
        xml0_.write_attribute_string("b", str(self.begin_char))
        xml0_.write_attribute_string("e", str(self.end_char))
        if (self.style_id >= 0 and self.style is not None): 
            for kp in self.style.attrs.items(): 
                xml0_.write_attribute_string(kp[0], kp[1])
        if (self.text is not None): 
            xml0_.write_element_string("text", MiscHelper.correct_xml_value(self.text))
        if (not out_style_full): 
            for ch in self.children: 
                ch.get_xml(xml0_, None, False)
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for a in xml0_.attrib.items(): 
            if (Utils.getXmlAttrLocalName(a) == "typ"): 
                try: 
                    self.typ = (Utils.valToEnum(a[1], UnitextStyledFragmentType))
                except Exception as ex577: 
                    pass
            elif (Utils.getXmlAttrLocalName(a) == "style"): 
                self.style_id = int(a[1])
            elif (Utils.getXmlAttrLocalName(a) == "b"): 
                self.begin_char = int(a[1])
            elif (Utils.getXmlAttrLocalName(a) == "e"): 
                self.end_char = int(a[1])
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "stylefrag"): 
                fr = UnitextStyledFragment()
                fr.parent = self
                fr.from_xml(x)
                self.children.append(fr)
            elif (Utils.getXmlLocalName(x) == "text"): 
                self.text = Utils.getXmlInnerText(x)
    
    def find_by_char_position(self, cp : int) -> 'UnitextStyledFragment':
        """ Найти самый мелкий в дереве фрагмент (удалённный от корня),
        содержащий указанную позицию плоского текста.
        
        Args:
            cp(int): позиция символа плоского текста
        
        Returns:
            UnitextStyledFragment: фрагмент или null
        """
        if ((cp < self.begin_char) or cp > self.end_char): 
            return None
        if (len(self.children) > 10): 
            i = math.floor(len(self.children) / 2)
            d = math.floor(len(self.children) / 4)
            if (d == 0): 
                d = 1
            k = d + 2
            while k > 0:
                if (i >= len(self.children) or (i < 0)): 
                    break
                ch = self.children[i]
                if (ch.begin_char <= cp and cp <= ch.end_char): 
                    res = ch.find_by_char_position(cp)
                    if (res is not None): 
                        return res
                    return self
                if (ch.begin_char < cp): 
                    i += d
                elif (ch.end_char > cp): 
                    i -= d
                else: 
                    i += d
                d = math.floor(d / 2)
                if (d == 0): 
                    d = 1
                    k -= 1
        for ch in self.children: 
            if (ch.begin_char <= cp and cp <= ch.end_char): 
                res = ch.find_by_char_position(cp)
                if (res is not None): 
                    return res
                return self
        return self
    
    @staticmethod
    def _new424(_arg1 : 'UnitextStyledFragmentType', _arg2 : 'UnitextStyledFragment') -> 'UnitextStyledFragment':
        res = UnitextStyledFragment()
        res.typ = _arg1
        res.parent = _arg2
        return res
    
    @staticmethod
    def _new464(_arg1 : 'UnitextStyledFragment', _arg2 : 'UnitextStyledFragmentType') -> 'UnitextStyledFragment':
        res = UnitextStyledFragment()
        res.parent = _arg1
        res.typ = _arg2
        return res
    
    @staticmethod
    def _new476(_arg1 : 'UnitextStyledFragmentType', _arg2 : 'UnitextStyle', _arg3 : 'UnitextStyledFragment') -> 'UnitextStyledFragment':
        res = UnitextStyledFragment()
        res.typ = _arg1
        res.style = _arg2
        res.parent = _arg3
        return res