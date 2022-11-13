# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.internal.html.HtmlTag import HtmlTag
from pullenti.unitext.internal.html.HtmlNode import HtmlNode
from pullenti.unitext.internal.html.HtmlParserNode import HtmlParserNode

class HtmlParser:
    # Парсинг Html-текста
    
    @staticmethod
    def parse(shtml : io.StringIO, preserve_whitespaces : bool=False) -> 'HtmlNode':
        i = 0
        j = 0
        k = 0
        par = None
        nod = None
        tmp_html = Utils.toStringStringIO(shtml)
        Utils.setLengthStringIO(shtml, 0)
        i = 0
        while i < len(tmp_html): 
            if (not Utils.isWhitespace(tmp_html[i])): 
                break
            i += 1
        new_line = "\r"
        while i < len(tmp_html): 
            ch = tmp_html[i]
            if (ch == '\t'): 
                print("    ", end="", file=shtml)
            elif (ch != '\r' and ch != '\n'): 
                print(ch, end="", file=shtml)
            elif (ch == '\n'): 
                print(new_line, end="", file=shtml)
            elif (ch == '\r'): 
                if (((i + 1) < len(tmp_html)) and tmp_html[i + 1] == '\n'): 
                    i += 1
                print(new_line, end="", file=shtml)
            i += 1
        html_ = Utils.toStringStringIO(shtml)
        items = list()
        pn = HtmlParserNode()
        preserve = 0
        i = 0
        first_pass616 = True
        while True:
            if first_pass616: first_pass616 = False
            else: i += 1
            if (not (i < len(html_))): break
            tag = None
            for j in range(len(items) - 1, -1, -1):
                if (items[j].tag_name is not None): 
                    if (items[j].tag_name == "SCRIPT" and items[j].tag_type == HtmlParserNode.TagTypes.OPEN): 
                        tag = "SCRIPT"
                    break
            else: j = -1
            if (len(items) == 47): 
                pass
            if (not pn.analize(html_, i, tag, preserve > 0 or preserve_whitespaces)): 
                break
            i = pn.index_to
            if (pn.tag_name == "PRE"): 
                if (pn.tag_type == HtmlParserNode.TagTypes.OPEN): 
                    preserve += 1
                elif (pn.tag_type == HtmlParserNode.TagTypes.CLOSE): 
                    preserve -= 1
            if (pn.tag_name == "META"): 
                val = None
                wrapval20 = RefOutArgWrapper(None)
                inoutres21 = Utils.tryGetValue(pn.attributes, "CONTENT", wrapval20)
                val = wrapval20.value
                if (pn.attributes is not None and inoutres21): 
                    if (val == "Word.Document"): 
                        preserve = 1
                    elif ("Microsoft Word" in val): 
                        preserve = 1
            pn.whitespace_preserve = (preserve > 0 or preserve_whitespaces)
            if (pn.is_empty): 
                continue
            items.append(pn)
            if (pn.tag_name is not None): 
                pn.tag = HtmlTag.find_tag(pn.tag_name)
            pn.close_tag_index = -1
            pn = HtmlParserNode()
        stack = list()
        error = False
        i = 0
        first_pass617 = True
        while True:
            if first_pass617: first_pass617 = False
            else: i += 1
            if (not (i < len(items))): break
            pn = items[i]
            if (pn.tag is None): 
                continue
            if (pn.tag_type == HtmlParserNode.TagTypes.CLOSE): 
                if (not pn.tag.endtag_required or len(stack) == 0): 
                    continue
                pp = stack[len(stack) - 1]
                if (pp.tag == pn.tag): 
                    del stack[len(stack) - 1]
                    pp.close_tag_index = i
                    continue
                for j in range(len(stack) - 1, -1, -1):
                    if (stack[j].tag == pn.tag): 
                        break
                else: j = -1
                if (j < 0): 
                    continue
                stack[j].close_tag_index = i
                del stack[j:j+len(stack) - j]
                continue
            if (pn.tag_type == HtmlParserNode.TagTypes.OPENCLOSE): 
                pn.close_tag_index = i
                continue
            if (pn.tag_type != HtmlParserNode.TagTypes.OPEN): 
                continue
            if (pn.tag.is_empty): 
                pn.close_tag_index = i
                continue
            if (pn.tag.endtag_required): 
                stack.append(pn)
        if (len(stack) > 0): 
            error = True
        if (error): 
            pass
        i = 0
        first_pass618 = True
        while True:
            if first_pass618: first_pass618 = False
            else: i += 1
            if (not (i < len(items))): break
            pn = items[i]
            if (pn.tag_name == "BR"): 
                pass
            if (pn.close_tag_index >= 0 or pn.tag_name is None or pn.tag_type != HtmlParserNode.TagTypes.OPEN): 
                continue
            maxi = -1
            for j in range(i - 1, -1, -1):
                if (items[j].close_tag_index > i): 
                    maxi = items[j].close_tag_index
                    break
            else: j = -1
            if (maxi < 0): 
                maxi = (len(items) - 1)
            first_item_with_same_tag = -1
            k = 1
            j = (i + 1)
            while j <= maxi: 
                if (items[j].close_tag_index >= j): 
                    j = items[j].close_tag_index
                elif (items[j].tag_name == pn.tag_name): 
                    if (items[j].tag_type != HtmlParserNode.TagTypes.CLOSE and (first_item_with_same_tag < 0)): 
                        first_item_with_same_tag = j
                    if (items[j].tag_type == HtmlParserNode.TagTypes.OPEN): 
                        k += 1
                    elif (items[j].tag_type == HtmlParserNode.TagTypes.CLOSE): 
                        k -= 1
                        if (k == 0): 
                            pn.close_tag_index = j
                            break
                j += 1
            if (pn.close_tag_index >= 0): 
                continue
            if (pn.tag_name == "HTML"): 
                pn.close_tag_index = (len(items) - 1)
                continue
            if (first_item_with_same_tag >= 0): 
                pn.close_tag_index = (first_item_with_same_tag - 1)
            else: 
                if (items[maxi].tag_name is not None): 
                    pn.close_tag_index = (maxi - 1)
                else: 
                    pn.close_tag_index = maxi
                if (pn.tag_name == "HEAD"): 
                    j = (i + 1)
                    while j < len(items): 
                        if (items[j].tag_name == "BODY"): 
                            pn.close_tag_index = (j - 1)
                            break
                        j += 1
                elif (pn.tag_name == "P"): 
                    j = (i + 1)
                    while j < len(items): 
                        if (items[j].tag is not None and not items[j].tag.is_inline): 
                            pn.close_tag_index = (j - 1)
                            break
                        j += 1
        res_list = list()
        i = 0
        while i < len(items): 
            items[i]._printed = False
            i += 1
        i = 0
        first_pass619 = True
        while True:
            if first_pass619: first_pass619 = False
            else: i += 1
            if (not (i < len(items))): break
            if (items[i]._printed): 
                continue
            wrapj22 = RefOutArgWrapper(0)
            nod = HtmlParser.__create_node(items, i, wrapj22)
            j = wrapj22.value
            if (j < 0): 
                break
            if (j < i): 
                pass
            if (nod is None): 
                i = j
                continue
            if (i == 0 and j == (len(items) - 1)): 
                nod._correct_rus_texts(0)
                return nod
            res_list.append(nod)
            i = j
        if (len(res_list) == 0): 
            return None
        for li in res_list: 
            li._correct_rus_texts(0)
        if (len(res_list) == 1): 
            return res_list[0]
        res = HtmlNode()
        res.tag_name = "HTML"
        res.source_html_position = 0
        res.source_html_length = len(html_)
        for ch in res_list: 
            res.children.append(ch)
            ch.parent = res
        return res
    
    @staticmethod
    def __create_node(list0_ : typing.List['HtmlParserNode'], ind_from : int, ind_to : int) -> 'HtmlNode':
        ind_to.value = ind_from
        if ((ind_from < 0) or ind_from >= len(list0_)): 
            return None
        pn = list0_[ind_from]
        if (pn.tag_type == HtmlParserNode.TagTypes.CLOSE): 
            pn._printed = True
            ind_to.value = ind_from
            return None
        if (pn._printed): 
            return None
        res = HtmlNode()
        res.source_html_position = pn.index_from
        res.source_html_end_position = pn.index_to
        res.whitespace_preserve = pn.whitespace_preserve
        if (pn.tag_name is None): 
            if (pn.pure_text is None): 
                return None
            res.text = pn.pure_text
            pn._printed = True
            return res
        res.tag_name = pn.tag_name
        res.attrs = pn.attributes
        res.text = pn.pure_text
        pn._printed = True
        if (res.tag_name == "SPAN"): 
            pass
        if (pn.close_tag_index <= ind_from): 
            return res
        ind_to.value = pn.close_tag_index
        cl = list0_[pn.close_tag_index]
        if (cl.tag_type == HtmlParserNode.TagTypes.CLOSE and cl.tag_name == pn.tag_name): 
            res.source_html_end_position = cl.index_to
            if ((ind_from + 2) == pn.close_tag_index and list0_[ind_from + 1].tag_name is None): 
                res.text = list0_[ind_from + 1].pure_text
                return res
        elif (pn.close_tag_index > ind_from): 
            res.source_html_end_position = list0_[pn.close_tag_index].index_to
            if ((ind_from + 1) == pn.close_tag_index and list0_[ind_from + 1].tag_name is None): 
                res.text = list0_[ind_from + 1].pure_text
                ind_to.value = (ind_from + 1)
                return res
        else: 
            pass
        i = ind_from + 1
        first_pass620 = True
        while True:
            if first_pass620: first_pass620 = False
            else: i += 1
            if (not (i <= pn.close_tag_index)): break
            if (list0_[i]._printed): 
                continue
            j = 0
            wrapj23 = RefOutArgWrapper(0)
            chi = HtmlParser.__create_node(list0_, i, wrapj23)
            j = wrapj23.value
            if (j < i): 
                break
            if (chi is not None): 
                if (chi.total_children > 100): 
                    pass
                res.children.append(chi)
                chi.parent = res
                if (chi.tag_name == "UL"): 
                    pass
            i = j
        return res
    
    __m_table_tags = None
    
    # static constructor for class HtmlParser
    @staticmethod
    def _static_ctor():
        HtmlParser.__m_table_tags = dict()
        HtmlParser.__m_table_tags["TABLE"] = 0
        HtmlParser.__m_table_tags["TBODY"] = 1
        HtmlParser.__m_table_tags["THEAD"] = 1
        HtmlParser.__m_table_tags["TFOOT"] = 1
        HtmlParser.__m_table_tags["TR"] = 2
        HtmlParser.__m_table_tags["TH"] = 3
        HtmlParser.__m_table_tags["TD"] = 3
        HtmlParser.__m_table_tags["UL"] = 0
        HtmlParser.__m_table_tags["OL"] = 0
        HtmlParser.__m_table_tags["DL"] = 0
        HtmlParser.__m_table_tags["LI"] = 1
        HtmlParser.__m_table_tags["DT"] = 1
        HtmlParser.__m_table_tags["DD"] = 1

HtmlParser._static_ctor()