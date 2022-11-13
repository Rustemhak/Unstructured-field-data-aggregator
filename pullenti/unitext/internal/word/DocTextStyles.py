# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.internal.word.DocTextStyle import DocTextStyle
from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextStyle import UnitextStyle
from pullenti.util.SizeunitConverter import SizeunitConverter

class DocTextStyles:
    
    def __init__(self) -> None:
        self.m_text_styles = dict()
        self.def_style = None;
        self.ustyles = list()
        self.__m_ustyles = dict()
        self.ignore = False
        self.__m_major_font = None;
        self.__m_minor_font = None;
    
    def register_style(self, st : 'UnitextStyle') -> 'UnitextStyle':
        if (self.ignore): 
            return st
        key = str(st)
        if (Utils.isNullOrEmpty(key)): 
            return None
        res = None
        wrapres433 = RefOutArgWrapper(None)
        inoutres434 = Utils.tryGetValue(self.__m_ustyles, key, wrapres433)
        res = wrapres433.value
        if (inoutres434): 
            return res
        self.__m_ustyles[key] = st
        st.id0_ = len(self.ustyles)
        self.ustyles.append(st)
        return st
    
    def get_style(self, x : xml.etree.ElementTree.Element, nam : str) -> 'DocTextStyle':
        id0_ = DocTextStyles.__read_attr_val(x, nam, None)
        if (id0_ is None): 
            return None
        res = None
        wrapres435 = RefOutArgWrapper(None)
        inoutres436 = Utils.tryGetValue(self.m_text_styles, id0_, wrapres435)
        res = wrapres435.value
        if (not inoutres436): 
            return None
        return res
    
    @staticmethod
    def __read_attr_val(x : xml.etree.ElementTree.Element, nam : str, nam2 : str=None) -> str:
        if (x.attrib is not None): 
            for a in x.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == nam): 
                    return a[1]
                elif (nam2 is not None and Utils.getXmlAttrLocalName(a) == nam2): 
                    return a[1]
        return None
    
    @staticmethod
    def __get_size_val(val : str) -> str:
        if (val is None): 
            return None
        for ch in val: 
            if (str.isalpha(ch)): 
                return val
        d = 0
        wrapd437 = RefOutArgWrapper(0)
        inoutres438 = MiscHelper.try_parse_double(val, wrapd437)
        d = wrapd437.value
        if (not inoutres438): 
            return val
        d = round(d / (20), 2)
        return "{0}pt".format(MiscHelper.out_double(d))
    
    @staticmethod
    def __corr_color(val : str) -> str:
        if (val is None): 
            return None
        if (len(val) != 6): 
            return val
        for ch in val: 
            if (str.isdigit(ch)): 
                pass
            elif (ch >= 'A' and ch <= 'F'): 
                pass
            elif (ch >= 'a' and ch <= 'f'): 
                pass
            else: 
                return val
        val = "#" + val.upper()
        return val
    
    def read_unitext_style(self, node : xml.etree.ElementTree.Element, st : 'UnitextStyle') -> None:
        for x in node: 
            if (Utils.getXmlLocalName(x) == "pStyle" or Utils.getXmlLocalName(x) == "rStyle"): 
                id0_ = DocTextStyles.__read_attr_val(x, "val", None)
                if (id0_ in self.m_text_styles): 
                    self.m_text_styles[id0_].ustyle.copy_to(st)
            elif (Utils.getXmlLocalName(x) == "b"): 
                val = DocTextStyles.__read_attr_val(x, "val", None)
                if (val == "0"): 
                    val = "normal"
                else: 
                    val = "bold"
                st.add_attr("font-weight", val, False)
            elif (Utils.getXmlLocalName(x) == "i"): 
                val = DocTextStyles.__read_attr_val(x, "val", None)
                if (val == "0"): 
                    st.add_attr("font-style", "none", False)
                else: 
                    st.add_attr("font-style", "italic", False)
            elif (Utils.getXmlLocalName(x) == "u"): 
                val = DocTextStyles.__read_attr_val(x, "val", None)
                if (val == "none"): 
                    st.add_attr("text-decoration", "none", False)
                else: 
                    st.add_attr("text-decoration", "underline", False)
            elif (Utils.getXmlLocalName(x) == "strike"): 
                val = DocTextStyles.__read_attr_val(x, "val", None)
                if (val != "0"): 
                    st.add_attr("text-decoration", "line-through", False)
            elif (Utils.getXmlLocalName(x) == "caps"): 
                st.add_attr("upper-case", "true", False)
            elif (Utils.getXmlLocalName(x) == "rFonts"): 
                nam = DocTextStyles.__read_attr_val(x, "cs", "ansii")
                if (nam is None): 
                    nam = DocTextStyles.__read_attr_val(x, "ascii", "hAnsii")
                if (nam is None): 
                    nam = st.get_attr("font-name")
                if (nam is None): 
                    for a in x.attrib.items(): 
                        if (Utils.endsWithString(Utils.getXmlAttrLocalName(a), "theme", True) and not Utils.endsWithString(Utils.getXmlAttrLocalName(a), "asiatheme", True)): 
                            if (Utils.startsWithString(a[1], "major", True)): 
                                nam = self.__m_major_font
                            elif (Utils.startsWithString(a[1], "minor", True)): 
                                nam = self.__m_minor_font
                if (nam is None): 
                    for a in x.attrib.items(): 
                        if (not Utils.endsWithString(Utils.getXmlAttrLocalName(a), "theme", True) and not Utils.endsWithString(Utils.getXmlAttrLocalName(a), "asia", True)): 
                            nam = a[1]
                            break
                if (not Utils.isNullOrEmpty(nam)): 
                    st.add_attr("font-name", nam, False)
            elif (Utils.getXmlLocalName(x) == "sz"): 
                d = 0
                wrapd439 = RefOutArgWrapper(0)
                inoutres440 = MiscHelper.try_parse_double(DocTextStyles.__read_attr_val(x, "val", None), wrapd439)
                d = wrapd439.value
                if (inoutres440): 
                    st.add_attr("font-size", "{0}pt".format(MiscHelper.out_double(d / (2))), False)
            elif (Utils.getXmlLocalName(x) == "highlight" or Utils.getXmlLocalName(x) == "color"): 
                val = DocTextStyles.__corr_color(DocTextStyles.__read_attr_val(x, "val", None))
                if (val is None or val == "auto"): 
                    continue
                if (Utils.getXmlLocalName(x) == "color"): 
                    st.add_attr("color", val, False)
                else: 
                    st.add_attr("background-color", val, False)
            elif (Utils.getXmlLocalName(x) == "shd"): 
                val = DocTextStyles.__read_attr_val(x, "color", None)
                if (val == "auto"): 
                    val = DocTextStyles.__corr_color(DocTextStyles.__read_attr_val(x, "fill", None))
                else: 
                    val = DocTextStyles.__corr_color(val)
                if (val is not None and val != "auto"): 
                    st.add_attr("background-color", val, False)
            elif (Utils.getXmlLocalName(x) == "rPr"): 
                if (Utils.getXmlLocalName(node) == "pPr"): 
                    pass
                else: 
                    self.read_unitext_style(x, st)
            elif (Utils.getXmlLocalName(x) == "jc"): 
                val = DocTextStyles.__read_attr_val(x, "val", None)
                if (val == "start"): 
                    val = "left"
                elif (val == "end"): 
                    val = "right"
                elif (val == "both"): 
                    val = "justify"
                st.add_attr("text-align", val, False)
            elif (Utils.getXmlLocalName(x) == "spacing"): 
                rule = DocTextStyles.__read_attr_val(x, "lineRule", None)
                for a in x.attrib.items(): 
                    if (Utils.getXmlAttrLocalName(a) == "before" or Utils.getXmlAttrLocalName(a) == "top"): 
                        st.add_attr("margin-top", DocTextStyles.__get_size_val(a[1]), False)
                    elif (Utils.getXmlAttrLocalName(a) == "after" or Utils.getXmlAttrLocalName(a) == "bottom"): 
                        st.add_attr("margin-bottom", DocTextStyles.__get_size_val(a[1]), False)
                    elif (Utils.getXmlAttrLocalName(a) == "line"): 
                        d = 0
                        wrapd441 = RefOutArgWrapper(0)
                        inoutres442 = MiscHelper.try_parse_double(a[1], wrapd441)
                        d = wrapd441.value
                        if (inoutres442): 
                            val = None
                            if (rule == "auto"): 
                                d = round(d / (240), 2)
                                val = "{0}".format(MiscHelper.out_double(d))
                            elif (rule == "exact"): 
                                d = round(d / (20), 2)
                                val = "{0}pt".format(MiscHelper.out_double(d))
                                pt = SizeunitConverter.convert(st.get_attr("font-size"), "pt")
                                if (pt is not None and pt > 0): 
                                    val = MiscHelper.out_double(round(d / pt, 2))
                            else: 
                                pass
                            if (val is not None): 
                                st.add_attr("line-height", val, False)
            elif (Utils.getXmlLocalName(x) == "tcW"): 
                val = DocTextStyles.__read_attr_val(x, "w", None)
                if (val is not None): 
                    st.add_attr("width", DocTextStyles.__get_size_val(val), False)
            elif (Utils.getXmlLocalName(x) == "ind"): 
                for a in x.attrib.items(): 
                    if (Utils.getXmlAttrLocalName(a) == "left" or Utils.getXmlAttrLocalName(a) == "start"): 
                        st.add_attr("margin-left", DocTextStyles.__get_size_val(a[1]), False)
                    elif (Utils.getXmlAttrLocalName(a) == "right" or Utils.getXmlAttrLocalName(a) == "left"): 
                        st.add_attr("margin-right", DocTextStyles.__get_size_val(a[1]), False)
                    elif (Utils.getXmlAttrLocalName(a) == "firstLine"): 
                        st.add_attr("text-indent", DocTextStyles.__get_size_val(a[1]), False)
                    elif (Utils.getXmlAttrLocalName(a) == "hanging"): 
                        st.add_attr("text-indent", "-" + DocTextStyles.__get_size_val(a[1]), False)
    
    def read_theme(self, node : xml.etree.ElementTree.Element) -> None:
        for x1 in node: 
            for x2 in x1: 
                if (Utils.getXmlLocalName(x2) == "fontScheme"): 
                    for x3 in x2: 
                        if (Utils.getXmlLocalName(x3) == "majorFont" or Utils.getXmlLocalName(x3) == "minorFont"): 
                            for x4 in x3: 
                                if (Utils.getXmlLocalName(x4) == "latin"): 
                                    if (Utils.getXmlLocalName(x3) == "majorFont"): 
                                        self.__m_major_font = DocTextStyles.__read_attr_val(x4, "typeface", None)
                                    else: 
                                        self.__m_minor_font = DocTextStyles.__read_attr_val(x4, "typeface", None)
    
    def read_all_styles(self, node : xml.etree.ElementTree.Element) -> None:
        for xnum in node: 
            if (Utils.getXmlLocalName(xnum) == "docDefaults"): 
                for x in xnum: 
                    if (Utils.getXmlLocalName(x) == "rPrDefault"): 
                        for xx in x: 
                            if (Utils.getXmlLocalName(xx) == "rPr"): 
                                self.def_style = UnitextStyle()
                                self.read_unitext_style(xx, self.def_style)
            elif (Utils.getXmlLocalName(xnum) == "style" and xnum.attrib is not None and len(xnum.attrib) >= 1): 
                id0_ = DocTextStyles.__read_attr_val(xnum, "styleId", None)
                if (id0_ is None or id0_ in self.m_text_styles): 
                    continue
                sty = DocTextStyle()
                if (self.def_style is not None): 
                    sty.ustyle = self.def_style.clone(False)
                self.m_text_styles[id0_] = sty
                for x in xnum: 
                    if (Utils.getXmlLocalName(x) == "name"): 
                        if (x.attrib is not None and len(x.attrib) > 0): 
                            sty.name = Utils.getXmlAttrByIndex(x.attrib, 0)[1]
                    elif (Utils.getXmlLocalName(x) == "aliases"): 
                        if (x.attrib is not None and len(x.attrib) > 0): 
                            sty.aliases = Utils.getXmlAttrByIndex(x.attrib, 0)[1]
                    elif (Utils.getXmlLocalName(x) == "basedOn"): 
                        if (x.attrib is not None): 
                            for a in x.attrib.items(): 
                                if (Utils.getXmlAttrLocalName(a) == "val" and a[1] in self.m_text_styles): 
                                    st0 = self.m_text_styles[a[1]]
                                    sty.num_id = st0.num_id
                                    sty.num_lvl = st0.num_lvl
                                    sty.ustyle = st0.ustyle.clone(False)
                    elif (Utils.getXmlLocalName(x) == "rPr"): 
                        self.read_unitext_style(x, sty.ustyle)
                        if (DocTextStyles.__read_attr_val(xnum, "default", None) == "1"): 
                            if (DocTextStyles.__read_attr_val(xnum, "type", None) == "paragraph"): 
                                self.def_style = sty.ustyle
                    elif (Utils.getXmlLocalName(x) == "pPr"): 
                        self.read_unitext_style(x, sty.ustyle)
                        for xx in x: 
                            if (Utils.getXmlLocalName(xx) == "numPr"): 
                                for xxx in xx: 
                                    if (Utils.getXmlLocalName(xxx) == "numId" and xxx.attrib is not None): 
                                        for a in xxx.attrib.items(): 
                                            if (Utils.getXmlAttrLocalName(a) == "val"): 
                                                sty.num_id = a[1]
                                    elif (Utils.getXmlLocalName(xxx) == "ilvl" and xxx.attrib is not None): 
                                        for a in xxx.attrib.items(): 
                                            if (Utils.getXmlAttrLocalName(a) == "val"): 
                                                ll = 0
                                                wrapll443 = RefOutArgWrapper(0)
                                                inoutres444 = Utils.tryParseInt(a[1], wrapll443)
                                                ll = wrapll443.value
                                                if (inoutres444): 
                                                    sty.num_lvl = ll
                if (sty.is_heading): 
                    sty.ustyle.add_attr("heading-level", str(sty.calc_heading_level()), False)