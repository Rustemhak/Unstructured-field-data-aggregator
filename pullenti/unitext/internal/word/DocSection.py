# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.UnitextPagesectionItemPages import UnitextPagesectionItemPages
from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextPagesection import UnitextPagesection

class DocSection:
    
    def __init__(self) -> None:
        self.usect = UnitextPagesection()
        self.title_pg = False
        self.loaded = False
        self.head_ids = dict()
        self.foot_ids = dict()
    
    @staticmethod
    def __read_double_cm(str0_ : str) -> float:
        d = 0
        wrapd422 = RefOutArgWrapper(0)
        inoutres423 = MiscHelper.try_parse_double(str0_, wrapd422)
        d = wrapd422.value
        if (not inoutres423): 
            return 0
        d /= (20)
        d *= 2.54
        d /= (72)
        return round(d, 2)
    
    @staticmethod
    def __read_attr_val(x : xml.etree.ElementTree.Element, nam : str, nam2 : str=None) -> str:
        if (x.attrib is not None): 
            for a in x.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == nam): 
                    return a[1]
                elif (nam2 is not None and Utils.getXmlAttrLocalName(a) == nam2): 
                    return a[1]
        return None
    
    def load(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        self.loaded = True
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "pgSz"): 
                self.usect.width = DocSection.__read_double_cm(DocSection.__read_attr_val(x, "w", None))
                self.usect.height = DocSection.__read_double_cm(DocSection.__read_attr_val(x, "h", None))
            elif (Utils.getXmlLocalName(x) == "pgMar"): 
                self.usect.left = DocSection.__read_double_cm(DocSection.__read_attr_val(x, "left", None))
                self.usect.right = DocSection.__read_double_cm(DocSection.__read_attr_val(x, "right", None))
                self.usect.top = DocSection.__read_double_cm(DocSection.__read_attr_val(x, "top", None))
                self.usect.bottom = DocSection.__read_double_cm(DocSection.__read_attr_val(x, "bottom", None))
                self.usect.header_height = DocSection.__read_double_cm(DocSection.__read_attr_val(x, "header", None))
                self.usect.footer_height = DocSection.__read_double_cm(DocSection.__read_attr_val(x, "footer", None))
            elif (Utils.getXmlLocalName(x) == "titlePg"): 
                self.title_pg = True
            elif (Utils.getXmlLocalName(x) == "headerReference" or Utils.getXmlLocalName(x) == "footerReference"): 
                id0_ = DocSection.__read_attr_val(x, "id", None)
                typ = DocSection.__read_attr_val(x, "type", None)
                ptyp = UnitextPagesectionItemPages.DEFAULT
                if (Utils.compareStrings(typ, "first", True) == 0): 
                    ptyp = UnitextPagesectionItemPages.FIRST
                elif (Utils.compareStrings(typ, "even", True) == 0): 
                    ptyp = UnitextPagesectionItemPages.EVEN
                elif (Utils.compareStrings(typ, "odd", True) == 0): 
                    ptyp = UnitextPagesectionItemPages.ODD
                if (Utils.getXmlLocalName(x) == "headerReference"): 
                    if (not ptyp in self.head_ids): 
                        self.head_ids[ptyp] = id0_
                elif (not ptyp in self.foot_ids): 
                    self.foot_ids[ptyp] = id0_