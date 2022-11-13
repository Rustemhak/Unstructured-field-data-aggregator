# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextNewline import UnitextNewline
from pullenti.unitext.UnitextTablecell import UnitextTablecell
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextComment import UnitextComment
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextList import UnitextList
from pullenti.unitext.UnitextHyperlink import UnitextHyperlink
from pullenti.unitext.UnitextListitem import UnitextListitem
from pullenti.unitext.UnitextDocblock import UnitextDocblock
from pullenti.unitext.UnitextFootnote import UnitextFootnote
from pullenti.unitext.UnitextContainerType import UnitextContainerType
from pullenti.unitext.UnitextTable import UnitextTable

class UnitextImplantateHelper:
    
    @staticmethod
    def clear(content : 'UnitextItem', id0_ : str, type_name : str, cnt_typ : 'UnitextContainerType', own : 'UnitextContainer', cou : int) -> 'UnitextItem':
        tab = Utils.asObjectOrNull(content, UnitextTable)
        if (tab is not None): 
            r = 0
            while r < tab.rows_count: 
                c = 0
                while c < tab.cols_count: 
                    cel = tab.get_cell(r, c)
                    if (cel is not None and cel.content is not None): 
                        cel.content = UnitextImplantateHelper.clear(cel.content, id0_, type_name, cnt_typ, None, cou)
                    c += 1
                r += 1
            return tab
        li = Utils.asObjectOrNull(content, UnitextList)
        if (li is not None): 
            for l_ in li.items: 
                if (l_.prefix is not None): 
                    l_.prefix = UnitextImplantateHelper.clear(l_.prefix, id0_, type_name, cnt_typ, None, cou)
                if (l_.content is not None): 
                    l_.content = UnitextImplantateHelper.clear(l_.content, id0_, type_name, cnt_typ, None, cou)
                if (l_.sublist is not None): 
                    UnitextImplantateHelper.clear(l_.sublist, id0_, type_name, cnt_typ, None, cou)
            return li
        foot = Utils.asObjectOrNull(content, UnitextFootnote)
        if (foot is not None): 
            if (foot.content is not None): 
                foot.content = UnitextImplantateHelper.clear(foot.content, id0_, type_name, cnt_typ, None, cou)
            return foot
        hyp = Utils.asObjectOrNull(content, UnitextHyperlink)
        if (hyp is not None): 
            if (hyp.content is not None): 
                hyp.content = UnitextImplantateHelper.clear(hyp.content, id0_, type_name, cnt_typ, None, cou)
            return hyp
        dbl = Utils.asObjectOrNull(content, UnitextDocblock)
        if (dbl is not None): 
            if (dbl.head is not None): 
                dbl.head = (Utils.asObjectOrNull(UnitextImplantateHelper.clear(dbl.head, id0_, type_name, cnt_typ, None, cou), UnitextContainer))
            if (dbl.body is not None): 
                dbl.body = UnitextImplantateHelper.clear(dbl.body, id0_, type_name, cnt_typ, None, cou)
            if (dbl.tail is not None): 
                dbl.tail = (Utils.asObjectOrNull(UnitextImplantateHelper.clear(dbl.tail, id0_, type_name, cnt_typ, None, cou), UnitextContainer))
            if (dbl.appendix is not None): 
                dbl.appendix = (Utils.asObjectOrNull(UnitextImplantateHelper.clear(dbl.appendix, id0_, type_name, cnt_typ, None, cou), UnitextContainer))
            return dbl
        cnt = Utils.asObjectOrNull(content, UnitextContainer)
        if (cnt is None): 
            return content
        i = 0
        while i < len(cnt.children): 
            cc = UnitextImplantateHelper.clear(cnt.children[i], id0_, type_name, cnt_typ, cnt, cou)
            if (cc is None): 
                pass
            cnt.children[i] = cc
            i += 1
        if (id0_ is not None): 
            if (cnt.id0_ != id0_): 
                return content
        if (len(cnt.children) == 0): 
            return None
        if (len(cnt.children) == 1): 
            cnt.children[0].parent = cnt.parent
            return cnt.children[0]
        if (own is None): 
            return content
        ii = own.get_child_index_of(cnt)
        if (ii < 0): 
            return content
        del own.children[ii]
        own.children[ii:ii] = cnt.children
        for ch in own.children: 
            ch.parent = (own)
        cou.value += 1
        return own.children[ii]
    
    @staticmethod
    def __split_texts(content : 'UnitextItem', begin : int, end : int, own : 'UnitextContainer'=None) -> 'UnitextItem':
        if (content is None): 
            return None
        if (end < content.begin_char): 
            return content
        if (begin > content.end_char): 
            return content
        if (begin <= content.begin_char and end >= content.end_char): 
            return content
        tab = Utils.asObjectOrNull(content, UnitextTable)
        if (tab is not None): 
            cel = tab._find_cell_by_pos(begin)
            if (cel is not None and cel.content is not None): 
                cel.content = UnitextImplantateHelper.__split_texts(cel.content, begin, end, None)
            return tab
        li = Utils.asObjectOrNull(content, UnitextList)
        if (li is not None): 
            for l_ in li.items: 
                if (l_.prefix is not None): 
                    l_.prefix = UnitextImplantateHelper.__split_texts(l_.prefix, begin, end, None)
                if (l_.content is not None): 
                    l_.content = UnitextImplantateHelper.__split_texts(l_.content, begin, end, None)
                if (l_.sublist is not None): 
                    UnitextImplantateHelper.__split_texts(l_.sublist, begin, end, None)
            return li
        foot = Utils.asObjectOrNull(content, UnitextFootnote)
        if (foot is not None): 
            if (foot.content is not None): 
                foot.content = UnitextImplantateHelper.__split_texts(foot.content, begin, end, None)
            return foot
        hyp = Utils.asObjectOrNull(content, UnitextHyperlink)
        if (hyp is not None): 
            if (hyp.content is not None): 
                hyp.content = UnitextImplantateHelper.__split_texts(hyp.content, begin, end, None)
            return hyp
        dbl = Utils.asObjectOrNull(content, UnitextDocblock)
        if (dbl is not None): 
            if (dbl.head is not None): 
                hh = Utils.asObjectOrNull(UnitextImplantateHelper.__split_texts(dbl.head, begin, end, None), UnitextContainer)
                if (dbl in hh.children): 
                    pass
                dbl.head = hh
            if (dbl.body is not None): 
                dbl.body = UnitextImplantateHelper.__split_texts(dbl.body, begin, end, None)
            if (dbl.tail is not None): 
                dbl.tail = (Utils.asObjectOrNull(UnitextImplantateHelper.__split_texts(dbl.tail, begin, end, None), UnitextContainer))
            if (dbl.appendix is not None): 
                dbl.appendix = UnitextImplantateHelper.__split_texts(dbl.appendix, begin, end, None)
            return dbl
        cnt = Utils.asObjectOrNull(content, UnitextContainer)
        if (cnt is not None): 
            i = 0
            first_pass685 = True
            while True:
                if first_pass685: first_pass685 = False
                else: i += 1
                if (not (i < len(cnt.children))): break
                ch = cnt.children[i]
                if (ch.end_char < begin): 
                    continue
                if (ch.begin_char > end): 
                    if (end == (begin - 1) and ch.begin_char <= begin): 
                        pass
                    else: 
                        break
                cc = UnitextImplantateHelper.__split_texts(ch, begin, end, cnt)
                if (cc is None): 
                    pass
                cnt.children[i] = cc
            return content
        txt = Utils.asObjectOrNull(content, UnitextPlaintext)
        if (txt is not None): 
            if (begin == txt.begin_char and end == txt.end_char): 
                return txt
            creat = False
            if (own is None): 
                own = UnitextContainer._new377(txt.parent, txt.begin_char, txt.end_char, "cnt0_{0}_{1}".format(txt.begin_char, txt.end_char))
                own.children.append(txt)
                creat = True
            ii = own.get_child_index_of(content)
            if (ii < 0): 
                return content
            jj = ii
            del own.children[ii]
            if (begin > txt.begin_char): 
                b = txt._remove_start(begin - txt.begin_char)
                if (b is not None): 
                    own.children.insert(jj, b)
                    jj += 1
            if (end < txt.end_char): 
                e0_ = txt._remove_end(txt.end_char - end)
                if (e0_ is not None): 
                    own.children.insert(jj, e0_)
            own.children.insert(jj, txt)
            txt.parent = (own)
            if (creat): 
                return own
            else: 
                return own.children[ii]
        return content
    
    @staticmethod
    def implantate(content : 'UnitextItem', impl : 'UnitextContainer', text : str, own : 'UnitextContainer'=None) -> 'UnitextItem':
        if (content is None or content == impl): 
            return content
        if (impl.end_char < content.begin_char): 
            return content
        if (impl.begin_char > content.end_char): 
            return content
        if ((impl.begin_char == content.begin_char and impl.end_char == content.end_char and own is None) and not (isinstance(content, UnitextContainer))): 
            impl.parent = content.parent
            impl.children.append(content)
            content.parent = (impl)
            return impl
        content = UnitextImplantateHelper.__split_texts(content, impl.begin_char, impl.end_char, own)
        if (content is None): 
            return None
        if (content == impl): 
            return content
        if (impl.begin_char <= content._get_plaintext_ns_pos(text) and content._get_plaintext_ns_pos1(text) <= impl.end_char): 
            if ((isinstance(content, UnitextDocblock)) and Utils.compareStrings(Utils.ifNotNull(content.typname, ""), "Footnote", True) == 0): 
                db = Utils.asObjectOrNull(content, UnitextDocblock)
                if (db.body is not None): 
                    db.body = UnitextImplantateHelper.implantate(db.body, impl, text, None)
                    return db.body
            if (((impl.typ == UnitextContainerType.NUMBER or impl.typ == UnitextContainerType.NAME)) and (isinstance(content, UnitextContainer)) and content.typ == UnitextContainerType.HEAD): 
                for ch in content.children: 
                    ch.parent = (impl)
                    impl.children.append(ch)
                impl.parent = content.parent
            else: 
                cnt1 = Utils.asObjectOrNull(content, UnitextContainer)
                if (cnt1 is not None): 
                    i = 0
                    while i < len(cnt1.children): 
                        ch = cnt1.children[i]
                        if (ch.begin_char <= impl.begin_char and impl.end_char <= ch.end_char): 
                            ch1 = UnitextImplantateHelper.implantate(ch, impl, text, None)
                            if (ch1 is None): 
                                return None
                            cnt1.children[i] = ch1
                            ch1.parent = (cnt1)
                            return content
                        i += 1
                impl.children.append(content)
                impl.parent = content.parent
                content.parent = (impl)
            if (impl.end_char > content.end_char or (impl.begin_char < content.begin_char)): 
                impl.begin_char = content.begin_char
                impl.end_char = content.end_char
            if (own is not None): 
                ii = own.get_child_index_of(content)
                if (ii >= 0): 
                    own.children[ii] = (impl)
                    impl.parent = (own)
                else: 
                    return content
            return impl
        tab = Utils.asObjectOrNull(content, UnitextTable)
        if (tab is not None): 
            cel = tab._find_cell_by_pos(impl.begin_char)
            if (cel is not None and cel.content is not None): 
                cel.content = UnitextImplantateHelper.implantate(cel.content, impl, text, None)
            return tab
        li = Utils.asObjectOrNull(content, UnitextList)
        if (li is not None): 
            for l_ in li.items: 
                if (l_.begin_char <= impl.begin_char and impl.begin_char <= l_.end_char): 
                    if (l_.prefix is not None): 
                        l_.prefix = UnitextImplantateHelper.implantate(l_.prefix, impl, text, None)
                    if (l_.content is not None): 
                        l_.content = UnitextImplantateHelper.implantate(l_.content, impl, text, None)
                    if (l_.sublist is not None): 
                        UnitextImplantateHelper.implantate(l_.sublist, impl, text, None)
            return li
        foot = Utils.asObjectOrNull(content, UnitextFootnote)
        if (foot is not None): 
            if (foot.content is not None): 
                foot.content = UnitextImplantateHelper.implantate(foot.content, impl, text, None)
            return foot
        hyp = Utils.asObjectOrNull(content, UnitextHyperlink)
        if (hyp is not None): 
            if (hyp.content is not None): 
                hyp.content = UnitextImplantateHelper.implantate(hyp.content, impl, text, None)
            return hyp
        dbl = Utils.asObjectOrNull(content, UnitextDocblock)
        if (dbl is not None): 
            if (dbl.head is not None): 
                hh = Utils.asObjectOrNull(UnitextImplantateHelper.implantate(dbl.head, impl, text, None), UnitextContainer)
                if (dbl in hh.children): 
                    pass
                dbl.head = hh
            if (dbl.body is not None): 
                dbl.body = UnitextImplantateHelper.implantate(dbl.body, impl, text, None)
            if (dbl.tail is not None): 
                dbl.tail = (Utils.asObjectOrNull(UnitextImplantateHelper.implantate(dbl.tail, impl, text, None), UnitextContainer))
            if (dbl.appendix is not None): 
                dbl.appendix = UnitextImplantateHelper.implantate(dbl.appendix, impl, text, None)
            return dbl
        cnt = Utils.asObjectOrNull(content, UnitextContainer)
        if (cnt is not None): 
            i = 0
            first_pass686 = True
            while True:
                if first_pass686: first_pass686 = False
                else: i += 1
                if (not (i < len(cnt.children))): break
                if (i == 49): 
                    pass
                ch = cnt.children[i]
                if (impl.end_char < ch.begin_char): 
                    if (impl.end_char == (impl.begin_char - 1) and impl.begin_char == ch.begin_char): 
                        pass
                    else: 
                        continue
                if (impl.begin_char > ch.end_char): 
                    continue
                if (((isinstance(ch, UnitextFootnote)) or (isinstance(ch, UnitextTable)) or (isinstance(ch, UnitextList))) or (isinstance(ch, UnitextHyperlink)) or (isinstance(ch, UnitextDocblock))): 
                    UnitextImplantateHelper.implantate(ch, impl, text, cnt)
                    if (impl.parent is not None): 
                        break
                    continue
                if (isinstance(ch, UnitextComment)): 
                    continue
                if (ch.begin_char > ch.end_char): 
                    continue
                i1 = impl._get_plaintext_ns_pos(text)
                i2 = ch._get_plaintext_ns_pos(text)
                e1 = impl._get_plaintext_ns_pos1(text)
                e2 = ch._get_plaintext_ns_pos1(text)
                if (i1 > i2 or ((i1 == i2 and (e1 < e2)))): 
                    if (isinstance(ch, UnitextContainer)): 
                        cc = UnitextImplantateHelper.implantate(ch, impl, text, None)
                        if (cc is None): 
                            pass
                        cnt.children[i] = cc
                    continue
                j = 0
                j = i
                while j < len(cnt.children): 
                    ch = cnt.children[j]
                    if (impl.end_char < ch.begin_char): 
                        if (impl.end_char == (impl.begin_char - 1) and impl.begin_char == ch.begin_char): 
                            cnt.children.insert(j, impl)
                            impl.parent = (cnt)
                            return content
                        break
                    if (ch == impl): 
                        return content
                    impl.children.append(ch)
                    ch.parent = (impl)
                    j += 1
                if (j > i): 
                    cnt.children[i] = (impl)
                    impl.parent = (cnt)
                    if (j > (i + 1)): 
                        del cnt.children[i + 1:i + 1+j - i - 1]
                    impl.end_char = impl.children[len(impl.children) - 1].end_char
                break
            return content
        impl.children.append(content)
        impl.parent = content.parent
        content.parent = (impl)
        if (own is not None): 
            ii = own.get_child_index_of(content)
            if (ii >= 0): 
                own.children[ii] = (impl)
                impl.parent = (own)
            else: 
                return content
        return impl
    
    @staticmethod
    def _is_table_char(ch : 'char') -> bool:
        return (ord(ch)) == 7 or (ord(ch)) == 0x1E or (ord(ch)) == 0x1F
    
    @staticmethod
    def implantate_block(content : 'UnitextItem', begin_head : int, begin_body : int, begin_tail : int, begin_appendix : int, end : int, text : str, own : 'UnitextContainer', res : 'UnitextDocblock') -> 'UnitextItem':
        if (content is None): 
            return None
        if (end < content.begin_char): 
            return content
        if (begin_head > content.end_char): 
            return content
        if ((begin_head < begin_body) and (begin_body < end)): 
            content = UnitextImplantateHelper.__split_texts(content, begin_head, begin_body - 1, own)
        tab = Utils.asObjectOrNull(content, UnitextTable)
        if (tab is not None): 
            bh = begin_head
            while bh < len(text): 
                if (not UnitextImplantateHelper._is_table_char(text[bh])): 
                    break
                bh += 1
            bb = begin_body
            if (bb < bh): 
                bb = bh
            r = 0
            while r < tab.rows_count: 
                c = 0
                first_pass687 = True
                while True:
                    if first_pass687: first_pass687 = False
                    else: c += 1
                    if (not (c < tab.cols_count)): break
                    cel = tab.get_cell(r, c)
                    if (cel is None or cel.content is None): 
                        continue
                    c = cel.col_end
                    if (cel.begin_char <= bh and bh <= cel.end_char and cel.row_begin == cel.row_end): 
                        if ((bh < bb) and cel.end_char > bh and bb > cel.end_char): 
                            res0 = UnitextDocblock._new378(bh, cel.end_char)
                            res0.head = UnitextContainer._new92(UnitextContainerType.HEAD)
                            res0.head.children.append(cel.content)
                            res0.head.begin_char = bh
                            res0.head.end_char = cel.end_char
                            cel.content = (res0)
                            if (res.value is None): 
                                res.value = res0
                            return tab
                        cel.content = UnitextImplantateHelper.implantate_block(cel.content, begin_head, begin_body, begin_tail, begin_appendix, end, text, None, res)
                    elif (cel.begin_char <= bb and bb <= cel.end_char): 
                        if ((bh < bb) and cel.end_char > bh and bb > cel.end_char): 
                            res0 = UnitextDocblock._new378(bh, cel.end_char)
                            res0.body = (UnitextContainer._new92(UnitextContainerType.HEAD))
                            res0.body.children.append(cel.content)
                            res0.body.begin_char = bb
                            res0.body.end_char = cel.end_char
                            cel.content = (res0)
                            if (res.value is None): 
                                res.value = res0
                            return tab
                        cel.content = UnitextImplantateHelper.implantate_block(cel.content, begin_head, begin_body, begin_tail, begin_appendix, end, text, None, res)
                r += 1
            return tab
        li = Utils.asObjectOrNull(content, UnitextList)
        if (li is not None): 
            for l_ in li.items: 
                if (l_.begin_char <= begin_head and begin_head <= l_.end_char): 
                    if (l_.content is not None): 
                        l_.content = UnitextImplantateHelper.implantate_block(l_.content, begin_head, begin_body, begin_tail, begin_appendix, end, text, None, res)
                    if (l_.sublist is not None): 
                        UnitextImplantateHelper.implantate_block(l_.sublist, begin_head, begin_body, begin_tail, begin_appendix, end, text, None, res)
            return li
        cnt = Utils.asObjectOrNull(content, UnitextContainer)
        if (cnt is not None): 
            i = 0
            first_pass688 = True
            while True:
                if first_pass688: first_pass688 = False
                else: i += 1
                if (not (i < len(cnt.children))): break
                ch = cnt.children[i]
                if (ch.is_whitespaces): 
                    continue
                if (end < ch.begin_char): 
                    break
                if ((isinstance(ch, UnitextTable)) or (isinstance(ch, UnitextList)) or (isinstance(ch, UnitextDocblock))): 
                    pass
                if (begin_head > ch._get_plaintext_ns_pos(text)): 
                    if ((begin_head < ch.end_char) and (isinstance(ch, UnitextTable))): 
                        UnitextImplantateHelper.implantate_block(ch, begin_head, begin_body, begin_tail, begin_appendix, end, text, None, res)
                        return content
                    continue
                if (ch != cnt.children[i]): 
                    pass
                ch = cnt.children[i]
                if (isinstance(ch, UnitextDocblock)): 
                    continue
                if ((isinstance(ch, UnitextList)) and (begin_head < begin_body) and ch._get_plaintext_ns_pos(text) == begin_head): 
                    list0_ = Utils.asObjectOrNull(ch, UnitextList)
                    jj = i + 1
                    for it in list0_.items: 
                        if (it.prefix is not None): 
                            it.prefix.parent = (cnt)
                            cnt.children.insert(jj, it.prefix)
                            jj += 1
                            sp = UnitextPlaintext._new51(" ")
                            sp.begin_char = (it.prefix.end_char + 1)
                            sp.end_char = sp.begin_char
                            sp.parent = (cnt)
                            cnt.children.insert(jj, sp)
                            jj += 1
                        if (it.content is not None): 
                            it.content.parent = (cnt)
                            cnt.children.insert(jj, it.content)
                            jj += 1
                        nl = UnitextNewline()
                        nl.begin_char = (cnt.children[jj - 1].end_char + 1)
                        nl.end_char = nl.begin_char
                        nl.parent = (cnt)
                        cnt.children.insert(jj, nl)
                        jj += 1
                        if (it.sublist is not None): 
                            it.sublist.parent = (cnt)
                            cnt.children.insert(jj, it.sublist)
                            jj += 1
                    del cnt.children[i]
                    i -= 1
                    continue
                if ((isinstance(ch, UnitextTable)) and ch.begin_char <= begin_head and (end < ch.end_char)): 
                    UnitextImplantateHelper.implantate_block(ch, begin_head, begin_body, begin_tail, begin_appendix, end, text, None, res)
                    return content
                res.value = UnitextDocblock._new378(begin_head, end)
                head = UnitextContainer._new92(UnitextContainerType.HEAD)
                body = UnitextContainer()
                tail = UnitextContainer._new92(UnitextContainerType.TAIL)
                apps = UnitextContainer()
                j = 0
                j = i
                while j < len(cnt.children): 
                    if (begin_head == begin_body): 
                        break
                    ch = cnt.children[j]
                    if (not ch.is_whitespaces): 
                        ppp = ch._get_plaintext_ns_pos1(text)
                        if (begin_body < ppp): 
                            break
                        if (begin_body == ppp and (begin_body < end)): 
                            break
                    head.children.append(ch)
                    ch.parent = (head)
                    j += 1
                while j < len(cnt.children): 
                    if (begin_body == begin_tail or begin_body == begin_appendix): 
                        break
                    ch = cnt.children[j]
                    if (not ch.is_whitespaces): 
                        if (begin_tail < ch._get_plaintext_ns_pos1(text)): 
                            break
                    body.children.append(ch)
                    ch.parent = (body)
                    j += 1
                while j < len(cnt.children): 
                    if (begin_tail == end): 
                        break
                    ch = cnt.children[j]
                    if (not ch.is_whitespaces): 
                        if (begin_appendix < ch._get_plaintext_ns_pos1(text)): 
                            break
                    tail.children.append(ch)
                    ch.parent = (tail)
                    j += 1
                while j < len(cnt.children): 
                    if (begin_appendix == end): 
                        break
                    ch = cnt.children[j]
                    if (not ch.is_whitespaces): 
                        if (end < ch._get_plaintext_ns_pos1(text)): 
                            break
                    apps.children.append(ch)
                    ch.parent = (apps)
                    j += 1
                if (j > i): 
                    cnt.children[i] = (res.value)
                    res.value.parent = (cnt)
                    if (j > (i + 1)): 
                        del cnt.children[i + 1:i + 1+j - i - 1]
                    if (len(head.children) > 0): 
                        res.value.head = head
                        head.parent = (res.value)
                        head.begin_char = begin_head
                        head.end_char = head.children[len(head.children) - 1].end_char
                    if (len(body.children) > 0): 
                        res.value.body = (body)
                        body.parent = (res.value)
                        body.begin_char = begin_body
                        body.end_char = body.children[len(body.children) - 1].end_char
                    if (len(tail.children) > 0): 
                        res.value.tail = tail
                        tail.parent = (res.value)
                        tail.begin_char = begin_tail
                        tail.end_char = tail.children[len(tail.children) - 1].end_char
                    if (len(apps.children) > 0): 
                        res.value.appendix = (apps)
                        apps.parent = (res.value)
                        apps.begin_char = begin_appendix
                        apps.end_char = apps.children[len(apps.children) - 1].end_char
                break
            return content
        if ((isinstance(content, UnitextPlaintext)) and (((isinstance(content.parent, UnitextTablecell)) or (isinstance(content.parent, UnitextListitem))))): 
            if ((content.begin_char == begin_body and begin_body == begin_head and end == begin_tail) and end == begin_appendix and end == content.end_char): 
                res.value = UnitextDocblock._new378(begin_head, end)
                res.value.body = content
                return res.value
        return content