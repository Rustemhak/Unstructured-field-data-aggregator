# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import pathlib
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.UnitextPlaintextType import UnitextPlaintextType
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextList import UnitextList
from pullenti.unitext.GetPlaintextParam import GetPlaintextParam
from pullenti.unitext.internal.uni.UniTextGenCell import UniTextGenCell
from pullenti.unitext.internal.misc.WebdingsHelper import WebdingsHelper
from pullenti.unitext.internal.misc.SymbolHelper import SymbolHelper
from pullenti.unitext.internal.misc.WingdingsHelper import WingdingsHelper
from pullenti.unitext.UnitextHyperlink import UnitextHyperlink
from pullenti.unitext.UnitextImage import UnitextImage
from pullenti.unitext.internal.uni.UnitextGenTable import UnitextGenTable
from pullenti.unitext.internal.html.HtmlNode import HtmlNode
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.UnitextDocument import UnitextDocument
from pullenti.unitext.UnitextFootnote import UnitextFootnote
from pullenti.unitext.UnitextListitem import UnitextListitem
from pullenti.unitext.internal.html.HtmlTag import HtmlTag
from pullenti.unitext.internal.uni.UnitextGen import UnitextGen
from pullenti.unitext.UnitextComment import UnitextComment
from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
from pullenti.unitext.UnitextPagesectionItem import UnitextPagesectionItem
from pullenti.unitext.UnitextPagesection import UnitextPagesection
from pullenti.unitext.internal.html.HtmlSection import HtmlSection

