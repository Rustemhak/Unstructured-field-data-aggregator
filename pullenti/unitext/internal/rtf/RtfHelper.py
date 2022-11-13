# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextPlaintextType import UnitextPlaintextType
from pullenti.unitext.internal.misc.SymbolHelper import SymbolHelper
from pullenti.unitext.GetPlaintextParam import GetPlaintextParam
from pullenti.unitext.UnitextFootnote import UnitextFootnote
from pullenti.unitext.UnitextComment import UnitextComment
from pullenti.unitext.UnitextHyperlink import UnitextHyperlink
from pullenti.unitext.internal.rtf.RichTextItem import RichTextItem
from pullenti.unitext.internal.rtf.RichTextCell import RichTextCell
from pullenti.unitext.UnitextTable import UnitextTable
from pullenti.unitext.internal.rtf.RichTextRow import RichTextRow
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextMiscType import UnitextMiscType
from pullenti.unitext.UnitextMisc import UnitextMisc
from pullenti.unitext.internal.rtf.RichTextTable import RichTextTable
from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.internal.rtf.RtfItem import RtfItem
from pullenti.util.EncodingStandard import EncodingStandard
from pullenti.unitext.internal.rtf.RftItemTyp import RftItemTyp
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.internal.uni.UnitextGen import UnitextGen
from pullenti.unitext.UnitextDocument import UnitextDocument
from pullenti.util.EncodingWrapper import EncodingWrapper
from pullenti.unitext.UnitextImage import UnitextImage
from pullenti.unitext.internal.rtf.RtfItemImage import RtfItemImage
from pullenti.unitext.internal.misc.WingdingsHelper import WingdingsHelper
from pullenti.unitext.internal.html.HtmlParser import HtmlParser
from pullenti.unitext.UnitextPagesectionItem import UnitextPagesectionItem
from pullenti.unitext.UnitextPagesection import UnitextPagesection
from pullenti.unitext.internal.html.HtmlHelper import HtmlHelper

