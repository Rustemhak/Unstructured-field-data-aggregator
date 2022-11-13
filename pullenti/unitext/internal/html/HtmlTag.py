# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

class HtmlTag:
    
    class Attrs(IntEnum):
        INLINE = 1
        BLOCK = 2
        TABLEITEM = 4
        CONTROL = 8
        IGNORETHIS = 0x10
        IGNOREWITHCONTENT = 0x20
        EMPTY = 0x40
        ENDTAGREQ = 0x80
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    @staticmethod
    def find_tag(name_ : str) -> 'HtmlTag':
        if (name_ is None): 
            return None
        res = None
        wrapres37 = RefOutArgWrapper(None)
        inoutres38 = Utils.tryGetValue(HtmlTag.__get_all_tags(), name_, wrapres37)
        res = wrapres37.value
        if (not inoutres38): 
            return None
        return res
    
    @property
    def is_inline(self) -> bool:
        return (((self.__m_attrs) & (HtmlTag.Attrs.INLINE))) != 0
    
    @property
    def is_block(self) -> bool:
        return (((self.__m_attrs) & (HtmlTag.Attrs.BLOCK))) != 0
    
    @property
    def is_table(self) -> bool:
        return (((self.__m_attrs) & (HtmlTag.Attrs.TABLEITEM))) != 0
    
    @property
    def is_empty(self) -> bool:
        return (((self.__m_attrs) & (HtmlTag.Attrs.EMPTY))) != 0
    
    @property
    def endtag_required(self) -> bool:
        return (((self.__m_attrs) & (HtmlTag.Attrs.ENDTAGREQ))) != 0
    
    @property
    def ignore_with_content(self) -> bool:
        return (((self.__m_attrs) & (HtmlTag.Attrs.IGNOREWITHCONTENT))) != 0
    
    def __init__(self, name_ : str, typ : 'Attrs') -> None:
        self.name = None;
        self.__m_attrs = HtmlTag.Attrs.INLINE
        self.name = name_
        self.__m_attrs = typ
        HtmlTag.M_ALL_TAGS[name_] = self
    
    M_ALL_TAGS = None
    
    @staticmethod
    def __get_all_tags() -> typing.List[tuple]:
        if (HtmlTag.M_ALL_TAGS is None): 
            HtmlTag.M_ALL_TAGS = dict()
            HtmlTag.__create_all_tags()
        return HtmlTag.M_ALL_TAGS
    
    @staticmethod
    def __create_all_tags() -> None:
        ht = None
        ht = HtmlTag("A", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("ABBR", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("ACRONYM", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("ADDRESS", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("APPLET", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNOREWITHCONTENT) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("AREA", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.EMPTY), HtmlTag.Attrs))
        ht = HtmlTag("B", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("BASE", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNORETHIS) | (HtmlTag.Attrs.EMPTY), HtmlTag.Attrs))
        ht = HtmlTag("BASEFONT", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.EMPTY), HtmlTag.Attrs))
        ht = HtmlTag("BDO", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("BIG", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("BLOCKQUOTE", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("BODY", HtmlTag.Attrs.BLOCK)
        ht = HtmlTag("BR", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.EMPTY), HtmlTag.Attrs))
        ht = HtmlTag("BUTTON", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNORETHIS) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("CAPTION", Utils.valToEnum((HtmlTag.Attrs.TABLEITEM) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("CENTER", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("CITE", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("CODE", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNOREWITHCONTENT) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("COL", Utils.valToEnum((HtmlTag.Attrs.TABLEITEM) | (HtmlTag.Attrs.EMPTY), HtmlTag.Attrs))
        ht = HtmlTag("COLGROUP", HtmlTag.Attrs.TABLEITEM)
        ht = HtmlTag("DD", HtmlTag.Attrs.BLOCK)
        ht = HtmlTag("DEL", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.IGNOREWITHCONTENT) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("DFN", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("DIR", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("DIV", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("DL", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("DT", HtmlTag.Attrs.INLINE)
        ht = HtmlTag("EM", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("FIELDSET", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNORETHIS) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("FONT", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("FORM", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNORETHIS) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("FRAME", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.EMPTY), HtmlTag.Attrs))
        ht = HtmlTag("FRAMESET", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("H1", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("H2", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("H3", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("H4", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("H5", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("H6", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("HEAD", HtmlTag.Attrs.BLOCK)
        ht = HtmlTag("HR", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.EMPTY), HtmlTag.Attrs))
        ht = HtmlTag("HTML", HtmlTag.Attrs.BLOCK)
        ht = HtmlTag("I", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("IFRAME", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("IMG", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.EMPTY), HtmlTag.Attrs))
        ht = HtmlTag("INPUT", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNORETHIS) | (HtmlTag.Attrs.EMPTY), HtmlTag.Attrs))
        ht = HtmlTag("INS", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.IGNORETHIS) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("ISINDEX", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.EMPTY), HtmlTag.Attrs))
        ht = HtmlTag("KBD", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNORETHIS) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("LABEL", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNORETHIS) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("LEGEND", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNORETHIS) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("LI", HtmlTag.Attrs.BLOCK)
        ht = HtmlTag("LINK", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.EMPTY), HtmlTag.Attrs))
        ht = HtmlTag("MAP", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("MENU", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("META", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.EMPTY), HtmlTag.Attrs))
        ht = HtmlTag("NOFRAMES", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("NOSCRIPT", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("OBJECT", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNOREWITHCONTENT) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("OL", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("OPTGROUP", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNORETHIS) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("OPTION", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNORETHIS), HtmlTag.Attrs))
        ht = HtmlTag("P", HtmlTag.Attrs.BLOCK)
        ht = HtmlTag("PARAM", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNOREWITHCONTENT) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("PRE", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("Q", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("S", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("SAMP", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNORETHIS) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("SCRIPT", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNOREWITHCONTENT) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("SELECT", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNORETHIS) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("SMALL", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("SPAN", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("STRIKE", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("STRONG", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("STYLE", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNOREWITHCONTENT) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("SUB", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("SUP", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("TABLE", Utils.valToEnum((HtmlTag.Attrs.TABLEITEM) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("TBODY", HtmlTag.Attrs.TABLEITEM)
        ht = HtmlTag("TD", HtmlTag.Attrs.TABLEITEM)
        ht = HtmlTag("TFOOT", HtmlTag.Attrs.TABLEITEM)
        ht = HtmlTag("TH", HtmlTag.Attrs.TABLEITEM)
        ht = HtmlTag("THEAD", HtmlTag.Attrs.TABLEITEM)
        ht = HtmlTag("TR", HtmlTag.Attrs.TABLEITEM)
        ht = HtmlTag("TEXTAREA", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("TITLE", Utils.valToEnum((HtmlTag.Attrs.CONTROL) | (HtmlTag.Attrs.IGNORETHIS) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("TT", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("U", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("UL", Utils.valToEnum((HtmlTag.Attrs.BLOCK) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))
        ht = HtmlTag("VAR", Utils.valToEnum((HtmlTag.Attrs.INLINE) | (HtmlTag.Attrs.ENDTAGREQ), HtmlTag.Attrs))