class UnitextHtmlGen:
    
    class MsoListItem:
        
        def __init__(self) -> None:
            self.level = 0
            self.list_id = None;
            self.item = None;
        
        @staticmethod
        def _new58(_arg1 : str) -> 'MsoListItem':
            res = UnitextHtmlGen.MsoListItem()
            res.list_id = _arg1
            return res
    
    def __init__(self) -> None:
        self.__m_dir_name = None
        self.__m_images = None
        self.__m_foots = dict()
        self.__m_anno = dict()
        self.__m_shapes = dict()
        self.__m_ignored = list()
    
    def create(self, nod : 'HtmlNode', dir_name : str, images : typing.List[tuple], pars : 'CreateDocumentParam') -> 'UnitextDocument':
        if (dir_name is not None and pathlib.Path(dir_name).is_dir()): 
            self.__m_dir_name = dir_name
        self.__m_images = images
        doc = UnitextDocument._new41(FileFormat.HTML)
        self.__prepare(nod, False)
        if (pars.load_document_structure): 
            s = HtmlSection.create(nod)
            if (s is not None): 
                doc.content = s.generate(self)
                if (len(s.head) > 0 or len(s.tail) > 0): 
                    doc.sections.append(UnitextPagesection())
                    if (len(s.head) > 0): 
                        gen = UnitextGen()
                        for n in s.head: 
                            self.get_uni_text(n, gen, None, 0)
                        doc.sections[0].items.append(UnitextPagesectionItem._new42(gen.finish(True, None)))
                    if (len(s.tail) > 0): 
                        gen = UnitextGen()
                        for n in s.tail: 
                            self.get_uni_text(n, gen, None, 0)
                        doc.sections[0].items.append(UnitextPagesectionItem._new43(True, gen.finish(True, None)))
        if (doc.content is None): 
            gen = UnitextGen()
            self.get_uni_text(nod, gen, None, 0)
            doc.content = gen.finish(True, None)
        h = nod.find_subnode("HEAD", None, None)
        ti = (h.find_subnode("TITLE", None, None) if h is not None else None)
        if (ti is not None and ti.text is not None and not "title" in doc.attrs): 
            doc.attrs["title"] = ti.text.strip()
        doc.optimize(False, None)
        return doc
    
    def __prepare(self, nod : 'HtmlNode', ok_foots : bool) -> None:
        val = nod.get_attribute("STYLE")
        if (val is not None and (("footnote-list" in val or "endnote-list" in val or "comment-list" in val))): 
            ok_foots = True
            self.__m_ignored.append(nod)
        if (ok_foots and nod.tag_name == "P"): 
            val = nod.get_attribute("CLASS")
            if (val == "MsoFootnoteText" or val == "MsoEndnoteText" or val == "MsoCommentText"): 
                nam = None
                val1 = None
                val1 = nod.get_attribute("NAME")
                if ((val1) is not None): 
                    nam = val1
                else: 
                    ch = nod.find_subnode("A", "NAME", None)
                    if (ch is None and nod.parent is not None and val == "MsoCommentText"): 
                        ch = nod.parent.find_subnode("A", "NAME", None)
                    if (ch is not None): 
                        val1 = ch.get_attribute("NAME")
                        nam = val1
                        if (nam is not None): 
                            self.__m_ignored.append(ch)
                if (nam is not None): 
                    if ("Comment" in val): 
                        if (not nam in self.__m_anno): 
                            gg = UnitextGen()
                            self.get_uni_text(nod, gg, None, 0)
                            it = gg.finish(True, None)
                            if (it is not None): 
                                tmp = io.StringIO()
                                it.get_plaintext(tmp, None)
                                if (tmp.tell() > 0): 
                                    if (Utils.toStringStringIO(tmp).find('[') >= 0): 
                                        ii = Utils.toStringStringIO(tmp).find(']')
                                        if (ii > 0): 
                                            Utils.removeStringIO(tmp, 0, ii + 1)
                                    self.__m_anno[nam] = UnitextComment._new44(Utils.toStringStringIO(tmp).strip())
                    else: 
                        gg = UnitextGen()
                        self.get_uni_text(nod, gg, None, 0)
                        fn = UnitextFootnote()
                        fn.is_endnote = "Endnote" in val
                        fn.content = gg.finish(True, None)
                        if (not nam in self.__m_foots): 
                            self.__m_foots[nam] = fn
                return
        ii = 0
        while ii < len(nod.children): 
            self.__prepare(nod.children[ii], ok_foots)
            ii += 1
    
    def get_uni_text(self, nod : 'HtmlNode', res : 'UnitextGen', blk : object, lev : int) -> None:
        if (lev > 100): 
            return
        tag_name = nod.tag_name
        if ((tag_name == "SCRIPT" or tag_name == "NOSCRIPT" or tag_name == "STYLE") or tag_name == "META" or tag_name == "TITLE"): 
            return
        if (tag_name == "DEL"): 
            return
        if (tag_name == "TEMPLATE"): 
            return
        if (nod in self.__m_ignored): 
            return
        tag = HtmlTag.find_tag(tag_name)
        st = nod.get_attribute("STYLE")
        if (st is not None and "page-break-before" in st.lower()): 
            res.append_pagebreak()
        if (tag is not None and tag.name == "BR"): 
            if (res is not None): 
                res.append_newline(False)
            return
        if (tag is not None and tag.name == "TABLE"): 
            tbl = UnitextGenTable()
            ii = 0
            while ii < len(nod.children): 
                self.get_uni_text(nod.children[ii], None, tbl, lev + 1)
                ii += 1
            if (res is not None): 
                tab = tbl.convert()
                if (tab is not None): 
                    tab.width = nod.get_style_value("width")
                    if ((tab.width) is None): 
                        tab.width = nod.get_attribute("WIDTH")
                    vv = nod.get_attribute("BORDER")
                    if (vv is not None): 
                        if (vv.startswith("0")): 
                            tab.hide_borders = True
                    else: 
                        vv = nod.get_style_value("border")
                        if ((vv) is not None): 
                            if (vv.startswith("0")): 
                                tab.hide_borders = True
                        else: 
                            vv = nod.get_style_value("border-width")
                            if ((vv) is not None): 
                                if (vv.startswith("0")): 
                                    tab.hide_borders = True
                    if (nod.get_style_value("BORDER") == "none"): 
                        if (nod.get_style_value("MSO-BORDER-ALT") is None): 
                            tab.hide_borders = True
                    if (res.last_char != '\r'): 
                        res.append_newline(False)
                    res.append(tab, None, -1, False)
                res.append_newline(False)
            return
        if (tag is not None and tag.name == "TR"): 
            tab = Utils.asObjectOrNull(blk, UnitextGenTable)
            if (tab is None): 
                return
            row = list()
            tab.cells.append(row)
            ii = 0
            first_pass626 = True
            while True:
                if first_pass626: first_pass626 = False
                else: ii += 1
                if (not (ii < len(nod.children))): break
                ch = nod.children[ii]
                tag2 = HtmlTag.find_tag(ch.tag_name)
                if (tag2 is None or ((tag2.name != "TD" and tag2.name != "TH"))): 
                    continue
                cel = UniTextGenCell()
                row.append(cel)
                colsp = 1
                rowsp = 1
                if (ch.get_attribute("ROWSPAN") is not None): 
                    wraprowsp45 = RefOutArgWrapper(0)
                    inoutres46 = Utils.tryParseInt(ch.get_attribute("ROWSPAN"), wraprowsp45)
                    rowsp = wraprowsp45.value
                    if (inoutres46): 
                        if (rowsp > 65534): 
                            rowsp = 65534
                        cel.row_span = rowsp
                if (ch.get_attribute("COLSPAN") is not None): 
                    wrapcolsp47 = RefOutArgWrapper(0)
                    inoutres48 = Utils.tryParseInt(ch.get_attribute("COLSPAN"), wrapcolsp47)
                    colsp = wrapcolsp47.value
                    if (inoutres48): 
                        if (colsp < 100): 
                            cel.col_span = colsp
                if (colsp <= 1): 
                    wi = Utils.ifNotNull(ch.get_style_value("width"), ch.get_attribute("WIDTH"))
                    if (wi is not None): 
                        cel.width = wi
                gg = UnitextGen()
                self.get_uni_text(ch, gg, None, lev + 1)
                cel.content = gg.finish(True, None)
            return
        if (tag is not None and tag.name == "COLGROUP"): 
            tab = Utils.asObjectOrNull(blk, UnitextGenTable)
            if (tab is None): 
                return
            ii = 0
            first_pass627 = True
            while True:
                if first_pass627: first_pass627 = False
                else: ii += 1
                if (not (ii < len(nod.children))): break
                ch = nod.children[ii]
                tag2 = HtmlTag.find_tag(ch.tag_name)
                if (tag2 is None or tag2.name != "COL"): 
                    continue
                wi = Utils.ifNotNull(ch.get_style_value("width"), ch.get_attribute("WIDTH"))
                tab.m_col_width.append(wi)
            return
        if (tag is not None and ((tag.name == "OL" or tag.name == "UL"))): 
            li = UnitextList()
            li_num = 0
            li_typ = None
            if (tag.name == "OL"): 
                wrapli_num49 = RefOutArgWrapper(0)
                inoutres50 = Utils.tryParseInt(Utils.ifNotNull(nod.get_attribute("START"), ""), wrapli_num49)
                li_num = wrapli_num49.value
                if (not inoutres50): 
                    li_num = 1
                li_typ = (Utils.ifNotNull(nod.get_attribute("TYPE"), "1"))
            else: 
                li.unorder_prefix = ""
            ii = 0
            first_pass628 = True
            while True:
                if first_pass628: first_pass628 = False
                else: ii += 1
                if (not (ii < len(nod.children))): break
                ch = nod.children[ii]
                tag2 = HtmlTag.find_tag(ch.tag_name)
                if (tag2 is None or tag2.name != "LI"): 
                    continue
                it = UnitextListitem()
                li.items.append(it)
                gg = UnitextGen()
                self.get_uni_text(ch, gg, None, lev + 1)
                it.content = gg.finish(True, None)
                if (li_num > 0 and li_typ is not None and li.unorder_prefix is None): 
                    pref = HtmlNode._get_li_num(li_num, li_typ)
                    if (pref is not None): 
                        it.prefix = (UnitextPlaintext._new51(pref))
                    li_num += 1
            if (res is not None): 
                res.append(li, None, -1, False)
            return
        if (tag is not None and ((tag.name == "SUP" or tag.name == "SUB"))): 
            tmp = io.StringIO()
            if (len(nod.children) == 0): 
                print(nod.text, end="", file=tmp)
            else: 
                ii = 0
                while ii < len(nod.children): 
                    nod.children[ii]._get_full_text(tmp, None, None)
                    ii += 1
            tt = Utils.toStringStringIO(tmp).strip()
            if (len(tt) > 0 and (len(tt) < 10)): 
                res.append(UnitextPlaintext._new52(tt, (UnitextPlaintextType.SUB if tag.name == "SUB" else UnitextPlaintextType.SUP)), None, -1, False)
                return
        if (res is None): 
            ii = 0
            while ii < len(nod.children): 
                self.get_uni_text(nod.children[ii], res, blk, lev + 1)
                ii += 1
            return
        if (tag_name == "A"): 
            val = nod.get_attribute("HREF")
            if (val is not None): 
                fn = None
                wrapfn54 = RefOutArgWrapper(None)
                inoutres55 = Utils.tryGetValue(self.__m_foots, val[1:], wrapfn54)
                fn = wrapfn54.value
                if (val.startswith("#") and inoutres55): 
                    res.append(fn, None, -1, False)
                    return
                if (val.startswith("#") and val[1:] in self.__m_anno): 
                    res.append(self.__m_anno[val[1:]], None, -1, False)
                    return
                if (len(nod.children) > 0): 
                    no_tag = False
                    if (len(nod.children) > 20): 
                        no_tag = True
                    else: 
                        for ch in nod.children: 
                            if (ch.has_tag("A") or ch.has_block_tag()): 
                                no_tag = True
                                break
                    if (no_tag and (isinstance(nod.parent, HtmlNode))): 
                        i = Utils.indexOfList(nod.parent.children, nod, 0)
                        if (i >= 0): 
                            nod.parent.children[i + 1:i + 1] = nod.children
                        nod.children.clear()
                gg = UnitextGen()
                if (nod.text is not None): 
                    gg.append_text(nod.text, False)
                for ch in nod.children: 
                    self.get_uni_text(ch, gg, None, lev + 1)
                it = gg.finish(True, None)
                if (it is not None): 
                    hr = UnitextHyperlink._new53(val)
                    hr.content = it
                    res.append(hr, None, -1, False)
                    return
                val = nod.get_attribute("CLASS")
                if (Utils.compareStrings(Utils.ifNotNull(val, ""), "MSOCOMANCHOR", True) == 0): 
                    return
        if (tag_name == "V:TEXTBOX"): 
            pass
        if (tag_name == "V:IMAGEDATA" or tag_name == "IMG"): 
            shapes = nod.get_attribute("V:SHAPES")
            if (shapes is not None): 
                ids = Utils.splitString(shapes, ' ', False)
            img = UnitextImage()
            img.id0_ = nod.get_attribute("SRC")
            if ((img.id0_) is not None): 
                try: 
                    if (self.__m_dir_name is not None): 
                        if (img.id0_ is not None and not img.id0_.startswith("http")): 
                            fname = pathlib.PurePath(self.__m_dir_name).joinpath((Utils.ifNotNull(img.id0_, "")))
                            if (not pathlib.Path(fname).is_file()): 
                                fname = fname.replace('/', '\\')
                            if (pathlib.Path(fname).is_file()): 
                                img.content = UnitextHelper.load_data_from_file(fname, 0)
                    elif (self.__m_images is not None): 
                        for kp in self.__m_images.items(): 
                            if (kp[0].endswith(img.id0_)): 
                                img.content = kp[1]
                                break
                    res.append(img, None, -1, False)
                    hh = nod
                    while hh is not None: 
                        val = None
                        val = hh.get_style_value("WIDTH")
                        if ((val) is not None): 
                            img.width = UnitextGen._convert_to_pt(val, "px")
                        val = hh.get_style_value("HEIGHT")
                        if ((val) is not None): 
                            img.height = UnitextGen._convert_to_pt(val, "px")
                        if (img.width is not None or img.height is not None): 
                            break
                        val = hh.get_attribute("WIDTH")
                        if ((val) is not None): 
                            img.width = UnitextGen._convert_to_pt(val, "px")
                        val = hh.get_attribute("HEIGHT")
                        if ((val) is not None): 
                            img.height = UnitextGen._convert_to_pt(val, "px")
                        hh = (Utils.asObjectOrNull(hh.parent, HtmlNode))
                    if (img.width is None or img.height is None): 
                        img.height = None
                        img.width = img.height
                except Exception as ex56: 
                    pass
                return
        is_block = False
        if (tag is not None and ((tag.is_block or tag.is_table))): 
            is_block = True
        ish = False
        if (is_block): 
            res.append_newline(False)
            if (len((Utils.ifNotNull(tag_name, ""))) == 2): 
                if (((tag_name[0] == 'H' or tag_name[0] == 'h')) and str.isdigit(tag_name[1])): 
                    ish = True
                    res.append_newline(False)
                    if (tag_name[0] == '1'): 
                        res.append_newline(False)
        if (not Utils.isNullOrEmpty(nod.text)): 
            cou = 0
            wingdings = False
            webdings = False
            symbols = False
            pp = nod
            while pp is not None and (cou < 2): 
                ff = Utils.ifNotNull(pp.get_style_value("font-family"), pp.get_style_value("font"))
                if (ff is not None): 
                    if ("WINGDINGS" in ff.upper()): 
                        wingdings = True
                    elif ("WEBDINGS" in ff.upper()): 
                        webdings = True
                    elif ("SYMBOL" in ff.upper()): 
                        symbols = True
                    break
                pp = (Utils.asObjectOrNull(pp.parent, HtmlNode)); cou += 1
            if (wingdings): 
                res.append_text(WingdingsHelper.get_unicode_string(nod.text), False)
            elif (webdings): 
                res.append_text(WebdingsHelper.get_unicode_string(nod.text), False)
            elif (symbols): 
                res.append_text(SymbolHelper.get_unicode_string(nod.text), False)
            else: 
                res.append_text(nod.text, False)
        elif (len(nod.children) == 1): 
            cou = 0
            nn = nod
            while nn is not None: 
                if (len(nn.children) != 1): 
                    break
                if (nn.children[0].text is not None): 
                    break
                cou += 1
                nn = nn.children[0]
            if (cou > 100 and nn is not None): 
                nod = nn
            else: 
                nod = nod.children[0]
            self.get_uni_text(nod, res, None, lev + 1)
        else: 
            first = True
            lists = None
            list_id = None
            ii = 0
            first_pass629 = True
            while True:
                if first_pass629: first_pass629 = False
                else: ii += 1
                if (not (ii < len(nod.children))): break
                ch = nod.children[ii]
                li = self.__try_parse_list(ch, lev + 1)
                if (li is not None and li.item.content is None and nod.tag_name == "TD"): 
                    li = (None)
                if (li is None): 
                    if (lists is not None): 
                        if (len(ch.children) == 0 and len((Utils.ifNotNull(ch.text, "")).strip()) == 0): 
                            continue
                        lists = (None)
                        list_id = (None)
                elif (li.list_id != list_id and list_id is not None): 
                    list_id = (None)
                    lists = (None)
                if (li is not None): 
                    if (lists is None): 
                        list0_ = UnitextList()
                        if (res.last_char != '\r'): 
                            res.append_newline(False)
                        res.append(list0_, None, -1, False)
                        res.append_newline(False)
                        lists = list()
                        lists.append(list0_)
                        list_id = li.list_id
                    if (li.level == 3): 
                        pass
                    if (li.level == len(lists)): 
                        lists[0].items.append(li.item)
                        continue
                    if (li.level < len(lists)): 
                        while li.level < len(lists):
                            del lists[0]
                        lists[0].items.append(li.item)
                        continue
                    if (li.level == (len(lists) + 1) and len(lists[0].items) > 0): 
                        last = lists[0].items[len(lists[0].items) - 1]
                        if (last.sublist is None): 
                            last.sublist = UnitextList._new57(li.level - 1)
                        lists.insert(0, last.sublist)
                        last.sublist.items.append(li.item)
                        continue
                if (first): 
                    first = False
                elif (not ch.whitespace_preserve): 
                    res.append_text(" ", False)
                self.get_uni_text(ch, res, None, lev + 1)
        if (ish): 
            res.append_newline(False)
            if (tag_name[0] == '1'): 
                res.append_newline(False)
    
    def __try_parse_list(self, nod : 'HtmlNode', lev : int) -> 'MsoListItem':
        if (nod.tag_name != "P"): 
            return None
        val = nod.get_attribute("STYLE")
        if (val is None): 
            return None
        i = val.find("mso-list:")
        if (i < 0): 
            return None
        val = val[i + 9:].strip()
        fi = Utils.splitString(val, ' ', False)
        if (len(fi) < 3): 
            return None
        if (not Utils.startsWithString(fi[2], "LFO", True)): 
            return None
        res = UnitextHtmlGen.MsoListItem._new58(fi[2])
        wrapi60 = RefOutArgWrapper(0)
        inoutres61 = Utils.tryParseInt(fi[1][5:], wrapi60)
        i = wrapi60.value
        if (not Utils.startsWithString(fi[1], "level", True) or not inoutres61): 
            return None
        res.level = i
        if (i < 1): 
            return None
        if (len(nod.children) == 1 and nod.children[0].tag_name == "A"): 
            nod = nod.children[0]
        i = 0
        first_pass630 = True
        while True:
            if first_pass630: first_pass630 = False
            else: i += 1
            if (not (i < len(nod.children))): break
            ch = nod.children[i]
            if (ch.tag_name != "SPAN"): 
                continue
            val = ch.get_attribute("STYLE")
            if ((val) is not None and "Ignore" in val): 
                pass
            elif (ch.find_subnode("SPAN", "STYLE", "mso-list:Ignore") is not None): 
                pass
            elif (i == 0): 
                pass
            else: 
                continue
            tmp = io.StringIO()
            ch._get_full_text(tmp, GetPlaintextParam(), None)
            res.item = UnitextListitem()
            if (tmp.tell() > 0): 
                res.item.prefix = (UnitextPlaintext._new51(Utils.toStringStringIO(tmp).strip()))
            gg = UnitextGen()
            nod.children[i] = HtmlNode()
            nod.tag_name = "PPP"
            self.get_uni_text(nod, gg, None, lev + 1)
            nod.children[i] = ch
            nod.tag_name = "P"
            res.item.content = gg.finish(True, None)
            return res
        return None