class RtfHelper:
    """ Поддержка формата RTF """
    
    class RtfEncoder:
        
        def __init__(self) -> None:
            self.level = 0
            self.encoding = None;
        
        def __str__(self) -> str:
            return "{0}: {1}".format(self.level, str(self.encoding))
        
        @staticmethod
        def _new236(_arg1 : int, _arg2 : 'EncodingWrapper') -> 'RtfEncoder':
            res = RtfHelper.RtfEncoder()
            res.level = _arg1
            res.encoding = _arg2
            return res
    
    class RtfTablerow(RtfItem):
        
        def __init__(self) -> None:
            super().__init__()
            self.props = list()
        
        @property
        def is_last(self) -> bool:
            return "lastrow" in self.props
        
        def __str__(self) -> str:
            return "{0}: TableRow{1}".format(self.level, (" Last" if self.is_last else ""))
    
    class RtfListinf(RtfItem):
        
        def __init__(self) -> None:
            super().__init__()
            self.props = list()
        
        def __str__(self) -> str:
            return "{0}: Listitem {1}".format(self.level, self.text)
    
    class RtfItemProxy(RtfItem):
        
        def __init__(self) -> None:
            super().__init__()
            self.uni = None;
        
        @staticmethod
        def _new271(_arg1 : 'RftItemTyp') -> 'RtfItemProxy':
            res = RtfHelper.RtfItemProxy()
            res.typ = _arg1
            return res
    
    M_LANG_ID_TO_CODEPAGE = None
    
    @staticmethod
    def __manage_encodings(items : typing.List['RtfItem']) -> None:
        font_charsets = dict()
        font_encodings = dict()
        font_name = None
        defs = list()
        curs = list()
        is_ansi = False
        i = 0
        first_pass649 = True
        while True:
            if first_pass649: first_pass649 = False
            else: i += 1
            if (not (i < len(items))): break
            it = items[i]
            while len(curs) > 0:
                if (curs[0].level > it.level): 
                    del curs[0]
                else: 
                    break
            while len(defs) > 0:
                if (defs[0].level > it.level): 
                    del defs[0]
                else: 
                    break
            if (it.typ == RftItemTyp.TEXT): 
                if (it.text is None and it.codes is not None and len(it.codes) > 0): 
                    if (len(it.codes) > 5): 
                        pass
                    cur = (curs[0] if len(curs) > 0 else None)
                    if (cur is not None and cur.level > it.level): 
                        cur = (None)
                    def0_ = (defs[0] if len(defs) > 0 else None)
                    if (def0_ is not None and def0_.level > it.level): 
                        def0_ = (None)
                    enc = (None if cur is None else cur.encoding)
                    if (font_name is not None and font_name in font_encodings): 
                        enc = font_encodings[font_name]
                    if (enc is None and def0_ is not None): 
                        enc = def0_.encoding
                    if (enc is None): 
                        enc = EncodingWrapper(EncodingStandard.CP1252)
                    try: 
                        str0_ = enc.get_string(it.codes, 0, -1)
                        it.text = str0_
                    except Exception as ex235: 
                        pass
                elif (i > 0 and items[i - 1].typ == RftItemTyp.COMMAND and items[i - 1].text[0] == 'f'): 
                    if (it.text is not None and it.text.endswith(" Cyr;") and font_name is not None): 
                        if (not font_name in font_encodings): 
                            font_encodings[font_name] = EncodingWrapper(EncodingStandard.CP1251)
                continue
            if (it.typ != RftItemTyp.COMMAND): 
                continue
            cmd = it.text
            if (cmd is None): 
                continue
            if (cmd == "plain"): 
                if (len(curs) > 0): 
                    del curs[0]
                continue
            if (cmd == "ansi"): 
                is_ansi = True
                continue
            if (cmd.startswith("ansicpg")): 
                cp = 0
                wrapcp237 = RefOutArgWrapper(0)
                inoutres238 = Utils.tryParseInt(cmd[7:], wrapcp237)
                cp = wrapcp237.value
                if (not inoutres238): 
                    continue
                defs.insert(0, RtfHelper.RtfEncoder._new236(it.level, EncodingWrapper(EncodingStandard.UNDEFINED, None, cp)))
                continue
            if (cmd.startswith("deflangfe")): 
                cp = 0
                wrapcp242 = RefOutArgWrapper(0)
                inoutres243 = Utils.tryParseInt(cmd[9:], wrapcp242)
                cp = wrapcp242.value
                if (not inoutres243): 
                    continue
                wrapcp240 = RefOutArgWrapper(0)
                inoutres241 = Utils.tryGetValue(RtfHelper.M_LANG_ID_TO_CODEPAGE, cp, wrapcp240)
                cp = wrapcp240.value
                if (not inoutres241): 
                    continue
                defs.insert(0, RtfHelper.RtfEncoder._new236(it.level, EncodingWrapper(EncodingStandard.UNDEFINED, None, cp)))
                continue
            if (cmd.startswith("deflang")): 
                cp = 0
                wrapcp247 = RefOutArgWrapper(0)
                inoutres248 = Utils.tryParseInt(cmd[7:], wrapcp247)
                cp = wrapcp247.value
                if (not inoutres248): 
                    continue
                wrapcp245 = RefOutArgWrapper(0)
                inoutres246 = Utils.tryGetValue(RtfHelper.M_LANG_ID_TO_CODEPAGE, cp, wrapcp245)
                cp = wrapcp245.value
                if (not inoutres246): 
                    continue
                defs.insert(0, RtfHelper.RtfEncoder._new236(it.level, EncodingWrapper(EncodingStandard.UNDEFINED, None, cp)))
                continue
            if (cmd.startswith("langfe")): 
                continue
            if (cmd.startswith("lang")): 
                cp = 0
                wrapcp252 = RefOutArgWrapper(0)
                inoutres253 = Utils.tryParseInt(cmd[4:], wrapcp252)
                cp = wrapcp252.value
                if (not inoutres253): 
                    continue
                wrapcp250 = RefOutArgWrapper(0)
                inoutres251 = Utils.tryGetValue(RtfHelper.M_LANG_ID_TO_CODEPAGE, cp, wrapcp250)
                cp = wrapcp250.value
                if (not inoutres251): 
                    continue
                if ((i > 0 and items[i - 1].typ == RftItemTyp.COMMAND and items[i - 1].text.startswith("f")) and len(curs) > 0 and curs[0].level == it.level): 
                    continue
                curs.insert(0, RtfHelper.RtfEncoder._new236(it.level, EncodingWrapper(EncodingStandard.UNDEFINED, None, cp)))
                continue
            if (len(cmd) >= 2 and cmd[0] == 'f' and str.isdigit(cmd[1])): 
                if (cmd == "f674"): 
                    pass
                if (cmd in font_charsets): 
                    cs = font_charsets[cmd]
                    enc = None
                    swichVal = cs
                    if (swichVal == 204): 
                        enc = EncodingWrapper(EncodingStandard.CP1251)
                    elif (swichVal == 238): 
                        enc = EncodingWrapper(EncodingStandard.UNDEFINED, None, 1250)
                    elif (swichVal == 161): 
                        enc = EncodingWrapper(EncodingStandard.UNDEFINED, None, 1253)
                    elif (swichVal == 162): 
                        enc = EncodingWrapper(EncodingStandard.UNDEFINED, None, 1254)
                    if (enc is not None): 
                        curs.insert(0, RtfHelper.RtfEncoder._new236(it.level, enc))
                else: 
                    font_name = cmd
                continue
            if (cmd.startswith("fcharset") and font_name is not None): 
                cod = 0
                wrapcod255 = RefOutArgWrapper(0)
                inoutres256 = Utils.tryParseInt(cmd[8:], wrapcod255)
                cod = wrapcod255.value
                if (inoutres256): 
                    if (not font_name in font_charsets): 
                        font_charsets[font_name] = cod
                continue
        tmp = io.StringIO()
        i = 0
        while i < (len(items) - 1): 
            it = items[i]
            it1 = items[i + 1]
            if ((it1.typ == RftItemTyp.TEXT and it.typ == RftItemTyp.TEXT and it1.text is not None) and it.text is not None): 
                Utils.setLengthStringIO(tmp, 0)
                print(it.text, end="", file=tmp)
                j = i + 1
                while j < len(items): 
                    it1 = items[j]
                    if (it1.typ != RftItemTyp.TEXT or it1.text is None): 
                        break
                    print(it1.text, end="", file=tmp)
                    items[j] = (None)
                    i = j
                    j += 1
                it.text = Utils.toStringStringIO(tmp)
            i += 1
        k = 0
        i = 0
        while i < len(items): 
            if (items[i] is not None): 
                items[k] = items[i]
                k += 1
            i += 1
        if (k < len(items)): 
            del items[k:k+len(items) - k]
    
    @staticmethod
    def _create_uni_doc(stream : Stream, pars : 'CreateDocumentParam') -> 'UnitextDocument':
        doc = UnitextDocument._new41(FileFormat.RTF)
        stream.position = 0
        items = RtfItem.parse_list(stream)
        RtfHelper.__manage_encodings(items)
        cnt_gen = UnitextGen()
        head_gen = None
        foot_gen = None
        html_ = None
        i = 0
        if (len(items) > 100 and items[1].typ == RftItemTyp.COMMAND and items[1].text == "rtf1"): 
            ii = 2
            while ii < 20: 
                if (items[ii].typ == RftItemTyp.COMMAND and items[ii].text == "fromhtml1"): 
                    html_ = io.StringIO()
                    cnt_gen = (None)
                    while (ii < 500) and ((ii + 1) < len(items)): 
                        if ((items[ii].typ == RftItemTyp.COMMAND and items[ii].text == "*" and items[ii + 1].typ == RftItemTyp.COMMAND) and items[ii + 1].text.startswith("htmltag")): 
                            i = ii
                            break
                        ii += 1
                    break
                ii += 1
        first_pass650 = True
        while True:
            if first_pass650: first_pass650 = False
            else: i += 1
            if (not (i < len(items))): break
            it = items[i]
            if (it.typ == RftItemTyp.COMMAND): 
                cmd = it.text
                if (cmd is None): 
                    continue
                if (cmd.startswith("header") or cmd.startswith("footer")): 
                    if (not cmd.startswith("headery") and not cmd.startswith("footery")): 
                        ii = 0
                        ii = (i + 1)
                        while ii < len(items): 
                            if (items[ii].level < it.level): 
                                break
                            ii += 1
                        if (head_gen is None and cmd.startswith("head")): 
                            head_gen = UnitextGen()
                            RtfHelper.__manage_uni(items, html_, head_gen, i + 1, ii, False, 0)
                        elif (foot_gen is None and cmd.startswith("foot")): 
                            foot_gen = UnitextGen()
                            RtfHelper.__manage_uni(items, html_, foot_gen, i + 1, ii, False, 0)
                        i = (ii - 1)
                        continue
            if (isinstance(items[i], RtfHelper.RtfTablerow)): 
                pass
            j = RtfHelper.__manage_uni(items, html_, cnt_gen, i, i + 1, False, 0)
            i = (j - 1)
        if (html_ is None): 
            doc.content = cnt_gen.finish(True, None)
            sect = UnitextPagesection()
            if (head_gen is not None): 
                fi = head_gen.finish(True, None)
                if (fi is not None): 
                    sect.items.append(UnitextPagesectionItem._new42(fi))
            if (foot_gen is not None): 
                fi = foot_gen.finish(True, None)
                if (fi is not None): 
                    sect.items.append(UnitextPagesectionItem._new259(fi, True))
            if (len(sect.items) > 0): 
                doc.sections.append(sect)
        else: 
            txt = Utils.toStringStringIO(html_)
            nod = HtmlParser.parse(html_, False)
            if (nod is None): 
                return None
            doc = HtmlHelper.create(nod, None, None, pars)
            doc.source_format = FileFormat.RTF
        doc.optimize(False, None)
        return doc
    
    @staticmethod
    def __manage_uni(items : typing.List['RtfItem'], html_ : io.StringIO, gen : 'UnitextGen', i0 : int, i1 : int, in_tab : bool, lev : int) -> int:
        i = 0
        i = i0
        first_pass651 = True
        while True:
            if first_pass651: first_pass651 = False
            else: i += 1
            if (not (i < i1)): break
            it = items[i]
            if (it.typ == RftItemTyp.BRACKETOPEN or it.typ == RftItemTyp.BRACKETCLOSE): 
                continue
            if (it.typ == RftItemTyp.PROXY): 
                gen.append(it.uni, None, -1, False)
                continue
            if (it.typ == RftItemTyp.TEXT): 
                if (it.text is not None): 
                    if (html_ is not None): 
                        MiscHelper.correct_html_value(html_, it.text, False, False)
                    else: 
                        gen.append_text(it.text, False)
                continue
            if (isinstance(it, RtfItemImage)): 
                im = Utils.asObjectOrNull(it, RtfItemImage)
                img = UnitextImage._new260(im.codes)
                if (im.width > 0 and im.height > 0): 
                    img.width = "{0}pt".format(im.width)
                    img.height = "{0}pt".format(im.height)
                gen.append(img, None, -1, False)
                continue
            if (it.typ != RftItemTyp.COMMAND): 
                continue
            cmd = it.text
            if (cmd is None): 
                continue
            if ((cmd == "*" or cmd.startswith("fonttbl") or cmd == "stylesheet") or cmd.startswith("nonshppict") or cmd == "deleted"): 
                html_out_lev = -1
                last_out_ind = -1
                i += 1
                while i < len(items): 
                    if (items[i].level < it.level): 
                        i -= 1
                        break
                    elif (isinstance(items[i], RtfItemImage)): 
                        if (cmd == "*"): 
                            im = Utils.asObjectOrNull(items[i], RtfItemImage)
                            img = UnitextImage._new260(items[i].codes)
                            if (im.width > 0 and im.height > 0): 
                                img.width = "{0}pt".format(im.width)
                                img.height = "{0}pt".format(im.height)
                            gen.append(img, None, -1, False)
                    elif (items[i].typ == RftItemTyp.COMMAND): 
                        if (items[i].text == "footnote"): 
                            i -= 1
                            break
                        if (items[i].text == "annotation"): 
                            i -= 1
                            break
                        if (items[i].text == "shptxt"): 
                            i -= 1
                            break
                        if (items[i].text == "fldinst"): 
                            i -= 1
                            break
                        if (html_ is not None and items[i].text.startswith("htmltag")): 
                            html_out_lev = items[i].level
                    elif (items[i].typ == RftItemTyp.TEXT and html_ is not None): 
                        print(items[i].text, end="", file=html_)
                        last_out_ind = i
                    i += 1
                continue
            if (cmd == "fldinst"): 
                iii = list()
                ii = 0
                ii = (i + 1)
                while (ii < len(items)) and (ii < i1): 
                    if (items[ii].level < it.level): 
                        break
                    else: 
                        iii.append(items[ii])
                        if (items[ii].text is not None and items[ii].text.startswith("SYMBOL")): 
                            sss = items[ii].text[6:].strip()
                            jj = sss.find(' ')
                            if (jj > 0): 
                                sss = sss[0:0+jj]
                            wrapjj262 = RefOutArgWrapper(0)
                            inoutres263 = Utils.tryParseInt(sss, wrapjj262)
                            jj = wrapjj262.value
                            if (inoutres263): 
                                chu = chr(0)
                                if ("Wingdings" in items[ii].text): 
                                    chu = WingdingsHelper.get_unicode(jj)
                                else: 
                                    chu = SymbolHelper.get_unicode(jj)
                                if (chu == (chr(0))): 
                                    chu = '?'
                                gen.append_text("{0}".format(chu), False)
                    ii += 1
                i = (ii - 1)
                continue
            if (cmd == "field"): 
                iii = list()
                ii = 0
                ur = None
                ii = (i + 1)
                while ii < len(items): 
                    if (items[ii].level < it.level): 
                        break
                    else: 
                        iii.append(items[ii])
                        if (items[ii].typ == RftItemTyp.TEXT and items[ii].text is not None and items[ii].text.strip().startswith("HYPERLINK")): 
                            fff = items[ii].text
                            jj0 = fff.find('"')
                            jj1 = fff.rfind('"')
                            if (jj0 > 0 and jj1 > jj0): 
                                hy = fff[jj0 + 1:jj0 + 1+jj1 - jj0 - 1]
                                ur = hy
                            else: 
                                fff = fff[10:].strip()
                                if (fff.startswith("http")): 
                                    ur = fff
                                else: 
                                    pass
                            if (ur is None): 
                                pass
                    ii += 1
                gg = UnitextGen()
                RtfHelper.__manage_uni(iii, None, gg, 0, len(iii), False, lev + 1)
                cnt = gg.finish(True, None)
                if (cnt is not None): 
                    tmp = io.StringIO()
                    cnt.get_plaintext(tmp, GetPlaintextParam())
                    if (ur is None or tmp.tell() > 300): 
                        gen.append(cnt, None, -1, False)
                    else: 
                        hr = UnitextHyperlink._new53(ur)
                        hr.content = cnt
                        if (gen is not None): 
                            gen.append(hr, None, -1, False)
                        elif (html_ is not None): 
                            cnt.get_plaintext(html_, None)
                    i = (ii - 1)
                continue
            if (cmd == "annotation"): 
                iii = list()
                ii = 0
                ii = i
                while (ii < len(items)) and (ii < i1): 
                    if (items[ii].level < (it.level - 1)): 
                        break
                    else: 
                        iii.append(items[ii])
                    ii += 1
                gg = UnitextGen()
                RtfHelper.__manage_uni(items, html_, gg, i + 1, ii, False, lev)
                cnt = gg.finish(False, None)
                if (cnt is not None): 
                    tmp = io.StringIO()
                    cnt.get_plaintext(tmp, None)
                    if (tmp.tell() > 0): 
                        gen.append(UnitextComment._new44(Utils.toStringStringIO(tmp)), None, -1, False)
                i = (ii - 1)
                continue
            if (cmd == "shptxt"): 
                iii = list()
                ii = 0
                ii = i
                while (ii < len(items)) and (ii < i1): 
                    if (items[ii].level < (it.level - 1)): 
                        break
                    else: 
                        iii.append(items[ii])
                    ii += 1
                gg = UnitextGen()
                RtfHelper.__manage_uni(items, html_, gg, i + 1, ii, False, lev)
                cnt = gg.finish(True, None)
                if (isinstance(cnt, UnitextContainer)): 
                    cnt.typ = UnitextContainerType.SHAPE
                elif (cnt is not None): 
                    cnt2 = UnitextContainer._new92(UnitextContainerType.SHAPE)
                    cnt2.children.append(cnt)
                    cnt = cnt2.optimize(False, None)
                if (cnt is not None): 
                    gen.append(cnt, None, -1, False)
                i = (ii - 1)
                continue
            if (cmd == "footnote"): 
                iii = list()
                ii = 0
                endnote = False
                ii = i
                while (ii < len(items)) and (ii < i1): 
                    if (items[ii].level <= (it.level - 1)): 
                        break
                    else: 
                        iii.append(items[ii])
                        if (items[ii].typ == RftItemTyp.COMMAND and items[ii].text == "ftnalt"): 
                            endnote = True
                    ii += 1
                gg = UnitextGen()
                RtfHelper.__manage_uni(items, html_, gg, i + 1, ii, False, lev)
                cnt = gg.finish(False, None)
                if (cnt is not None): 
                    fn = UnitextFootnote._new267(cnt, endnote)
                    if (isinstance(cnt, UnitextContainer)): 
                        cc = Utils.asObjectOrNull(cnt, UnitextContainer)
                        if (len(cc.children) > 1 and (isinstance(cc.children[0], UnitextPlaintext)) and cc.children[0].typ == UnitextPlaintextType.SUP): 
                            fn.custom_mark = cc.children[0].text
                            del cc.children[0]
                            fn.content = cc.optimize(True, None)
                    gen.append(fn, None, -1, False)
                i = (ii - 1)
                continue
            if (cmd.startswith("listtext")): 
                list_id = None
                list_level = 0
                ii = 0
                ok = False
                end_of_num = False
                num = io.StringIO()
                tmp = list()
                ii = (i + 1)
                first_pass652 = True
                while True:
                    if first_pass652: first_pass652 = False
                    else: ii += 1
                    if (not (ii < len(items))): break
                    itt = items[ii]
                    tmp.append(itt)
                    if (itt.typ == RftItemTyp.TEXT): 
                        if (list_id is not None or end_of_num): 
                            ok = True
                            break
                        print(Utils.ifNotNull(itt.text, ""), end="", file=num)
                        continue
                    if (itt.typ == RftItemTyp.BRACKETCLOSE and num.tell() > 0): 
                        end_of_num = True
                    if (itt.typ != RftItemTyp.COMMAND): 
                        continue
                    if (in_tab): 
                        if ((itt.text == "cell" or itt.text == "row" or itt.text == "trowd") or itt.text == "intbl" or itt.text == "nestcell"): 
                            break
                    if (itt.text.startswith("ls") and len(itt.text) > 2 and str.isdigit(itt.text[2])): 
                        if (list_id is not None): 
                            break
                        list_id = itt.text[2:]
                        continue
                    if (itt.text.startswith("ilvl") and len(itt.text) > 4 and str.isdigit(itt.text[4])): 
                        wraplist_level268 = RefOutArgWrapper(0)
                        Utils.tryParseInt(itt.text[4:], wraplist_level268)
                        list_level = wraplist_level268.value
                        continue
                    if (itt.text == "listtext"): 
                        break
                if (ok): 
                    jj = 0
                    jj = (ii + 1)
                    first_pass653 = True
                    while True:
                        if first_pass653: first_pass653 = False
                        else: jj += 1
                        if (not (jj < len(items))): break
                        itt = items[jj]
                        tmp.append(itt)
                        if (itt.typ != RftItemTyp.COMMAND): 
                            continue
                        if (itt.text == "par"): 
                            jj += 1
                            break
                        if (itt.text == "sect"): 
                            break
                        if (itt.text == "listtext" or itt.text == "trowd"): 
                            break
                        if (itt.text.startswith("ls")): 
                            break
                    if ((ii > 2 and items[ii - 1].typ == RftItemTyp.COMMAND and items[ii - 2].typ == RftItemTyp.COMMAND) and items[ii - 2].text == "*"): 
                        ii -= 2
                    gg = UnitextGen()
                    RtfHelper.__manage_uni(items, html_, gg, ii, jj, False, lev)
                    gen.append_list_item(gg.finish(True, None), Utils.toStringStringIO(num).strip(), list_id, list_level, None)
                    i = (jj - 1)
                    continue
            if (cmd == "line"): 
                if (html_ is not None): 
                    print("\r\n", end="", file=html_)
                else: 
                    gen.append_newline(False)
                continue
            if (cmd == "page" or cmd == "sect"): 
                gen.append_pagebreak()
                continue
            if (cmd == "par"): 
                if (html_ is not None): 
                    print("\r\n", end="", file=html_)
                else: 
                    gen.append_newline(False)
                continue
            if (cmd == "brdrt" or cmd == "brdrb"): 
                if (html_ is not None): 
                    print("\r\n<hr/>", end="", file=html_)
                else: 
                    gen.append(UnitextMisc._new269(UnitextMiscType.HORIZONTALLINE), None, -1, False)
                continue
            if (cmd == "intbl" and not in_tab): 
                pass
            if (((cmd == "trowd" and not in_tab)) or ((cmd == "intbl" and not in_tab))): 
                if (lev < 5): 
                    if (lev > 10): 
                        pass
                    rtf_tab = RichTextTable()
                    rtf_row = RichTextRow()
                    ii = RtfHelper.__manage_table_row(items, i, rtf_row, lev + 1)
                    if (ii > i): 
                        rtf_tab.add_child(rtf_row)
                        i = ii
                        while i < len(items):
                            if (rtf_row._last_row): 
                                break
                            rtf_row = RichTextRow()
                            ii = RtfHelper.__manage_table_row(items, i, rtf_row, lev + 1)
                            if (ii < 0): 
                                break
                            rtf_tab.add_child(rtf_row)
                            if (ii <= i): 
                                break
                            i = ii
                        rtf_tab._correct()
                        tab = RtfHelper.__create_table(rtf_tab)
                        if (gen is not None): 
                            gen.append(tab, None, -1, False)
                        continue
            sub = -1
            if (cmd.startswith("super") or cmd.startswith("up")): 
                sub = 0
            elif (cmd.startswith("sub")): 
                sub = 1
            if (sub >= 0): 
                ii = 0
                ok = False
                tmp = io.StringIO()
                ii = (i + 1)
                while ii < len(items): 
                    if (items[ii].typ == RftItemTyp.BRACKETCLOSE or items[ii].typ == RftItemTyp.BRACKETOPEN): 
                        ok = True
                        break
                    elif (items[ii].typ == RftItemTyp.TEXT): 
                        print(Utils.ifNotNull(items[ii].text, ""), end="", file=tmp)
                    elif (items[ii].typ != RftItemTyp.COMMAND): 
                        break
                    elif (items[ii].text == "pard"): 
                        ok = True
                        break
                    elif (items[ii].text == "footnote"): 
                        break
                    ii += 1
                if (ok): 
                    tt = Utils.toStringStringIO(tmp).strip()
                    if (len(tt) > 0 and (len(tt) < 10)): 
                        gen.append(UnitextPlaintext._new52(tt, (UnitextPlaintextType.SUB if sub > 0 else UnitextPlaintextType.SUP)), None, -1, False)
                        i = (ii - 1)
                continue
        return i
    
    @staticmethod
    def __create_table(tbl : 'RichTextTable') -> 'UnitextTable':
        res = UnitextTable()
        rn = 0
        for rr in tbl.children: 
            cn = 0
            for c in rr.children: 
                while True: 
                    if (res.get_cell(rn, cn) is None): 
                        break
                    cn += 1
                cel = res.add_cell(rn, (rn + c.rows_span) - 1, cn, (cn + c.cols_span) - 1, Utils.asObjectOrNull(c.tag, UnitextItem))
                if (cel is not None): 
                    c._res_col_index = cel.col_begin
            rn += 1
        if (res.cols_count > 1): 
            wi = Utils.newArray(res.cols_count, 0)
            for kk in range(3):
                for rr in tbl.children: 
                    r = Utils.asObjectOrNull(rr, RichTextRow)
                    if (r is None): 
                        continue
                    if (len(r._cells_info) != len(r.children)): 
                        continue
                    sum0_ = 0
                    for ci in r._cells_info: 
                        sum0_ += ci.width
                    if (sum0_ <= 0): 
                        continue
                    i = 0
                    first_pass654 = True
                    while True:
                        if first_pass654: first_pass654 = False
                        else: i += 1
                        if (not (i < len(r.children))): break
                        c = Utils.asObjectOrNull(r.children[i], RichTextCell)
                        if ((c._res_col_index < 0) or c._res_col_index >= len(wi)): 
                            continue
                        w = math.floor((r._cells_info[i].width * 100) / sum0_)
                        co = 0
                        j = c._res_col_index
                        while (j < (c._res_col_index + c.cols_span)) and (j < len(wi)): 
                            if (wi[j] > 0): 
                                w -= wi[j]
                            else: 
                                co += 1
                            j += 1
                        if (co == 1 and w > 0): 
                            j = c._res_col_index
                            while (j < (c._res_col_index + c.cols_span)) and (j < len(wi)): 
                                if (wi[j] == 0): 
                                    wi[j] = w
                                    break
                                j += 1
            i = 0
            while i < len(wi): 
                if (wi[i] > 0): 
                    res.set_col_width(i, "{0}%".format(wi[i]))
                i += 1
        return res
    
    @staticmethod
    def __manage_table_row(items : typing.List['RtfItem'], i : int, rtf_row : 'RichTextRow', lev : int) -> int:
        ok = False
        while i < len(items): 
            it = items[i]
            if (it.typ == RftItemTyp.COMMAND and ((it.text == "trowd" or it.text == "intbl"))): 
                ok = True
                break
            if (it.typ == RftItemTyp.TEXT or it.typ == RftItemTyp.IMAGE): 
                break
            i += 1
        if (not ok): 
            return -1
        col_width = list()
        while i < len(items): 
            it = items[i]
            if (it.typ == RftItemTyp.COMMAND and it.text == "row"): 
                return i + 1
            j = 0
            ok = False
            j = i
            first_pass655 = True
            while True:
                if first_pass655: first_pass655 = False
                else: j += 1
                if (not (j < len(items))): break
                itt = items[j]
                if (itt.typ != RftItemTyp.COMMAND): 
                    continue
                if (itt.text == "cell"): 
                    ok = True
                    break
                if (itt.text == "row"): 
                    j -= 1
                    break
                if (itt.text == "nestcell"): 
                    nrow = RichTextRow()
                    jj = RtfHelper.__manage_nested_table_row(items, i, nrow, lev + 1)
                    if (jj > 0): 
                        ntab = RichTextTable()
                        ntab.add_child(nrow)
                        while True:
                            nrow = RichTextRow()
                            jjj = RtfHelper.__manage_nested_table_row(items, jj, nrow, lev + 1)
                            if (jjj < 0): 
                                break
                            ntab.add_child(nrow)
                            jj = jjj
                        ntab._correct()
                        ppp = RtfHelper.RtfItemProxy._new271(RftItemTyp.PROXY)
                        ppp.uni = (RtfHelper.__create_table(ntab))
                        del items[i + 1:i + 1+jj - i - 1]
                        items[i] = (ppp)
                        continue
                if (rtf_row is not None): 
                    rtf_row._add_cmd(itt.text)
            if (ok and rtf_row is not None): 
                gg = UnitextGen()
                RtfHelper.__manage_uni(items, None, gg, i, j, True, lev)
                cel = RichTextCell()
                cel.tag = (gg.finish(True, None))
                cel._end_of = True
                rtf_row.add_child(cel)
            i = j
            i += 1
        return -1
    
    @staticmethod
    def __manage_nested_table_row(items : typing.List['RtfItem'], i : int, rtf_row : 'RichTextRow', lev : int) -> int:
        end_of_row = False
        while i < len(items): 
            it = items[i]
            if (it.typ == RftItemTyp.COMMAND and ((it.text == "row" or it.text == "cell"))): 
                return -1
            j = 0
            ok = False
            j = i
            first_pass656 = True
            while True:
                if first_pass656: first_pass656 = False
                else: j += 1
                if (not (j < len(items))): break
                itt = items[j]
                if (itt.typ != RftItemTyp.COMMAND): 
                    continue
                if (itt.text == "nestcell"): 
                    ok = True
                    break
                if (itt.text == "row" or itt.text == "cell"): 
                    return -1
                if (itt.text == "nesttableprops" or itt.text == "nestrow"): 
                    end_of_row = True
                    break
            if (ok): 
                gg = UnitextGen()
                RtfHelper.__manage_uni(items, None, gg, i, j, True, lev + 1)
                cel = RichTextCell()
                cel.tag = (gg.finish(True, None))
                cel._end_of = True
                rtf_row.add_child(cel)
            i = j
            if (end_of_row): 
                break
            i += 1
        if (not end_of_row): 
            return -1
        first_pass657 = True
        while True:
            if first_pass657: first_pass657 = False
            else: i += 1
            if (not (i < len(items))): break
            it = items[i]
            if (it.typ != RftItemTyp.COMMAND): 
                continue
            if (it.text == "row" or it.text == "cell"): 
                return -1
            if (it.text == "nestrow"): 
                return i + 1
            rtf_row._add_cmd(it.text)
        return -1
    
    # static constructor for class RtfHelper
    @staticmethod
    def _static_ctor():
        RtfHelper.M_LANG_ID_TO_CODEPAGE = dict()
        for i in [1052, 1050, 1029, 1038, 1045, 1048, 2074, 1051, 1060]: 
            RtfHelper.M_LANG_ID_TO_CODEPAGE[i] = 1250
        for i in [2092, 1059, 1026, 1071, 1087, 1088, 1104, 1049, 3098, 1092, 1058, 2115]: 
            RtfHelper.M_LANG_ID_TO_CODEPAGE[i] = 1251
        for i in [1078, 1069, 1027, 1030, 2067, 1043, 3081, 10249, 4105, 9225, 2057, 6153, 8201, 5129, 13321, 7177, 11273, 1033, 12297, 1080, 1035, 2060, 3084, 1036, 5132, 6156, 4108, 1110, 3079, 1031, 5127, 4103, 2055, 1039, 1057, 1040, 2064, 2110, 1086, 1044, 2068, 1046, 2070, 11274, 16394, 13322, 9226, 5130, 7178, 12298, 17418, 4106, 18442, 2058, 19466, 6154, 15370, 10250, 20490, 1034, 14346, 8202, 1089, 2077, 1053]: 
            RtfHelper.M_LANG_ID_TO_CODEPAGE[i] = 1252
        RtfHelper.M_LANG_ID_TO_CODEPAGE[1032] = 1253
        for i in [1068, 1055, 1091]: 
            RtfHelper.M_LANG_ID_TO_CODEPAGE[i] = 1254
        RtfHelper.M_LANG_ID_TO_CODEPAGE[1037] = 1255
        for i in [5121, 15361, 3073, 2049, 11265, 13313, 12289, 4097, 6145, 8193, 16385, 1025, 10241, 7169, 14337, 9217, 1065, 1056]: 
            RtfHelper.M_LANG_ID_TO_CODEPAGE[i] = 1256
        for i in [1061, 1062, 1063, 1066]: 
            RtfHelper.M_LANG_ID_TO_CODEPAGE[i] = 1257

RtfHelper._static_ctor()