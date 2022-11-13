# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
import base64
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Xml import XmlWriter

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnilayOcrQuality import UnilayOcrQuality

class UnilayRectangle:
    """ Прямоугольник тексто-графического слоя """
    
    def __init__(self) -> None:
        self.page = None;
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0
        self.text = None;
        self.image_content = None;
        self.ignored = False
        self.line_number = 0
        self.quality = UnilayOcrQuality.UNDEFINED
        self.tag = None;
    
    def __str__(self) -> str:
        res = "{0}..{1} x {2}..{3}".format(round(self.left, 2), round(self.right, 2), round(self.top, 2), round(self.bottom, 2))
        if (self.text is not None): 
            return "{0}: {1}".format(res, self.text)
        if (self.image_content is not None): 
            return "{0}: Image".format(res)
        return res
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("rect")
        if (self.line_number > 0): 
            xml0_.write_attribute_string("line", str(self.line_number))
        xml0_.write_attribute_string("left", MiscHelper.out_double(self.left))
        xml0_.write_attribute_string("top", MiscHelper.out_double(self.top))
        xml0_.write_attribute_string("right", MiscHelper.out_double(self.right))
        xml0_.write_attribute_string("bottom", MiscHelper.out_double(self.bottom))
        if (self.quality != UnilayOcrQuality.UNDEFINED): 
            xml0_.write_attribute_string("q", Utils.enumToString(self.quality).lower())
        if (self.image_content is not None): 
            xml0_.write_element_string("image", base64.encodestring(self.image_content).decode('utf-8', 'ignore'))
        elif (self.text is not None): 
            xml0_.write_element_string("text", Utils.ifNotNull(MiscHelper.correct_xml_value(self.text), ""))
        xml0_.write_end_element()
    
    def restore(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        d = 0
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "line"): 
                    i = 0
                    wrapi532 = RefOutArgWrapper(0)
                    inoutres533 = Utils.tryParseInt(a[1], wrapi532)
                    i = wrapi532.value
                    if (inoutres533): 
                        self.line_number = i
                elif (Utils.getXmlAttrLocalName(a) == "left"): 
                    wrapd534 = RefOutArgWrapper(0)
                    inoutres535 = MiscHelper.try_parse_double(a[1], wrapd534)
                    d = wrapd534.value
                    if (inoutres535): 
                        self.left = d
                elif (Utils.getXmlAttrLocalName(a) == "top"): 
                    wrapd536 = RefOutArgWrapper(0)
                    inoutres537 = MiscHelper.try_parse_double(a[1], wrapd536)
                    d = wrapd536.value
                    if (inoutres537): 
                        self.top = d
                elif (Utils.getXmlAttrLocalName(a) == "right"): 
                    wrapd538 = RefOutArgWrapper(0)
                    inoutres539 = MiscHelper.try_parse_double(a[1], wrapd538)
                    d = wrapd538.value
                    if (inoutres539): 
                        self.right = d
                elif (Utils.getXmlAttrLocalName(a) == "bottom"): 
                    wrapd540 = RefOutArgWrapper(0)
                    inoutres541 = MiscHelper.try_parse_double(a[1], wrapd540)
                    d = wrapd540.value
                    if (inoutres541): 
                        self.bottom = d
                elif (Utils.getXmlAttrLocalName(a) == "q"): 
                    try: 
                        self.quality = (Utils.valToEnum(a[1], UnilayOcrQuality))
                    except Exception as ex542: 
                        pass
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "text"): 
                self.text = Utils.getXmlInnerText(x)
            elif (Utils.getXmlLocalName(x) == "image"): 
                self.image_content = base64.decodestring((Utils.getXmlInnerText(x)).encode('utf-8', 'ignore'))
    
    @staticmethod
    def _new531(_arg1 : 'UnilayPage') -> 'UnilayRectangle':
        res = UnilayRectangle()
        res.page = _arg1
        return res