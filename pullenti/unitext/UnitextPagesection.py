# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Xml import XmlWriter

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextPagesectionItem import UnitextPagesectionItem

class UnitextPagesection(UnitextItem):
    """ Информация о страницах и колонтитулах.
    Сегменты страниц
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.width = 0
        self.height = 0
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0
        self.header_height = 0
        self.footer_height = 0
        self.items = list()
    
    def clone(self) -> 'UnitextItem':
        res = UnitextPagesection()
        res._clone_from(self)
        res.width = self.width
        res.height = self.height
        res.left = self.left
        res.right = self.right
        res.top = self.top
        res.bottom = self.bottom
        res.header_height = self.header_height
        res.footer_height = self.footer_height
        for it in self.items: 
            res.items.append(Utils.asObjectOrNull(it.clone(), UnitextPagesectionItem))
        for it in res.items: 
            it.parent = (res)
        if (self._m_styled_frag is not None): 
            res._m_styled_frag = self._m_styled_frag.clone()
        return res
    
    def __str__(self) -> str:
        return "Section {0}: {1}x{2}".format(self.id0_, MiscHelper.out_double(self.width), MiscHelper.out_double(self.height))
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("section")
        self._write_xml_attrs(xml0_)
        if (self.width > 0): 
            xml0_.write_attribute_string("width", MiscHelper.out_double(self.width))
        if (self.height > 0): 
            xml0_.write_attribute_string("height", MiscHelper.out_double(self.height))
        if (self.left > 0): 
            xml0_.write_attribute_string("left", MiscHelper.out_double(self.left))
        if (self.top > 0): 
            xml0_.write_attribute_string("top", MiscHelper.out_double(self.top))
        if (self.right > 0): 
            xml0_.write_attribute_string("right", MiscHelper.out_double(self.right))
        if (self.bottom > 0): 
            xml0_.write_attribute_string("bottom", MiscHelper.out_double(self.bottom))
        if (self.header_height > 0): 
            xml0_.write_attribute_string("header", MiscHelper.out_double(self.header_height))
        if (self.footer_height > 0): 
            xml0_.write_attribute_string("footer", MiscHelper.out_double(self.footer_height))
        for it in self.items: 
            it.get_xml(xml0_)
        xml0_.write_end_element()
    
    def __parse_double(self, str0_ : str) -> float:
        d = 0
        wrapd568 = RefOutArgWrapper(0)
        inoutres569 = MiscHelper.try_parse_double(str0_, wrapd568)
        d = wrapd568.value
        if (inoutres569): 
            return d
        return 0
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        super().from_xml(xml0_)
        for a in xml0_.attrib.items(): 
            if (Utils.getXmlAttrLocalName(a) == "width"): 
                self.width = self.__parse_double(a[1])
            elif (Utils.getXmlAttrLocalName(a) == "height"): 
                self.height = self.__parse_double(a[1])
            elif (Utils.getXmlAttrLocalName(a) == "left"): 
                self.left = self.__parse_double(a[1])
            elif (Utils.getXmlAttrLocalName(a) == "top"): 
                self.top = self.__parse_double(a[1])
            elif (Utils.getXmlAttrLocalName(a) == "right"): 
                self.right = self.__parse_double(a[1])
            elif (Utils.getXmlAttrLocalName(a) == "bottom"): 
                self.bottom = self.__parse_double(a[1])
            elif (Utils.getXmlAttrLocalName(a) == "header"): 
                self.header_height = self.__parse_double(a[1])
            elif (Utils.getXmlAttrLocalName(a) == "footer"): 
                self.footer_height = self.__parse_double(a[1])
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "item"): 
                it = UnitextPagesectionItem()
                it.parent = (self)
                it.from_xml(x)
                self.items.append(it)
    
    def get_all_items(self, res : typing.List['UnitextItem'], lev : int) -> None:
        if (res is not None): 
            res.append(self)
        for it in self.items: 
            it.parent = (self)
            it.get_all_items(res, lev + 1)