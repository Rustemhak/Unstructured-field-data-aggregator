# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextItem import UnitextItem

class UnitextComment(UnitextItem):
    """ Примечание (аннотация). Оформляется двумя такими объектами -
    для начальной позиции и конечной позиции.
    Примечание (аннотация)
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.text = None;
        self.author = None;
        self.twin_id = None;
        self.is_end_of_comment = False
    
    def clone(self) -> 'UnitextItem':
        res = UnitextComment()
        res._clone_from(self)
        res.text = self.text
        res.author = self.author
        res.twin_id = self.twin_id
        return res
    
    def __str__(self) -> str:
        return "Comment: {0}{1}".format(self.text, (" (end)" if self.is_end_of_comment else ""))
    
    @property
    def _inner_tag(self) -> str:
        return "comment"
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        if (pars is not None and pars.set_positions): 
            self.end_char = res.tell()
            self.begin_char = self.end_char
            if (self.is_end_of_comment and res.tell() > 0): 
                self.end_char = res.tell() - 1
                self.begin_char = self.end_char
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (par.hide_editions_and_comments): 
            return
        if (not par.call_before(self, res)): 
            return
        if (self.text is not None and not self.is_end_of_comment): 
            if (par.out_comments_with_del_tags): 
                print("<del", end="", file=res)
                if (self.id0_ is not None): 
                    print(" id=\"{0}\"".format(self.id0_), end="", file=res, flush=True)
                print(">", end="", file=res)
                MiscHelper.correct_html_value(res, self.text, False, False)
                print("</del>", end="", file=res)
            else: 
                print(" <span id=\"{0}\" style=\"font-size:smaller;font-style:italic;color:blue;background:lightyellow\">[<b>Комментарий: </b>".format(self.id0_), end="", file=res, flush=True)
                MiscHelper.correct_html_value(res, self.text, False, False)
                print("]</span>", end="", file=res)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("comment")
        self._write_xml_attrs(xml0_)
        if (self.author is not None): 
            xml0_.write_attribute_string("author", MiscHelper.correct_xml_value(self.author))
        if (self.is_end_of_comment): 
            xml0_.write_attribute_string("end", "true")
        if (self.twin_id is not None): 
            xml0_.write_attribute_string("twin", self.twin_id)
        xml0_.write_string(MiscHelper.correct_xml_value(self.text))
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        super().from_xml(xml0_)
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "author"): 
                    self.author = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "twin"): 
                    self.twin_id = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "end"): 
                    self.is_end_of_comment = a[1] == "true"
        self.text = Utils.getXmlInnerText(xml0_)
    
    @staticmethod
    def _new44(_arg1 : str) -> 'UnitextComment':
        res = UnitextComment()
        res.text = _arg1
        return res
    
    @staticmethod
    def _new458(_arg1 : str, _arg2 : str, _arg3 : bool) -> 'UnitextComment':
        res = UnitextComment()
        res.id0_ = _arg1
        res.twin_id = _arg2
        res.is_end_of_comment = _arg3
        return res