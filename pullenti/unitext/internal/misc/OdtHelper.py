# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
import io
import typing
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.internal.uni.UnitextGenTable import UnitextGenTable
from pullenti.unitext.internal.uni.UniTextGenCell import UniTextGenCell
from pullenti.unitext.internal.uni.IUnitextGenNumStyle import IUnitextGenNumStyle
from pullenti.unitext.internal.misc.SymbolHelper import SymbolHelper
from pullenti.unitext.internal.misc.WingdingsHelper import WingdingsHelper
from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.unitext.UnitextPlaintextType import UnitextPlaintextType
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextList import UnitextList
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextDocument import UnitextDocument
from pullenti.unitext.UnitextImage import UnitextImage
from pullenti.unitext.UnitextComment import UnitextComment
from pullenti.unitext.internal.uni.UniTextGenNumType import UniTextGenNumType
from pullenti.unitext.internal.uni.UnitextGenNumStyle import UnitextGenNumStyle
from pullenti.unitext.UnitextHyperlink import UnitextHyperlink
from pullenti.unitext.internal.uni.UniTextGenNumLevel import UniTextGenNumLevel
from pullenti.unitext.UnitextFootnote import UnitextFootnote
from pullenti.unitext.internal.uni.UnitextGen import UnitextGen
from pullenti.unitext.UnitextPagesectionItem import UnitextPagesectionItem
from pullenti.unitext.UnitextPagesection import UnitextPagesection

