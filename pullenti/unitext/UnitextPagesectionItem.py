# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.unitext.UnitextStyledFragment import UnitextStyledFragment
from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
from pullenti.unitext.UnitextDocument import UnitextDocument
from pullenti.unitext.UnitextPagesectionItemPages import UnitextPagesectionItemPages
from pullenti.unitext.UnitextItem import UnitextItem

class UnitextPagesectionItem(UnitextItem):
    """ Элемент сегмента страниц """
    
    def __init__(self) -> None:
        super().__init__()
        self.is_footer = False
        self.pages = UnitextPagesectionItemPages.DEFAULT
        self.content = None;
    
    def __str__(self) -> str:
        return "{0} pages={1}".format(("Footer" if self.is_footer else "Header"), Utils.enumToString(self.pages).lower())
    
    def clone(self) -> 'UnitextItem':
        res = UnitextPagesectionItem()
        res._clone_from(self)
        res.is_footer = self.is_footer
        res.pages = self.pages
        if (self.content is not None): 
            res.content = self.content.clone()
            res.content.parent = (res)
        return res
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("sectionitem")
        self._write_xml_attrs(xml0_)
        xml0_.write_attribute_string("type", ("footer" if self.is_footer else "header"))
        xml0_.write_attribute_string("pages", Utils.enumToString(self.pages).lower())
        if (self.content is not None): 
            xml0_.write_start_element("content")
            self.content.get_xml(xml0_)
            xml0_.write_end_element()
            if (self.content._m_styled_frag is not None): 
                self.content._m_styled_frag.get_xml(xml0_, None, False)
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        doc = None
        it = self
        while it is not None: 
            if (isinstance(it, UnitextDocument)): 
                doc = (Utils.asObjectOrNull(it, UnitextDocument))
            it = it.parent
        super().from_xml(xml0_)
        for a in xml0_.attrib.items(): 
            if (Utils.getXmlAttrLocalName(a) == "type"): 
                self.is_footer = a[1] == "footer"
            elif (Utils.getXmlAttrLocalName(a) == "pages"): 
                try: 
                    self.pages = (Utils.valToEnum(a[1], UnitextPagesectionItemPages))
                except Exception as ex570: 
                    pass
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "content"): 
                for xx in x: 
                    self.content = UnitextHelper.create_item(xx)
                    if (self.content is not None): 
                        self.content.parent = (self)
                    break
            elif (Utils.getXmlLocalName(x) == "stylefrag" and self.content is not None): 
                self.content._m_styled_frag = UnitextStyledFragment()
                self.content._m_styled_frag.doc = doc
                self.content._m_styled_frag.from_xml(x)
    
    def get_all_items(self, res : typing.List['UnitextItem'], lev : int) -> None:
        if (res is not None): 
            res.append(self)
        if (self.content is not None): 
            self.content.parent = (self)
            self.content.get_all_items(res, lev + 1)
    
    @staticmethod
    def _new42(_arg1 : 'UnitextItem') -> 'UnitextPagesectionItem':
        res = UnitextPagesectionItem()
        res.content = _arg1
        return res
    
    @staticmethod
    def _new43(_arg1 : bool, _arg2 : 'UnitextItem') -> 'UnitextPagesectionItem':
        res = UnitextPagesectionItem()
        res.is_footer = _arg1
        res.content = _arg2
        return res
    
    @staticmethod
    def _new259(_arg1 : 'UnitextItem', _arg2 : bool) -> 'UnitextPagesectionItem':
        res = UnitextPagesectionItem()
        res.content = _arg1
        res.is_footer = _arg2
        return res