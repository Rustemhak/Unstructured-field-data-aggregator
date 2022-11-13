# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import math
import base64
import gc
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.unitext.FileFormat import FileFormat
from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.util.FileFormatsHelper import FileFormatsHelper

class UnitextImage(UnitextItem):
    """ Картинка """
    
    def __init__(self) -> None:
        super().__init__()
        self.content = None;
        self.width = None;
        self.height = None;
        self.rect = None;
        self.html_src_uri = None;
    
    def clone(self) -> 'UnitextItem':
        res = UnitextImage()
        res._clone_from(self)
        res.content = self.content
        res.width = self.width
        res.height = self.height
        res.rect = self.rect
        res.html_src_uri = self.html_src_uri
        return res
    
    @property
    def _inner_tag(self) -> str:
        return "img"
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print("Image", end="", file=tmp)
        if (self.width is not None or self.height is not None): 
            print(" {0} x {1}".format(Utils.ifNotNull(self.width, "?"), Utils.ifNotNull(self.height, "?")), end="", file=tmp, flush=True)
        if (self.content is not None): 
            frm = FileFormatsHelper.analize_format(None, self.content)
            if (frm != FileFormat.UNKNOWN): 
                print(" {0}".format(Utils.enumToString(frm).upper()), end="", file=tmp, flush=True)
            print(" {0}bytes".format(len(self.content)), end="", file=tmp, flush=True)
        elif (self.html_src_uri is not None): 
            print(" {0}".format(self.html_src_uri), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
        print(' ', end="", file=res)
        if (pars is not None and pars.set_positions): 
            self.end_char = self.begin_char
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (not par.call_before(self, res)): 
            return
        print("<img".format(), end="", file=res, flush=True)
        if (self.id0_ is not None): 
            print(" id=\"{0}\"".format(self.id0_), end="", file=res, flush=True)
        print(" style=\"max-width:100%;".format(), end="", file=res, flush=True)
        over = False
        if (self.content is None): 
            print("border:2pt solid red;", end="", file=res)
        elif (len(self.content) > 10000000 or ((par is not None and len(self.content) > par.max_image_size)) or ((res.tell() > 40000000 and len(self.content) > 10000))): 
            print("border:2pt solid red;", end="", file=res)
            over = True
        wi = 0
        hi = 0
        if (self.width is not None): 
            i = 0
            while i < len(self.width): 
                if (not str.isdigit(self.width[i])): 
                    break
                else: 
                    wi = int(self.width[0:0+i + 1])
                i += 1
        if (self.height is not None): 
            i = 0
            while i < len(self.height): 
                if (not str.isdigit(self.height[i])): 
                    break
                else: 
                    hi = int(self.height[0:0+i + 1])
                i += 1
        if ((wi < 500) and (hi < 500)): 
            if (self.width is not None): 
                print("width:{0};".format(self.width), end="", file=res, flush=True)
            if (self.height is not None): 
                print("height:{0};".format(self.height), end="", file=res, flush=True)
        print("\"", end="", file=res)
        if (self.content is not None): 
            if (over): 
                print(" alt=\"Image too large to show here ({0}Kb)\"".format(math.floor(len(self.content) / 1024)), end="", file=res, flush=True)
            else: 
                frm = FileFormatsHelper.analize_format(None, self.content)
                if (frm == FileFormat.JPG2000): 
                    print(" title=\"Image format JPEG 2000 not supported\"".format(), end="", file=res, flush=True)
                else: 
                    base640_ = base64.b64encode(self.content).decode('utf-8', 'ignore')
                    if (base640_.find('\n') >= 0): 
                        base640_ = base640_.replace("\n", "")
                    str0_ = None
                    if (frm != FileFormat.UNKNOWN): 
                        str0_ = FileFormatsHelper.get_format_ext(frm)
                        if (str0_.startswith(".")): 
                            str0_ = str0_[1:]
                    if (str0_ is None): 
                        str0_ = "png"
                    if (str0_ == "tif"): 
                        str0_ = "tiff"
                    src = "data:image/{0};base64,".format(str0_) + base640_
                    print(" src=\"{0}\"".format(src), end="", file=res, flush=True)
        else: 
            print(" src=\"{0}\"".format(Utils.ifNotNull(self.html_src_uri, "undefined")), end="", file=res, flush=True)
        print("/>", end="", file=res)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("image")
        self._write_xml_attrs(xml0_)
        if (self.width is not None): 
            xml0_.write_attribute_string("width", self.width)
        if (self.height is not None): 
            xml0_.write_attribute_string("height", self.height)
        if (self.html_src_uri is not None): 
            xml0_.write_attribute_string("uri", MiscHelper.correct_xml_value(self.html_src_uri))
        if (self.content is not None): 
            try: 
                dat = base64.encodestring(self.content).decode('utf-8', 'ignore')
                tmp = io.StringIO()
                i = 0
                for ch in dat: 
                    if (Utils.isWhitespace(ch)): 
                        continue
                    print(ch, end="", file=tmp)
                    i += 1
                    if (i >= 100): 
                        i = 0
                        print("\r\n", end="", file=tmp)
                xml0_.write_string(Utils.toStringStringIO(tmp))
            except Exception as ex: 
                gc.collect()
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        super().from_xml(xml0_)
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "width"): 
                    self.width = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "height"): 
                    self.height = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "uri"): 
                    self.html_src_uri = a[1]
        try: 
            txt = Utils.getXmlInnerText(xml0_)
            if (txt is not None): 
                self.content = base64.decodestring((txt).encode('utf-8', 'ignore'))
        except Exception as ex563: 
            pass
    
    def _set_default_text_pos(self, cp : int, res : io.StringIO) -> None:
        self.end_char = cp.value
        self.begin_char = self.end_char
        cp.value += 1
        if (res is not None): 
            print(' ', end="", file=res)
    
    @staticmethod
    def _new94(_arg1 : str) -> 'UnitextImage':
        res = UnitextImage()
        res.id0_ = _arg1
        return res
    
    @staticmethod
    def _new260(_arg1 : bytearray) -> 'UnitextImage':
        res = UnitextImage()
        res.content = _arg1
        return res
    
    @staticmethod
    def _new337(_arg1 : bytearray, _arg2 : 'UnilayRectangle', _arg3 : str) -> 'UnitextImage':
        res = UnitextImage()
        res.content = _arg1
        res.rect = _arg2
        res.page_section_id = _arg3
        return res
    
    @staticmethod
    def _new338(_arg1 : str) -> 'UnitextImage':
        res = UnitextImage()
        res.page_section_id = _arg1
        return res