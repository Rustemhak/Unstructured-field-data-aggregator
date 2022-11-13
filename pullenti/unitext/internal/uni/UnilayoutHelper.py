# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import math
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.UnitextImage import UnitextImage
from pullenti.unitext.UnitextPlaintextType import UnitextPlaintextType
from pullenti.unitext.UnitextNewline import UnitextNewline
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak
from pullenti.unitext.FileFormat import FileFormat
from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextPagesection import UnitextPagesection

class UnilayoutHelper:
    
    class LayLine(object):
        
        def __init__(self) -> None:
            self.boxes = list()
        
        def can_be_equals_except_page_number(self, ll : 'LayLine') -> bool:
            if (len(ll.boxes) != len(self.boxes)): 
                return False
            i = 0
            first_pass673 = True
            while True:
                if first_pass673: first_pass673 = False
                else: i += 1
                if (not (i < len(ll.boxes))): break
                b0 = self.boxes[i]
                b1 = ll.boxes[i]
                if (b0.text is None and b1.text is None): 
                    if (b0.image_content is not None and b1.image_content is not None): 
                        if (len(b0.image_content) != len(b1.image_content)): 
                            return False
                        j = 0
                        while j < len(b0.image_content): 
                            if (b0.image_content[j] != b1.image_content[j]): 
                                return False
                            j += 1
                    else: 
                        return False
                    continue
                if (b0.text is None or b1.text is None): 
                    return False
                if (b0.text == b1.text): 
                    continue
                i0 = 0
                i1 = 0
                while (i0 < len(b0.text)) and (i1 < len(b1.text)):
                    ch0 = b0.text[i0]
                    ch1 = b1.text[i1]
                    if (ch0 == ch1): 
                        i0 += 1
                        i1 += 1
                        continue
                    oo = False
                    while (i0 < len(b0.text)) and str.isdigit(b0.text[i0]):
                        i0 += 1
                        oo = True
                    while (i1 < len(b1.text)) and str.isdigit(b1.text[i1]):
                        i1 += 1
                        oo = True
                    if (not oo): 
                        return False
                if ((i0 < len(b0.text)) or (i1 < len(b1.text))): 
                    return False
            return True
        
        def __str__(self) -> str:
            txt = io.StringIO()
            for b in self.boxes: 
                if (b.text is not None): 
                    if (txt.tell() > 0): 
                        print(' ', end="", file=txt)
                    print(b.text, end="", file=txt)
            return "{0} X={1} X1={2} Y={3} Y2={4}".format(Utils.toStringStringIO(txt), self.x, self.x + self.width, self.y, self.y + self.height)
        
        @property
        def x(self) -> float:
            return (0 if len(self.boxes) == 0 else math.floor(self.boxes[0].left))
        
        @property
        def width(self) -> float:
            if (len(self.boxes) == 0): 
                return 0
            return (self.boxes[len(self.boxes) - 1].right - self.boxes[0].left)
        
        @property
        def y(self) -> float:
            y_ = 0
            for w in self.boxes: 
                y_ += w.top
            if (len(self.boxes) > 0): 
                y_ /= (len(self.boxes))
            return y_
        
        @property
        def height(self) -> float:
            y_ = 0
            h = 0
            for w in self.boxes: 
                y_ += w.top
                h += w.bottom
            if (len(self.boxes) > 0): 
                y_ /= (len(self.boxes))
                h /= (len(self.boxes))
                h -= y_
            return h
        
        def try_append(self, r : 'UnilayRectangle') -> bool:
            if (len(self.boxes) == 0): 
                self.boxes.append(r)
                return True
            if ((((r.top + r.bottom)) / (2)) < self.y): 
                return False
            if (r.top > ((self.y + ((self.height / (2)))))): 
                return False
            if (r.left >= ((self.x + self.width) - (2))): 
                self.boxes.append(r)
                return True
            i = 0
            while i < len(self.boxes): 
                if (r.right <= self.boxes[i].left): 
                    self.boxes.insert(i, r)
                    return True
                i += 1
            return False
        
        def compareTo(self, obj : object) -> int:
            l_ = Utils.asObjectOrNull(obj, UnilayoutHelper.LayLine)
            if (self.y < l_.y): 
                return -1
            if (self.y > l_.y): 
                return 1
            if (self.x < l_.x): 
                return -1
            if (self.x > l_.x): 
                return 1
            return 0
    
    @staticmethod
    def _correct_pdf_spacings(pages : typing.List['UnilayPage']) -> None:
        sp0 = 0
        sp1 = 0
        for p in pages: 
            for r in p.rects: 
                if (r.text is not None): 
                    i = 0
                    while i < (len(r.text) - 1): 
                        ch1 = r.text[i]
                        ch2 = r.text[i + 1]
                        if (not Utils.isWhitespace(ch1)): 
                            if (not Utils.isWhitespace(ch2)): 
                                sp0 += 1
                            elif (((i + 2) < len(r.text)) and not Utils.isWhitespace(r.text[i + 2])): 
                                sp1 += 1
                        i += 1
        if (sp0 > (math.floor(sp1 / 100))): 
            return
        tmp = io.StringIO()
        for p in pages: 
            for r in p.rects: 
                if (r.text is not None): 
                    Utils.setLengthStringIO(tmp, 0)
                    i = 0
                    first_pass674 = True
                    while True:
                        if first_pass674: first_pass674 = False
                        else: i += 1
                        if (not (i < len(r.text))): break
                        ch1 = r.text[i]
                        if (Utils.isWhitespace(ch1)): 
                            continue
                        print(ch1, end="", file=tmp)
                        j = 0
                        k = 0
                        j = (i + 1)
                        while j < len(r.text): 
                            if (not Utils.isWhitespace(r.text[j])): 
                                break
                            else: 
                                k += 1
                            j += 1
                        k = math.floor(k / 2)
                        while k > 0: 
                            print(' ', end="", file=tmp)
                            k -= 1
                    r.text = Utils.toStringStringIO(tmp)
    
    @staticmethod
    def _correct_pdf_encoding(pages : typing.List['UnilayPage']) -> None:
        tot = 0
        err = 0
        lat = 0
        rus = 0
        for p in pages: 
            for r in p.rects: 
                if (r.text is not None): 
                    for ch in r.text: 
                        if (str.isalpha(ch)): 
                            tot += 1
                            cod = ord(ch)
                            if (cod < 0x80): 
                                lat += 1
                            elif (cod < 0x100): 
                                err += 1
                            elif (cod >= 0x400 and (cod < 0x500)): 
                                rus += 1
        if (err > 10 and err > (math.floor(tot / 2)) and (rus < (math.floor(err / 2)))): 
            pass
        else: 
            return
        tmp = io.StringIO()
        b1 = Utils.newArrayOfBytes(1, 0)
        for p in pages: 
            for r in p.rects: 
                if (r.text is not None): 
                    Utils.setLengthStringIO(tmp, 0)
                    for ch in r.text: 
                        cod = ord(ch)
                        res_ch = ch
                        if (cod > 0x80 and (cod < 0x100)): 
                            b1[0] = (cod)
                            s = MiscHelper.decode_string1251(b1, 0, -1)
                            if ((s is not None and len(s) == 1 and (ord(s[0])) >= 0x400) and ((ord(s[0])) < 0x500)): 
                                res_ch = s[0]
                                if (((res_ch >= 'А' and res_ch <= 'Я')) or ((res_ch >= 'а' and res_ch <= 'я'))): 
                                    pass
                                elif (res_ch == 'њ'): 
                                    res_ch = 'Ё'
                                elif (cod == 188): 
                                    res_ch = 'ё'
                                elif (cod == 190): 
                                    res_ch = '«'
                                elif (cod == 191): 
                                    res_ch = '»'
                                else: 
                                    pass
                            else: 
                                pass
                        print(res_ch, end="", file=tmp)
                    r.text = Utils.toStringStringIO(tmp)
    
    @staticmethod
    def __cm_from_pt(pt : int) -> float:
        v = pt
        v = ((v * 2.54) / (72))
        return round(v, 1)
    
    @staticmethod
    def create_content_from_pages(doc : 'UnitextDocument', after_ocr : bool) -> None:
        if (len(doc.pages) == 0): 
            return
        if (doc.source_format == FileFormat.PDF and not after_ocr): 
            UnilayoutHelper._correct_pdf_encoding(doc.pages)
        cnt = UnitextContainer()
        doc.content = (cnt)
        plines = list()
        for p in doc.pages: 
            plines.append(UnilayoutHelper.__correct_page_lines(p))
        head_title = list()
        header = None
        footer = None
        if (len(doc.pages) > 1): 
            while len(plines[0]) > 0:
                if (len(head_title) > 0): 
                    if (plines[0][0].y > (head_title[0].y + head_title[0].height)): 
                        break
                pn = 0
                eq = 0
                pn = 1
                while pn < len(plines): 
                    if (len(plines[pn]) > 0): 
                        if (plines[pn][0].can_be_equals_except_page_number(plines[0][0])): 
                            eq += 1
                        else: 
                            break
                    pn += 1
                if (eq > 0 and pn >= len(plines)): 
                    head_title.append(plines[0][0])
                    for pp in plines: 
                        if (len(pp) > 0): 
                            del pp[0]
                    continue
                break
            if (len(head_title) > 0): 
                fcnt = UnitextContainer()
                for ht in head_title: 
                    for b in ht.boxes: 
                        b.ignored = True
                        if (b.text is not None): 
                            fcnt.children.append(UnitextPlaintext._new51(b.text))
                        elif (b.image_content is not None): 
                            fcnt.children.append(UnitextImage._new260(b.image_content))
                ttt = fcnt.get_plaintext_string(None)
                if (ttt is not None and len(ttt) > 5): 
                    header = (fcnt)
        cur = UnitextPagesection()
        cur.width = UnilayoutHelper.__cm_from_pt(doc.pages[0].width)
        cur.height = UnilayoutHelper.__cm_from_pt(doc.pages[0].height)
        doc.sections.append(cur)
        pn = 0
        first_pass675 = True
        while True:
            if first_pass675: first_pass675 = False
            else: pn += 1
            if (not (pn < len(doc.pages))): break
            p = doc.pages[pn]
            if (pn > 0): 
                cnt.children.append(UnitextPagebreak._new333(cur.id0_))
            pw = UnilayoutHelper.__cm_from_pt(p.width)
            ph = UnilayoutHelper.__cm_from_pt(p.height)
            if (math.fabs(pw - cur.width) > 1 or math.fabs(ph - cur.height) > 1): 
                cur = UnitextPagesection()
                doc.sections.append(cur)
                cur.id0_ = "ps{0}".format(len(doc.sections))
                cur.width = pw
                cur.height = ph
            lines = plines[pn]
            if (lines is None): 
                continue
            char_width = 0
            cou = 0
            for l_ in lines: 
                for r in l_.boxes: 
                    if (r.text is not None): 
                        cou += len(r.text)
                        char_width += (r.right - r.left)
            if (cou > 0): 
                char_width /= (cou)
            i = 0
            while i < len(lines): 
                if (i > 0): 
                    cou = 1
                    h1 = lines[i - 1].height
                    h2 = lines[i].height
                    y1 = lines[i - 1].y
                    y2 = lines[i].y
                    if (((h1 < (h2 * (0.75)))) or (((h1 * (0.75)) >= h2))): 
                        cou = 2
                    elif ((y1 + h1) <= y2 and h1 > 0): 
                        cou = (math.floor((((y2 - y1)) / h1)))
                        if (cou < 1): 
                            cou = 1
                        elif (cou > 5): 
                            cou = 5
                    elif (y1 > y2): 
                        cou = 3
                    cnt.children.append(UnitextNewline._new334(cou, cur.id0_))
                l_ = lines[i]
                for b in l_.boxes: 
                    b.tag = None
                if (i == 13): 
                    pass
                j = 0
                while j < len(l_.boxes): 
                    r = l_.boxes[j]
                    r.line_number = (j + 1)
                    if (j > 0): 
                        d = r.left - l_.boxes[j - 1].right
                        if (d > (char_width / (3))): 
                            sps = (math.floor((d / char_width)) if char_width > 0 else 1)
                            if (sps < 1): 
                                sps = 1
                            str0_ = " "
                            while sps > 1: 
                                str0_ = (str0_ + " ")
                                sps -= 1
                            cnt.children.append(UnitextPlaintext._new335(str0_, cur.id0_))
                    if (r.text is not None): 
                        txt = UnitextPlaintext._new335(r.text, cur.id0_)
                        txt.layout = Utils.newArray(len(r.text), None)
                        k = 0
                        while k < len(txt.layout): 
                            txt.layout[k] = r
                            k += 1
                        cnt.children.append(txt)
                        if (j > 0 and UnilayoutHelper.__has_letter_or_digit(txt.text)): 
                            r0 = l_.boxes[j - 1]
                            if (r0.tag is None and (r0.right + (3)) >= r.left): 
                                prev = (Utils.asObjectOrNull(cnt.children[len(cnt.children) - 2], UnitextPlaintext) if len(cnt.children) > 1 else None)
                                if (prev is not None and UnilayoutHelper.__has_letter_or_digit(prev.text)): 
                                    if (r.bottom > ((((r0.bottom + r0.top)) / (2))) and r.bottom > r0.top and (r.top < r0.top)): 
                                        if ((len(prev.text) < 3) and len(txt.text) > 4): 
                                            prev.typ = UnitextPlaintextType.SUB
                                        elif (len(txt.text) < 5): 
                                            r.tag = (txt)
                                            txt.typ = UnitextPlaintextType.SUP
                                    elif ((r.top < ((((r0.bottom + r0.top)) / (2)))) and (r.top < r0.bottom)): 
                                        if (r.bottom > ((r0.bottom + (((r.bottom - r0.top)) / (6))))): 
                                            if (prev is not None and (len(prev.text) < 3) and len(txt.text) > 4): 
                                                prev.typ = UnitextPlaintextType.SUP
                                            elif (len(txt.text) < 5): 
                                                r.tag = (txt)
                                                txt.typ = UnitextPlaintextType.SUB
                    elif (r.image_content is not None): 
                        img = UnitextImage._new337(r.image_content, r, cur.id0_)
                        img.width = "{0}pt".format(math.floor((r.right - r.left)))
                        img.height = "{0}pt".format(math.floor((r.bottom - r.top)))
                        cnt.children.append(img)
                    j += 1
                i += 1
            if (p.image_content is not None): 
                img = UnitextImage._new338(cur.id0_)
                img.content = p.image_content
                if (p.width > 0): 
                    img.width = "{0}pt".format(p.width)
                if (p.height > 0): 
                    img.height = "{0}pt".format(p.height)
                cnt.children.append(img)
    
    @staticmethod
    def __has_letter_or_digit(txt : str) -> bool:
        if (txt is not None): 
            for ch in txt: 
                if ((str.isalnum(ch) or ch == '*' or ch == '<') or ch == '>'): 
                    return True
        return False
    
    @staticmethod
    def __correct_page_lines(p : 'UnilayPage') -> typing.List['LayLine']:
        lines = list()
        for r in p.rects: 
            if (len(lines) > 0 and lines[len(lines) - 1].try_append(r)): 
                pass
            else: 
                l_ = UnilayoutHelper.LayLine()
                l_.boxes.append(r)
                lines.append(l_)
                if (len(lines) == 14): 
                    pass
        if (len(lines) < 1): 
            return lines
        height = 0
        x = 10000000
        for l_ in lines: 
            height += l_.height
            if (l_.x < x): 
                x = l_.x
        height /= (len(lines))
        errs = 0
        max0_ = math.floor((len(lines) * ((len(lines) - 1))) / 2)
        i = 0
        while i < (len(lines) - 1): 
            j = i + 1
            while j < len(lines): 
                if (lines[i].y > (lines[j].y + height)): 
                    errs += 1
                j += 1
            i += 1
        if (errs > (math.floor(max0_ / 2))): 
            ii = 0
            while ii < len(lines): 
                ch = False
                jj = 0
                while jj < (len(lines) - 1): 
                    if (lines[jj].compareTo(lines[jj + 1]) > 0): 
                        v = lines[jj]
                        lines[jj] = lines[jj + 1]
                        lines[jj + 1] = v
                        ch = True
                    jj += 1
                if (not ch): 
                    break
                ii += 1
        return lines