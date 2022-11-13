# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import base64
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Xml import XmlWriter

from pullenti.unitext.UnilayRectangle import UnilayRectangle

class UnilayPage:
    """ Страница тексто-графического слоя """
    
    def __init__(self) -> None:
        self.number = 0
        self.width = 0
        self.height = 0
        self.image_content = None;
        self.rects = list()
        self.top_number = 0
        self.bottom_number = 0
        self.page_title = None;
        self.tag = None;
    
    def __str__(self) -> str:
        return "Page {0} ({1}x{2}){3}".format(self.number, self.width, self.height, ("" if self.image_content is None else " has image"))
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("page")
        if (self.number > 0): 
            xml0_.write_attribute_string("number", str(self.number))
        if (self.top_number > 0): 
            xml0_.write_attribute_string("topnumber", str(self.top_number))
        if (self.bottom_number > 0): 
            xml0_.write_attribute_string("bottomnumber", str(self.bottom_number))
        if (self.width > 0): 
            xml0_.write_attribute_string("width", str(self.width))
        if (self.height > 0): 
            xml0_.write_attribute_string("height", str(self.height))
        if (self.image_content is not None): 
            xml0_.write_element_string("image", base64.encodestring(self.image_content).decode('utf-8', 'ignore'))
        for r in self.rects: 
            r.get_xml(xml0_)
        xml0_.write_end_element()
    
    def restore(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        d = 0
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "number"): 
                    i = 0
                    wrapi521 = RefOutArgWrapper(0)
                    inoutres522 = Utils.tryParseInt(a[1], wrapi521)
                    i = wrapi521.value
                    if (inoutres522): 
                        self.number = i
                elif (Utils.getXmlAttrLocalName(a) == "topnumber"): 
                    i = 0
                    wrapi523 = RefOutArgWrapper(0)
                    inoutres524 = Utils.tryParseInt(a[1], wrapi523)
                    i = wrapi523.value
                    if (inoutres524): 
                        self.top_number = i
                elif (Utils.getXmlAttrLocalName(a) == "bottomnumber"): 
                    i = 0
                    wrapi525 = RefOutArgWrapper(0)
                    inoutres526 = Utils.tryParseInt(a[1], wrapi525)
                    i = wrapi525.value
                    if (inoutres526): 
                        self.bottom_number = i
                elif (Utils.getXmlAttrLocalName(a) == "width"): 
                    i = 0
                    wrapi527 = RefOutArgWrapper(0)
                    inoutres528 = Utils.tryParseInt(a[1], wrapi527)
                    i = wrapi527.value
                    if (inoutres528): 
                        self.width = i
                elif (Utils.getXmlAttrLocalName(a) == "height"): 
                    i = 0
                    wrapi529 = RefOutArgWrapper(0)
                    inoutres530 = Utils.tryParseInt(a[1], wrapi529)
                    i = wrapi529.value
                    if (inoutres530): 
                        self.height = i
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "rect"): 
                r = UnilayRectangle._new531(self)
                r.restore(x)
                self.rects.append(r)
            elif (Utils.getXmlLocalName(x) == "image"): 
                self.image_content = base64.decodestring((Utils.getXmlInnerText(x)).encode('utf-8', 'ignore'))
    
    def find_rect(self, x : float, y : float) -> 'UnilayRectangle':
        """ Найти по координате накрывающий её прямоугольник
        
        Args:
            x(float): 
            y(float): 
        
        """
        for r in self.rects: 
            if ((r.left <= x and x <= r.right and r.top <= y) and y <= r.bottom): 
                return r
        return None
    
    def merge_rects_by_quality(self, page : 'UnilayPage') -> None:
        # Объединить результат распознавания с распознаванием страницы другим движком,
        # взяв наилучшие Rects по их качеству Quality.
        # page - страница с таким же изображением</param>
        for r in page.rects: 
            r.tag = None
        max_line = 0
        for r in self.rects: 
            if (r.line_number > max_line): 
                max_line = r.line_number
            rr = page.find_rect(((r.left + r.right)) / (2), ((r.top + r.bottom)) / (2))
            if (rr is None): 
                continue
            rr.tag = (r)
            if ((r.quality) >= (rr.quality)): 
                continue
            r.text = rr.text
            r.quality = rr.quality
            r.left = rr.left
            r.top = rr.top
            r.right = rr.right
            r.bottom = rr.bottom
    
    @staticmethod
    def _new156(_arg1 : bytearray) -> 'UnilayPage':
        res = UnilayPage()
        res.image_content = _arg1
        return res