class OdtHelper:
    
    class OdtStyle:
        
        def __init__(self) -> None:
            self.name = None;
            self.parent_name = None;
            self.font_family = None;
            self.is_super = False
            self.is_sub = False
            self.is_wingdings = False
            self.is_symbol = False
            self.num_style_id = None;
            self.table_width = None;
            self.table_column_width = 0
    
    def __init__(self) -> None:
        self.__m_styles = dict()
        self.__m_nums = dict()
        self.__m_outline_num = None;
    
    def create_uni(self, xml0_ : xml.etree.ElementTree.Element, styles : xml.etree.ElementTree.Element) -> 'UnitextDocument':
        if (Utils.getXmlLocalName(xml0_) != "document-content"): 
            return None
        doc = UnitextDocument._new41(FileFormat.ODT)
        sect = UnitextPagesection()
        if (styles is not None): 
            for x in styles: 
                if (Utils.getXmlLocalName(x) == "master-styles"): 
                    for xx in x: 
                        if (Utils.getXmlLocalName(xx) == "master-page"): 
                            for xxx in xx: 
                                if (Utils.getXmlLocalName(xxx) == "header"): 
                                    gg = UnitextGen()
                                    self.__read_gen0(xxx, gg, True, None, 0)
                                    sect.items.append(UnitextPagesectionItem._new42(gg.finish(True, None)))
                                elif (Utils.getXmlLocalName(xxx) == "footer"): 
                                    gg = UnitextGen()
                                    self.__read_gen0(xxx, gg, True, None, 0)
                                    sect.items.append(UnitextPagesectionItem._new43(True, gg.finish(True, None)))
                            break
                elif (Utils.getXmlLocalName(x) == "styles"): 
                    for xx in x: 
                        if (Utils.getXmlLocalName(xx) == "style"): 
                            self.__read_style(xx)
                        elif (Utils.getXmlLocalName(xx) == "list-style"): 
                            self.__read_list_style(xx)
        if (len(sect.items) > 0): 
            doc.sections.append(sect)
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "automatic-styles"): 
                for xx in x: 
                    if (Utils.getXmlLocalName(xx) == "style"): 
                        self.__read_style(xx)
                    elif (Utils.getXmlLocalName(xx) == "list-style"): 
                        self.__read_list_style(xx)
            elif (Utils.getXmlLocalName(x) == "body"): 
                gen = UnitextGen()
                self.__read_gen0(x, gen, False, None, 0)
                doc.content = gen.finish(True, None)
        doc.optimize(False, None)
        if (doc.content is None): 
            return None
        return doc
    
    def __read_style(self, xx : xml.etree.ElementTree.Element) -> None:
        sty = OdtHelper.OdtStyle()
        if (xx.attrib is not None): 
            for a in xx.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "name"): 
                    sty.name = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "family"): 
                    sty.font_family = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "parent-style-name"): 
                    sty.parent_name = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "list-style-name"): 
                    sty.num_style_id = a[1]
        if (sty.name is None or sty.name in self.__m_styles): 
            return
        self.__m_styles[sty.name] = sty
        for p in xx: 
            if (Utils.getXmlLocalName(p) == "text-properties"): 
                if (p.attrib is not None): 
                    for a in p.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "text-position"): 
                            if (a[1].startswith("super")): 
                                sty.is_super = True
                            elif (a[1].startswith("sub")): 
                                sty.is_sub = True
                        elif (Utils.getXmlAttrLocalName(a) == "font-name"): 
                            if (a[1] == "Wingdings"): 
                                sty.is_wingdings = True
                            elif (a[1] == "Symbol"): 
                                sty.is_symbol = True
            elif (Utils.getXmlLocalName(p) == "table-column-properties"): 
                if (p.attrib is not None): 
                    for a in p.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "column-width"): 
                            dd = UnitextGen._convert_tomm(a[1], None)
                            if (dd > 0): 
                                sty.table_column_width = (dd)
                                continue
                            vv = a[1]
                            if (vv.endswith("in")): 
                                vv = vv[0:0+len(vv) - 2]
                            d = 0
                            wrapd106 = RefOutArgWrapper(0)
                            inoutres107 = MiscHelper.try_parse_double(vv, wrapd106)
                            d = wrapd106.value
                            if (inoutres107): 
                                sty.table_column_width = d
            elif (Utils.getXmlLocalName(p) == "table-properties"): 
                if (p.attrib is not None): 
                    for a in p.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "width"): 
                            sty.table_width = a[1]
    
    def __read_list_style(self, xx : xml.etree.ElementTree.Element) -> None:
        nam = None
        if (xx.attrib is not None): 
            for a in xx.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "name"): 
                    nam = a[1]
        if (nam is None): 
            return
        num = UnitextGenNumStyle._new108(nam)
        self.__read_odt_num_style(num, xx)
        if (not nam in self.__m_nums): 
            self.__m_nums[nam] = num
    
    def __read_odt_num_style(self, num : 'UnitextGenNumStyle', xml0_ : xml.etree.ElementTree.Element) -> None:
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "list-level-style-number"): 
                lev = UniTextGenNumLevel()
                num.levels.append(lev)
                pref = None
                suf = None
                frm = "1"
                cou = 1
                if (x.attrib is not None): 
                    for a in x.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "num-suffix"): 
                            suf = a[1]
                        elif (Utils.getXmlAttrLocalName(a) == "num-prefix"): 
                            pref = a[1]
                        elif (Utils.getXmlAttrLocalName(a) == "num-format"): 
                            frm = a[1]
                        elif (Utils.getXmlAttrLocalName(a) == "display-levels"): 
                            wrapcou109 = RefOutArgWrapper(0)
                            Utils.tryParseInt(a[1], wrapcou109)
                            cou = wrapcou109.value
                        elif (Utils.getXmlAttrLocalName(a) == "start-value"): 
                            nn = 0
                            wrapnn110 = RefOutArgWrapper(0)
                            inoutres111 = Utils.tryParseInt(a[1], wrapnn110)
                            nn = wrapnn110.value
                            if (inoutres111): 
                                lev.start = nn
                if (frm == "1"): 
                    lev.type0_ = UniTextGenNumType.DECIMAL
                elif (frm == "a"): 
                    lev.type0_ = UniTextGenNumType.LOWERLETTER
                elif (frm == "A"): 
                    lev.type0_ = UniTextGenNumType.UPPERLETTER
                elif (frm == "i"): 
                    lev.type0_ = UniTextGenNumType.LOWERROMAN
                elif (frm == "I"): 
                    lev.type0_ = UniTextGenNumType.UPPERROMAN
                elif (frm.startswith("А")): 
                    lev.type0_ = UniTextGenNumType.UPPERCYRLETTER
                elif (frm.startswith("а")): 
                    lev.type0_ = UniTextGenNumType.LOWERCYRLETTER
                tmp = io.StringIO()
                if (pref is not None): 
                    print(pref, end="", file=tmp)
                i = (len(num.levels) + 1) - cou
                while i <= len(num.levels): 
                    prev_frm = None
                    if (i < len(num.levels)): 
                        prev_frm = num.levels[i - 1].format0_
                    if (not Utils.isNullOrEmpty(prev_frm) and prev_frm[0] != '%'): 
                        print(prev_frm[0], end="", file=tmp)
                    print("%{0}".format(i), end="", file=tmp, flush=True)
                    if (not Utils.isNullOrEmpty(prev_frm) and not str.isdigit(prev_frm[len(prev_frm) - 1])): 
                        print(prev_frm[len(prev_frm) - 1], end="", file=tmp)
                    i += 1
                if (suf is not None): 
                    print(suf, end="", file=tmp)
                lev.format0_ = Utils.toStringStringIO(tmp)
            elif (Utils.getXmlLocalName(x) == "list-level-style-bullet"): 
                lev = UniTextGenNumLevel._new112(UniTextGenNumType.BULLET)
                if (x.attrib is not None): 
                    for a in x.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "bullet-char"): 
                            lev.format0_ = a[1]
                num.levels.append(lev)
    
    def __read_gen0(self, xml0_ : xml.etree.ElementTree.Element, gen : 'UnitextGen', pure : bool=False, num_style : 'UnitextGenNumStyle'=None, num_level : int=0) -> None:
        if (xml0_ is None): 
            return
        li = list()
        li.append(xml0_)
        self.__read_gen(li, gen, pure, num_style, num_level)
    
    def __read_gen(self, xml_stack : typing.List[xml.etree.ElementTree.Element], gen : 'UnitextGen', pure : bool=False, num_style : 'UnitextGenNumStyle'=None, num_level : int=0) -> None:
        xml0_ = xml_stack[len(xml_stack) - 1]
        if (not pure and Utils.getXmlLocalName(xml0_) != "#text"): 
            if (Utils.getXmlLocalName(xml0_) == "s"): 
                gen.append_text(" ", False)
                if (xml0_.attrib is not None): 
                    for a in xml0_.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "c"): 
                            cou = 0
                            wrapcou113 = RefOutArgWrapper(0)
                            inoutres114 = Utils.tryParseInt(Utils.ifNotNull(a[1], ""), wrapcou113)
                            cou = wrapcou113.value
                            if (inoutres114): 
                                while cou > 1: 
                                    gen.append_text(" ", False)
                                    cou -= 1
                return
            if (Utils.getXmlLocalName(xml0_) == "soft-page-break"): 
                gen.append_pagebreak()
                return
            if (Utils.getXmlLocalName(xml0_) == "line-break"): 
                gen.append_newline(False)
                return
            if (Utils.getXmlLocalName(xml0_) == "table"): 
                gt = UnitextGenTable()
                colwi = list()
                for r in xml0_: 
                    if (Utils.getXmlLocalName(r) == "table-row"): 
                        row = list()
                        gt.cells.append(row)
                        for c in r: 
                            if (Utils.getXmlLocalName(c) == "table-cell"): 
                                cel = UniTextGenCell()
                                row.append(cel)
                                if (c.attrib is not None): 
                                    for a in c.attrib.items(): 
                                        if (Utils.getXmlAttrLocalName(a) == "number-rows-spanned"): 
                                            nn = 0
                                            wrapnn115 = RefOutArgWrapper(0)
                                            inoutres116 = Utils.tryParseInt(a[1], wrapnn115)
                                            nn = wrapnn115.value
                                            if (inoutres116): 
                                                cel.row_span = nn
                                        elif (Utils.getXmlAttrLocalName(a) == "number-columns-spanned"): 
                                            nn = 0
                                            wrapnn117 = RefOutArgWrapper(0)
                                            inoutres118 = Utils.tryParseInt(a[1], wrapnn117)
                                            nn = wrapnn117.value
                                            if (inoutres118): 
                                                cel.col_span = nn
                                gg = UnitextGen()
                                xml_stack.append(c)
                                self.__read_gen(xml_stack, gg, True, num_style, num_level)
                                del xml_stack[len(xml_stack) - 1]
                                cel.content = gg.finish(True, None)
                    elif (Utils.getXmlLocalName(r) == "table-columns"): 
                        for x in r: 
                            if (Utils.getXmlLocalName(x) == "table-column"): 
                                if (xml0_.attrib is not None): 
                                    for a in x.attrib.items(): 
                                        if (Utils.getXmlAttrLocalName(a) == "style-name"): 
                                            sty1 = None
                                            wrapsty1119 = RefOutArgWrapper(None)
                                            inoutres120 = Utils.tryGetValue(self.__m_styles, a[1], wrapsty1119)
                                            sty1 = wrapsty1119.value
                                            if (inoutres120): 
                                                if (sty1.table_column_width > 0): 
                                                    colwi.append(sty1.table_column_width)
                                            break
                    elif (Utils.getXmlLocalName(r) == "table-column"): 
                        if (r.attrib is not None): 
                            for a in r.attrib.items(): 
                                if (Utils.getXmlAttrLocalName(a) == "style-name"): 
                                    sty1 = None
                                    wrapsty1121 = RefOutArgWrapper(None)
                                    inoutres122 = Utils.tryGetValue(self.__m_styles, a[1], wrapsty1121)
                                    sty1 = wrapsty1121.value
                                    if (inoutres122): 
                                        if (sty1.table_column_width > 0): 
                                            colwi.append(sty1.table_column_width)
                                    break
                sum0_ = 0
                for w in colwi: 
                    sum0_ += w
                if (sum0_ > 0): 
                    for w in colwi: 
                        gt.m_col_width.append("{0}%".format(math.floor(((w * (100)) / sum0_))))
                tab = gt.convert()
                if (tab is not None): 
                    gen.append(tab, None, -1, False)
                    return
            if (Utils.getXmlLocalName(xml0_) == "a"): 
                uri = None
                if (xml0_.attrib is not None): 
                    for a in xml0_.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "href"): 
                            uri = a[1]
                            break
                if (uri is not None): 
                    gg = UnitextGen()
                    xml_stack.append(xml0_)
                    self.__read_gen(xml_stack, gg, True, None, 0)
                    del xml_stack[len(xml_stack) - 1]
                    it = gg.finish(True, None)
                    if (it is not None): 
                        hr = UnitextHyperlink._new53(uri)
                        hr.content = it
                        gen.append(hr, None, -1, False)
                        return
            if (Utils.getXmlLocalName(xml0_) == "note"): 
                fn = UnitextFootnote()
                if (xml0_.attrib is not None): 
                    for a in xml0_.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "note-class" and a[1] == "endnote"): 
                            fn.is_endnote = True
                for x in xml0_: 
                    if (Utils.getXmlLocalName(x) == "note-body"): 
                        gg = UnitextGen()
                        xml_stack.append(x)
                        self.__read_gen(xml_stack, gg, True, None, 0)
                        del xml_stack[len(xml_stack) - 1]
                        fn.content = gg.finish(True, None)
                        break
                if (fn.content is not None): 
                    gen.append(fn, None, -1, False)
                return
            if (Utils.getXmlLocalName(xml0_) == "bookmark-ref"): 
                gg = UnitextGen()
                xml_stack.append(xml0_)
                self.__read_gen(xml_stack, gg, True, None, 0)
                del xml_stack[len(xml_stack) - 1]
                pl = Utils.asObjectOrNull(gg.finish(True, None), UnitextPlaintext)
                if (pl is not None): 
                    if (not gen.last_text.endswith(pl.text)): 
                        gen.append_text(pl.text, False)
                    return
            if (Utils.getXmlLocalName(xml0_) == "annotation"): 
                cmt = UnitextComment()
                gg = UnitextGen()
                for x in xml0_: 
                    if (Utils.getXmlLocalName(x) == "creator"): 
                        cmt.author = Utils.getXmlInnerText(x)
                    elif (Utils.getXmlLocalName(x) == "date"): 
                        pass
                    else: 
                        xml_stack.append(x)
                        self.__read_gen(xml_stack, gg, False, None, 0)
                        del xml_stack[len(xml_stack) - 1]
                it = gg.finish(True, None)
                if (it is not None): 
                    tmp = io.StringIO()
                    it.get_plaintext(tmp, None)
                    if (tmp.tell() > 0): 
                        cmt.text = Utils.toStringStringIO(tmp)
                        gen.append(cmt, None, -1, False)
                return
            out_line_level = 0
            num_sty = None
            if (Utils.getXmlLocalName(xml0_) == "p" or Utils.getXmlLocalName(xml0_) == "h"): 
                if (xml0_.attrib is not None): 
                    for a in xml0_.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "outline-level"): 
                            wrapout_line_level124 = RefOutArgWrapper(0)
                            Utils.tryParseInt(Utils.ifNotNull(a[1], ""), wrapout_line_level124)
                            out_line_level = wrapout_line_level124.value
                        elif (Utils.getXmlAttrLocalName(a) == "style-name"): 
                            sty1 = None
                            num0 = None
                            if (a[1] == "P5"): 
                                pass
                            wrapsty1128 = RefOutArgWrapper(None)
                            inoutres129 = Utils.tryGetValue(self.__m_styles, a[1], wrapsty1128)
                            sty1 = wrapsty1128.value
                            if (not inoutres129): 
                                continue
                            for kk in range(10):
                                if (sty1.num_style_id is not None): 
                                    wrapnum0125 = RefOutArgWrapper(None)
                                    Utils.tryGetValue(self.__m_nums, sty1.num_style_id, wrapnum0125)
                                    num0 = wrapnum0125.value
                                    break
                                if (sty1.parent_name is None): 
                                    break
                                wrapsty1126 = RefOutArgWrapper(None)
                                inoutres127 = Utils.tryGetValue(self.__m_styles, sty1.parent_name, wrapsty1126)
                                sty1 = wrapsty1126.value
                                if (not inoutres127): 
                                    break
                            if (num0 is None): 
                                continue
                            num_sty = num0
            if (out_line_level > 0 or num_sty is not None): 
                if (self.__m_outline_num is None and num_sty is None): 
                    self.__m_outline_num = UnitextGenNumStyle()
                    self.__m_outline_num.levels.append(UniTextGenNumLevel._new130(UniTextGenNumType.DECIMAL, "%1."))
                    self.__m_outline_num.levels.append(UniTextGenNumLevel._new130(UniTextGenNumType.DECIMAL, "%1.%2."))
                    self.__m_outline_num.levels.append(UniTextGenNumLevel._new130(UniTextGenNumType.DECIMAL, "%1.%2.%3."))
                    self.__m_outline_num.levels.append(UniTextGenNumLevel._new130(UniTextGenNumType.DECIMAL, "%1.%2.%3.%4."))
                    self.__m_outline_num.levels.append(UniTextGenNumLevel._new130(UniTextGenNumType.DECIMAL, "%1.%2.%3.%4.%5."))
                    self.__m_outline_num.levels.append(UniTextGenNumLevel._new130(UniTextGenNumType.DECIMAL, "%1.%2.%3.%4.%5.%6."))
                li = UnitextList._new57(out_line_level - 1)
                gg = UnitextGen()
                for x in xml0_: 
                    xml_stack.append(x)
                    self.__read_gen(xml_stack, gg, False, (self.__m_outline_num if num_sty is None else num_style), num_level)
                    del xml_stack[len(xml_stack) - 1]
                gen.append_newline(True)
                gen.append(gg.finish(True, None), (self.__m_outline_num if num_sty is None else num_sty), out_line_level - 1, False)
                gen.append_newline(False)
                gen.append(li, None, -1, False)
                return
            if (Utils.getXmlLocalName(xml0_) == "list"): 
                li = UnitextList._new57(num_level)
                num0 = None
                cont_num = False
                style_name = None
                if (xml0_.attrib is not None): 
                    for a in xml0_.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "style-name"): 
                            sty1 = None
                            wrapsty1143 = RefOutArgWrapper(None)
                            inoutres144 = Utils.tryGetValue(self.__m_styles, a[1], wrapsty1143)
                            sty1 = wrapsty1143.value
                            if (inoutres144): 
                                if (sty1.num_style_id is not None): 
                                    wrapnum0138 = RefOutArgWrapper(None)
                                    style_name = sty1.num_style_id
                                    Utils.tryGetValue(self.__m_nums, style_name, wrapnum0138)
                                    num0 = wrapnum0138.value
                                elif (sty1.parent_name is not None): 
                                    sty2 = None
                                    wrapsty2140 = RefOutArgWrapper(None)
                                    inoutres141 = Utils.tryGetValue(self.__m_styles, sty1.parent_name, wrapsty2140)
                                    sty2 = wrapsty2140.value
                                    if (inoutres141): 
                                        if (sty2.num_style_id is not None): 
                                            wrapnum0139 = RefOutArgWrapper(None)
                                            style_name = sty2.num_style_id
                                            Utils.tryGetValue(self.__m_nums, style_name, wrapnum0139)
                                            num0 = wrapnum0139.value
                            else: 
                                wrapnum0142 = RefOutArgWrapper(None)
                                style_name = a[1]
                                Utils.tryGetValue(self.__m_nums, style_name, wrapnum0142)
                                num0 = wrapnum0142.value
                                if (style_name == "L9"): 
                                    pass
                        elif (Utils.getXmlAttrLocalName(a) == "continue-numbering"): 
                            cont_num = True
                if (num_style is None or num0 is not None): 
                    num_style = num0
                    num_level = 0
                if (num_style is None): 
                    num_style = UnitextGenNumStyle()
                    num_style.levels.append(UniTextGenNumLevel._new130(UniTextGenNumType.DECIMAL, "%1."))
                    num_style.levels.append(UniTextGenNumLevel._new130(UniTextGenNumType.DECIMAL, "%1.%2."))
                    num_style.levels.append(UniTextGenNumLevel._new130(UniTextGenNumType.DECIMAL, "%1.%2.%3."))
                    num_style.levels.append(UniTextGenNumLevel._new130(UniTextGenNumType.DECIMAL, "%1.%2.%3.%4."))
                    num_style.levels.append(UniTextGenNumLevel._new130(UniTextGenNumType.DECIMAL, "%1.%2.%3.%4.%5."))
                    num_style.levels.append(UniTextGenNumLevel._new130(UniTextGenNumType.DECIMAL, "%1.%2.%3.%4.%5.%6."))
                    num_level = 0
                    if (style_name is not None and not style_name in self.__m_nums): 
                        self.__m_nums[style_name] = num_style
                for x in xml0_: 
                    if (Utils.getXmlLocalName(x) == "list-item"): 
                        n0 = 0
                        if (x.attrib is not None): 
                            for a in x.attrib.items(): 
                                if (Utils.getXmlAttrLocalName(a) == "start-value"): 
                                    wrapn0151 = RefOutArgWrapper(0)
                                    Utils.tryParseInt(a[1], wrapn0151)
                                    n0 = wrapn0151.value
                        start_sub_list = False
                        for xx in x: 
                            if (Utils.getXmlLocalName(xx) == "list"): 
                                start_sub_list = True
                            break
                        if (n0 > 0 and (num_level < len(num_style.levels))): 
                            num_style.levels[num_level].current = n0
                        gg = UnitextGen()
                        xml_stack.append(x)
                        self.__read_gen(xml_stack, gg, True, num_style, num_level + 1)
                        del xml_stack[len(xml_stack) - 1]
                        gen.append_newline(True)
                        if (start_sub_list): 
                            gen.append(gg.finish(True, None), None, 0, False)
                        else: 
                            gen.append(gg.finish(True, None), num_style, num_level, False)
                    elif (Utils.getXmlLocalName(x) == "list-header"): 
                        gg = UnitextGen()
                        xml_stack.append(x)
                        self.__read_gen(xml_stack, gg, True, num_style, num_level + 1)
                        del xml_stack[len(xml_stack) - 1]
                        gen.append_newline(True)
                        gen.append(gg.finish(True, None), None, 0, False)
                gen.append(li, None, -1, False)
                return
            if (Utils.getXmlLocalName(xml0_) == "custom-shape"): 
                gg = UnitextGen()
                xml_stack.append(xml0_)
                self.__read_gen(xml_stack, gg, True, None, 0)
                del xml_stack[len(xml_stack) - 1]
                it = gg.finish(True, None)
                if (it is None): 
                    return
                if (isinstance(it, UnitextContainer)): 
                    it.typ = UnitextContainerType.SHAPE
                else: 
                    cnt = UnitextContainer._new92(UnitextContainerType.SHAPE)
                    cnt.children.append(it)
                    it = cnt.optimize(False, None)
                if (it is not None): 
                    gen.append(it, None, -1, False)
                return
            if (Utils.getXmlLocalName(xml0_) == "image"): 
                img = UnitextImage()
                if (xml0_.attrib is not None): 
                    for a in xml0_.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "href"): 
                            img.id0_ = a[1]
                            break
                if (img.id0_ is not None): 
                    gen.append(img, None, -1, False)
                    xml_stack.append(xml0_)
                    for jj in range(len(xml_stack) - 1, -1, -1):
                        pp = xml_stack[jj]
                        if (pp.attrib is None): 
                            continue
                        for a in pp.attrib.items(): 
                            if (Utils.getXmlAttrLocalName(a) == "width" and img.width is None): 
                                img.width = UnitextGen._convert_to_pt(a[1], None)
                            elif (Utils.getXmlAttrLocalName(a) == "height" and img.height is None and a[1] is not None): 
                                img.height = UnitextGen._convert_to_pt(a[1], None)
                        if (img.width is not None or img.height is not None): 
                            break
                    del xml_stack[len(xml_stack) - 1]
                return
            sty = None
            if (xml0_.attrib is not None): 
                for a in xml0_.attrib.items(): 
                    if (Utils.getXmlAttrLocalName(a) == "style-name"): 
                        wrapsty154 = RefOutArgWrapper(None)
                        Utils.tryGetValue(self.__m_styles, a[1], wrapsty154)
                        sty = wrapsty154.value
                        if (a[1] == "T53"): 
                            pass
                        if (sty is not None and ((sty.is_super or sty.is_sub))): 
                            gg = UnitextGen()
                            xml_stack.append(xml0_)
                            self.__read_gen(xml_stack, gg, True, None, 0)
                            del xml_stack[len(xml_stack) - 1]
                            it = gg.finish(True, None)
                            if (it is None): 
                                continue
                            tmp = io.StringIO()
                            it.get_plaintext(tmp, None)
                            tt = Utils.toStringStringIO(tmp).strip()
                            if (len(tt) > 0 and (len(tt) < 100)): 
                                gen.append(UnitextPlaintext._new52(tt, (UnitextPlaintextType.SUB if sty.is_super else UnitextPlaintextType.SUP)), None, -1, False)
                                return
                        if (sty is not None and ((sty.is_wingdings or sty.is_symbol))): 
                            gg = UnitextGen()
                            xml_stack.append(xml0_)
                            self.__read_gen(xml_stack, gg, True, None, 0)
                            del xml_stack[len(xml_stack) - 1]
                            it = gg.finish(True, None)
                            if (it is None): 
                                continue
                            tmp = io.StringIO()
                            it.get_plaintext(tmp, None)
                            tt = (SymbolHelper.get_unicode_string(Utils.toStringStringIO(tmp).strip()) if sty.is_symbol else WingdingsHelper.get_unicode_string(Utils.toStringStringIO(tmp).strip()))
                            if (len(tt) > 0): 
                                gen.append_text(tt, False)
                            return
        if (Utils.getXmlLocalName(xml0_) == "p"): 
            gen.append_newline(True)
        elif (Utils.getXmlLocalName(xml0_) == "h"): 
            gen.append_newline(False)
        if (len(xml0_) == 0 and Utils.getXmlInnerText(xml0_) is not None): 
            txt = Utils.getXmlInnerText(xml0_)
            if (txt.find(chr(0xAD)) >= 0): 
                txt = txt.replace("{0}".format(chr(0xAD)), "")
            if (len(txt) == 1 and (ord(txt[0])) >= 0xF000): 
                gen.append_text("{0}".format(chr(((ord(txt[0])) - 0xF000))), False)
            else: 
                gen.append_text(txt, False)
        else: 
            for x in xml0_: 
                xml_stack.append(x)
                self.__read_gen(xml_stack, gen, False, num_style, num_level)
                del xml_stack[len(xml_stack) - 1]
        if (Utils.getXmlLocalName(xml0_) == "p" or Utils.getXmlLocalName(xml0_) == "h"): 
            gen.append_newline(False)
            if (Utils.getXmlLocalName(xml0_) == "h"): 
                gen.append_newline(False)