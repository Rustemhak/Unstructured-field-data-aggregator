# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextMiscType import UnitextMiscType

class UnitextMisc(UnitextItem):
    """ Разные нетекстовые элементы """
    
    def __init__(self) -> None:
        super().__init__()
        self.typ = UnitextMiscType.UNDEFINED
    
    def __str__(self) -> str:
        if (self.typ == UnitextMiscType.ANCHOR): 
            return "{0}: {1}".format(Utils.enumToString(self.typ), Utils.ifNotNull(self.id0_, ""))
        return Utils.enumToString(self.typ)
    
    @property
    def _inner_tag(self) -> str:
        return "misc"
    
    def clone(self) -> 'UnitextItem':
        res = UnitextMisc()
        res._clone_from(self)
        res.typ = self.typ
        return res
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (not par.call_before(self, res)): 
            return
        if (self.id0_ is not None): 
            print("<a name=\"{0}\"> </a>".format(self.id0_), end="", file=res, flush=True)
        if (self.typ == UnitextMiscType.HORIZONTALLINE): 
            print("\r\n<HR/>", end="", file=res)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("misc")
        self._write_xml_attrs(xml0_)
        xml0_.write_attribute_string("type", Utils.enumToString(self.typ).lower())
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        super().from_xml(xml0_)
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "type"): 
                    try: 
                        self.typ = (Utils.valToEnum(a[1], UnitextMiscType))
                    except Exception as ex567: 
                        pass
    
    @property
    def is_whitespaces(self) -> bool:
        return False
    
    @staticmethod
    def _new269(_arg1 : 'UnitextMiscType') -> 'UnitextMisc':
        res = UnitextMisc()
        res.typ = _arg1
        return res