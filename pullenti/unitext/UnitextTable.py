# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Xml import XmlWriter

from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.UnitextTablecell import UnitextTablecell
from pullenti.unitext.UnitextStyledFragmentType import UnitextStyledFragmentType
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak
from pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextNewline import UnitextNewline
from pullenti.unitext.UnitextImage import UnitextImage
from pullenti.unitext.UnitextHyperlink import UnitextHyperlink

class UnitextTable(UnitextItem):
    """ Таблица, представляет собой матрицу из клеток.
    Ячейки могут заполнять прямоугольные области из клеток.
    Ячейки не могут пересекаться друг с другом.
    Таблица
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.__m_cells = list()
        self.__m_col_width = list()
        self.__m_cols_count = 0
        self.width = None;
        self.hide_borders = False
        self.may_has_error = False
        self.__m_map = None;
    
    def optimize(self, is_content : bool, pars : 'CreateDocumentParam') -> 'UnitextItem':
        if (self.__m_cols_count == 3 and len(self.__m_cells) == 2): 
            pass
        for ro in self.__m_cells: 
            for c in ro: 
                if (c is not None): 
                    c.optimize(False, pars)
        if (len(self.__m_cells) == 0): 
            return None
        r = 0
        while r < len(self.__m_cells): 
            c = 0
            first_pass709 = True
            while True:
                if first_pass709: first_pass709 = False
                else: c += 1
                if (not (c < len(self.__m_cells[r]))): break
                if (self.__m_cells[r][c] is not None): 
                    continue
                cc = 0
                cc = (c + 1)
                while cc < len(self.__m_cells[r]): 
                    if (self.__m_cells[r][cc] is not None): 
                        break
                    cc += 1
                self.add_cell(r, r, c, cc - 1, None)
            if (len(self.__m_cells[r]) < self.__m_cols_count): 
                self.add_cell(r, r, len(self.__m_cells[r]), self.__m_cols_count - 1, None)
            r += 1
        for i in range(self.__m_cols_count - 1, -1, -1):
            r = 0
            r = 0
            first_pass710 = True
            while True:
                if first_pass710: first_pass710 = False
                else: r += 1
                if (not (r < len(self.__m_cells))): break
                c = self.__m_cells[r][i]
                if (c is None): 
                    continue
                if (c.content is not None): 
                    if (c.col_begin == i): 
                        break
            if (r < len(self.__m_cells)): 
                continue
            r = 0
            while r < len(self.__m_cells): 
                c = 0
                first_pass711 = True
                while True:
                    if first_pass711: first_pass711 = False
                    else: c += 1
                    if (not (c < len(self.__m_cells[r]))): break
                    ce = self.__m_cells[r][c]
                    if (ce is None): 
                        continue
                    if (ce.col_begin != c or ce.row_begin != r): 
                        continue
                    if (ce.col_begin >= i): 
                        ce.col_begin = ce.col_begin - 1
                    if (ce.col_end >= i): 
                        ce.col_end = ce.col_end - 1
                r += 1
            r = 0
            while r < len(self.__m_cells): 
                del self.__m_cells[r][i]
                r += 1
            self.__m_cols_count -= 1
        for r in range(len(self.__m_cells) - 1, -1, -1):
            i = 0
            i = 0
            first_pass712 = True
            while True:
                if first_pass712: first_pass712 = False
                else: i += 1
                if (not (i < len(self.__m_cells[r]))): break
                cel = self.__m_cells[r][i]
                if (cel is None): 
                    continue
                if (cel.row_begin == r and cel.col_begin == i): 
                    if (cel.content is not None): 
                        break
            if (i < len(self.__m_cells[r])): 
                continue
            rr = 0
            while rr < len(self.__m_cells): 
                c = 0
                first_pass713 = True
                while True:
                    if first_pass713: first_pass713 = False
                    else: c += 1
                    if (not (c < len(self.__m_cells[r]))): break
                    ce = self.__m_cells[rr][c]
                    if (ce is None): 
                        continue
                    if (ce.col_begin != c or ce.row_begin != rr): 
                        continue
                    if (ce.row_begin >= r): 
                        ce.row_begin = ce.row_begin - 1
                    if (ce.row_end >= r): 
                        ce.row_end = ce.row_end - 1
                rr += 1
            del self.__m_cells[r]
        if (self.__m_cols_count == 1): 
            cnt = UnitextContainer()
            cnt.is_inline = False
            r = 0
            while r < len(self.__m_cells): 
                if (self.__m_cells[r][0].content is not None and self.__m_cells[r][0].row_begin == r): 
                    cnt.children.append(self.__m_cells[r][0].content)
                    cnt.children.append(UnitextNewline._new578(cnt))
                r += 1
            cnt.children.insert(0, UnitextNewline._new578(cnt))
            return cnt.optimize(False, pars)
        if (self.__m_cols_count == 0): 
            return None
        if (pars is not None and pars.split_table_rows): 
            r = 0
            first_pass714 = True
            while True:
                if first_pass714: first_pass714 = False
                else: r += 1
                if (not (r < self.rows_count)): break
                c = 0
                ppp = 0
                cou = 0
                c = 0
                first_pass715 = True
                while True:
                    if first_pass715: first_pass715 = False
                    else: c += 1
                    if (not (c < self.cols_count)): break
                    cel = self.get_cell(r, c)
                    if (cel is None): 
                        break
                    if (cel.col_begin != cel.col_end or cel.row_begin != cel.row_end): 
                        break
                    if (cel.content is None): 
                        continue
                    cnt = Utils.asObjectOrNull(cel.content, UnitextContainer)
                    if (cnt is None): 
                        break
                    i = 0
                    p = 0
                    i = 0
                    while i < len(cnt.children): 
                        ch = cnt.children[i]
                        if (((isinstance(ch, UnitextPlaintext)) or (isinstance(ch, UnitextHyperlink)) or (isinstance(ch, UnitextImage))) or (isinstance(ch, UnitextPagebreak))): 
                            pass
                        elif (isinstance(ch, UnitextNewline)): 
                            if (ch.count > 1): 
                                p += 1
                        else: 
                            break
                        i += 1
                    if (i < len(cnt.children)): 
                        break
                    if (p == 0): 
                        break
                    if (ppp == 0): 
                        ppp = p
                    elif (ppp != p): 
                        break
                    cou += 1
                if ((c < self.cols_count) or ppp == 0 or (cou < 2)): 
                    continue
                nrow = list()
                rr = r + 1
                while rr < len(self.__m_cells): 
                    c = 0
                    while c < self.cols_count: 
                        if (self.__m_cells[rr][c] is not None): 
                            self.__m_cells[rr][c].tag = None
                        c += 1
                    rr += 1
                rr = r + 1
                while rr < len(self.__m_cells): 
                    c = 0
                    while c < self.cols_count: 
                        if (self.__m_cells[rr][c] is not None and self.__m_cells[rr][c].tag is None): 
                            self.__m_cells[rr][c].tag = (self.__m_cells)
                            self.__m_cells[rr][c].row_begin = self.__m_cells[rr][c].row_begin + 1
                            self.__m_cells[rr][c].row_end = self.__m_cells[rr][c].row_end + 1
                        c += 1
                    rr += 1
                self.__m_cells.insert(r + 1, nrow)
                c = 0
                first_pass716 = True
                while True:
                    if first_pass716: first_pass716 = False
                    else: c += 1
                    if (not (c < self.cols_count)): break
                    cel = self.get_cell(r, c)
                    cel1 = UnitextTablecell._new580(True, c, c, r + 1, r + 1)
                    nrow.append(cel1)
                    if (cel.content is None): 
                        continue
                    cnt = Utils.asObjectOrNull(cel.content, UnitextContainer)
                    i = 0
                    for i in range(len(cnt.children) - 1, -1, -1):
                        if (isinstance(cnt.children[i], UnitextPagebreak)): 
                            del cnt.children[i]
                    else: i = -1
                    i = 0
                    while i < len(cnt.children): 
                        if ((isinstance(cnt.children[i], UnitextNewline)) and cnt.children[i].count > 1): 
                            break
                        i += 1
                    if (i >= len(cnt.children)): 
                        continue
                    if (i == 1): 
                        cel1.content = (cnt)
                        cel.content = cnt.children[0]
                        del cnt.children[0]
                        del cnt.children[0]
                        cel1.content = cel1.content.optimize(True, pars)
                    else: 
                        cnt1 = UnitextContainer()
                        ii = i + 1
                        while ii < len(cnt.children): 
                            cnt1.children.append(cnt.children[ii])
                            ii += 1
                        del cnt.children[i:i+len(cnt.children) - i]
                        cel1.content = cnt1.optimize(True, pars)
        return self
    
    def add_cell(self, row_begin : int, row_end : int, col_begin : int, col_end : int, content : 'UnitextItem'=None) -> 'UnitextTablecell':
        """ Добавить ячейку
        
        Args:
            row_begin(int): начальная строка
            row_end(int): конечная строка
            col_begin(int): начальный столбец
            col_end(int): конечный столбец
            content(UnitextItem): возможное содержимое
        
        Returns:
            UnitextTablecell: если null, то значит область пересекается с существующей ячейкой
        """
        if ((row_begin < 0) or row_begin > row_end): 
            return None
        if ((col_begin < 0) or col_begin > col_end): 
            return None
        if ((col_end + 1) > self.__m_cols_count): 
            self.__m_cols_count = (col_end + 1)
        while len(self.__m_cells) <= row_end:
            self.__m_cells.append(list())
        for r in range(row_end, row_begin - 1, -1):
            while len(self.__m_cells[r]) <= col_end:
                self.__m_cells[r].append(None)
            c = col_begin
            while c <= col_end: 
                if (self.__m_cells[r][c] is not None): 
                    if (r > row_begin): 
                        row_end = (r - 1)
                        break
                    if (c > col_begin): 
                        col_end = (c - 1)
                        break
                    return None
                c += 1
        cel = UnitextTablecell._new581(content, col_begin, col_end, row_begin, row_end)
        r = row_begin
        while r <= row_end: 
            c = col_begin
            while c <= col_end: 
                self.__m_cells[r][c] = cel
                c += 1
            r += 1
        return cel
    
    def get_cell(self, row : int, col : int) -> 'UnitextTablecell':
        """ Получить ячейку таблицы, накрывающую указанную клетку
        
        Args:
            row(int): строка клетки
            col(int): столбец клетки
        
        Returns:
            UnitextTablecell: ячейка (null - отсутствует)
        
        """
        if ((row < 0) or row >= len(self.__m_cells)): 
            return None
        if ((col < 0) or col >= len(self.__m_cells[row])): 
            return None
        return self.__m_cells[row][col]
    
    def get_col_width(self, col : int) -> str:
        """ Получить ширину столбца (если таковая была задана во входном файле)
        
        Args:
            col(int): номер столбца
        
        Returns:
            str: ширина (как она была задана в Html или Doc) или null
        """
        if (col >= 0 and (col < len(self.__m_col_width))): 
            return self.__m_col_width[col]
        else: 
            return None
    
    def set_col_width(self, col : int, val : str) -> None:
        if (col < 0): 
            return
        while col >= len(self.__m_col_width):
            self.__m_col_width.append(None)
        self.__m_col_width[col] = val
    
    @property
    def cols_count(self) -> int:
        """ Количество столбцов
        
        """
        return self.__m_cols_count
    
    @property
    def rows_count(self) -> int:
        """ Количество строк
        
        """
        return len(self.__m_cells)
    
    def clone(self) -> 'UnitextItem':
        res = UnitextTable()
        res._clone_from(self)
        res.__m_cols_count = self.__m_cols_count
        if (self.__m_col_width is not None): 
            res.__m_col_width = list(self.__m_col_width)
        res.width = self.width
        res.hide_borders = self.hide_borders
        res.may_has_error = self.may_has_error
        for r in self.__m_cells: 
            rr = list()
            res.__m_cells.append(rr)
            i = 0
            while i < len(r): 
                if (r[i] is None): 
                    rr.append(None)
                else: 
                    cc = Utils.asObjectOrNull(r[i].clone(), UnitextTablecell)
                    cc.tag = (r[i])
                    cc.parent = (self)
                    rr.append(cc)
                i += 1
        return res
    
    def append_table(self, tab : 'UnitextTable', dont_clone : bool, check_width : bool) -> bool:
        """ Добавить строки второй таблицы (количество колонок должно быть одинаковым, иначе не добавит)
        
        Args:
            tab(UnitextTable): таблица с добавляемыми строками
            dont_clone(bool): при true строки будут не клонироваться, а вставляться напрямую
            check_width(bool): при true будет проверяться ширина колонок, при этом возможно, что в добавляемой таблице одной колонки не будет
        
        Returns:
            bool: удалось ли добавить
        """
        if (tab is None): 
            return False
        if (tab.cols_count > self.cols_count): 
            return False
        if ((tab.cols_count + 1) < self.cols_count): 
            return False
        if (tab.cols_count != self.cols_count and not check_width): 
            return False
        merge_col = -1
        if (check_width): 
            k0 = 0
            k = 0
            first_pass717 = True
            while True:
                if first_pass717: first_pass717 = False
                else: k += 1; k0 += 1
                if (not (k < tab.cols_count)): break
                w1 = self.get_col_width(k0)
                w2 = tab.get_col_width(k)
                if (w1 == w2): 
                    continue
                if (w1.endswith("%")): 
                    w1 = w1[0:0+len(w1) - 1]
                if (w2.endswith("%")): 
                    w2 = w2[0:0+len(w2) - 1]
                n1 = 0
                n2 = 0
                wrapn1584 = RefOutArgWrapper(0)
                inoutres585 = Utils.tryParseInt(w1, wrapn1584)
                wrapn2586 = RefOutArgWrapper(0)
                inoutres587 = Utils.tryParseInt(w2, wrapn2586)
                n1 = wrapn1584.value
                n2 = wrapn2586.value
                if (not inoutres585 or not inoutres587): 
                    return False
                d = n1 - n2
                if (d < 0): 
                    d = (- d)
                if (d < 2): 
                    continue
                if (((k0 + 1) < self.cols_count) and (merge_col < 0)): 
                    w3 = tab.get_col_width(k0 + 1)
                    if (w3 is not None and w3.endswith("%")): 
                        w3 = w3[0:0+len(w3) - 1]
                    n3 = 0
                    wrapn3582 = RefOutArgWrapper(0)
                    inoutres583 = Utils.tryParseInt(Utils.ifNotNull(w3, ""), wrapn3582)
                    n3 = wrapn3582.value
                    if (inoutres583): 
                        d = (n2 - n3)
                        if (d < 0): 
                            d = (- d)
                        if (d < 2): 
                            merge_col = k0
                            k0 += 1
                            continue
                return False
        for r in tab.__m_cells: 
            rr = list()
            self.__m_cells.append(rr)
            i = 0
            while i < len(r): 
                if (r[i] is None): 
                    rr.append(None)
                elif (dont_clone): 
                    rr.append(r[i])
                else: 
                    cc = Utils.asObjectOrNull(r[i].clone(), UnitextTablecell)
                    cc.tag = (r[i])
                    cc.parent = (self)
                    rr.append(cc)
                if (i == merge_col): 
                    rr.append(None)
                i += 1
        return True
    
    def remove_rows(self, ind : int, cou : int) -> None:
        del self.__m_cells[ind:ind+cou]
    
    def _remove_last_column(self) -> None:
        self.__m_cols_count -= 1
        if (self.__m_col_width is not None and len(self.__m_col_width) > self.__m_cols_count): 
            del self.__m_col_width[self.__m_cols_count:self.__m_cols_count+len(self.__m_col_width) - self.__m_cols_count]
        for r in self.__m_cells: 
            if (len(r) > self.__m_cols_count): 
                del r[self.__m_cols_count:self.__m_cols_count+len(r) - self.__m_cols_count]
    
    @property
    def is_inline(self) -> bool:
        return False
    
    @property
    def _inner_tag(self) -> str:
        return "tbl"
    
    def find_by_id(self, id0__ : str) -> 'UnitextItem':
        if (self.id0_ == id0__): 
            return self
        r = 0
        while r < len(self.__m_cells): 
            c = 0
            while c < len(self.__m_cells[r]): 
                if (self.__m_cells[r][c] is not None): 
                    res = self.__m_cells[r][c].find_by_id(id0__)
                    if (res is not None): 
                        return res
                c += 1
            r += 1
        return None
    
    def _find_cell_by_pos(self, plain_pos : int) -> 'UnitextTablecell':
        if (self.__m_map is None and (self.begin_char < self.end_char)): 
            self.__m_map = Utils.newArray((self.end_char + 1) - self.begin_char, None)
            r = 0
            while r < len(self.__m_cells): 
                c = 0
                while c < len(self.__m_cells[r]): 
                    if (self.__m_cells[r][c] is not None): 
                        cel = self.__m_cells[r][c]
                        i = cel.begin_char
                        while i <= cel.end_char: 
                            if (i >= self.begin_char and i <= self.end_char): 
                                self.__m_map[i - self.begin_char] = cel
                            i += 1
                    c += 1
                r += 1
        if (self.__m_map is not None and plain_pos >= self.begin_char and plain_pos <= self.end_char): 
            return self.__m_map[plain_pos - self.begin_char]
        r = 0
        while r < len(self.__m_cells): 
            c = 0
            while c < len(self.__m_cells[r]): 
                if (self.__m_cells[r][c] is not None): 
                    cel = self.__m_cells[r][c]
                    if (cel.begin_char <= plain_pos and plain_pos <= cel.end_char): 
                        return cel
                c += 1
            r += 1
        return None
    
    def _try_append(self, tab : 'UnitextTable') -> bool:
        if (tab.cols_count != self.__m_cols_count): 
            return False
        if (self.page_section_id != tab.page_section_id): 
            return False
        if (tab.rows_count < 1): 
            return False
        k = 0
        for k in range(2):
            r = (0 if k == 0 else len(self.__m_cells) - 1)
            c = 0
            c = 0
            while c < len(self.__m_cells[r]): 
                if (self.__m_cells[r][c] is None): 
                    break
                cel = tab.get_cell(0, c)
                if (cel is None): 
                    break
                if (cel.col_begin != self.__m_cells[r][c].col_begin or cel.col_end != self.__m_cells[r][c].col_end): 
                    break
                c += 1
            if (c >= len(self.__m_cells[r])): 
                break
        else: k = 2
        if (k >= 2): 
            return False
        delt = len(self.__m_cells)
        for r in range(tab.rows_count - 1, -1, -1):
            c = 0
            first_pass718 = True
            while True:
                if first_pass718: first_pass718 = False
                else: c += 1
                if (not (c < tab.cols_count)): break
                cel = tab.get_cell(r, c)
                if (cel is None): 
                    continue
                if (cel.col_begin == c and cel.row_begin == r): 
                    cel.row_begin = cel.row_begin + delt
                    cel.row_end = cel.row_end + delt
        self.__m_cells.extend(tab.__m_cells)
        tab.__m_cells.clear()
        return True
    
    def __str__(self) -> str:
        return "Table [{0}x{1}]{2}".format(self.rows_count, self.cols_count, (" may be error" if self.may_has_error else ""))
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam'=None) -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
        if (pars is None): 
            pars = UnitextItem._m_def_params
        if (pars.table_start is not None): 
            print(pars.table_start, end="", file=res)
        r = 0
        while r < len(self.__m_cells): 
            c = 0
            first_pass719 = True
            while True:
                if first_pass719: first_pass719 = False
                else: c += 1
                if (not (c < len(self.__m_cells[r]))): break
                cel = self.__m_cells[r][c]
                if (cel is None): 
                    continue
                if (r == cel.row_begin and c == cel.col_begin): 
                    cel.get_plaintext(res, pars)
            if (pars is None): 
                print("\r\n{0}".format(chr(7)), end="", file=res, flush=True)
            else: 
                print(Utils.ifNotNull(pars.new_line, ""), end="", file=res)
                print(Utils.ifNotNull(pars.table_row_end, ""), end="", file=res)
            if (pars is not None and pars.max_text_length > 0 and res.tell() > pars.max_text_length): 
                break
            r += 1
        if (pars.table_end is not None): 
            print(pars.table_end, end="", file=res)
        if (pars is not None and pars.set_positions): 
            self.end_char = (res.tell() - 1)
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (not par.call_before(self, res)): 
            return
        print("\r\n<table border=\"{1}\" width=\"{2}\"{0}".format((" style=\"border-color:red\"" if self.may_has_error else ""), (3 if self.may_has_error else (0 if self.hide_borders else 1)), Utils.ifNotNull(self.width, "100%")), end="", file=res, flush=True)
        if (self.id0_ is not None): 
            print(" id=\"{0}\"".format(self.id0_), end="", file=res, flush=True)
            if (par is not None and self.id0_ in par.styles): 
                print(" style=\"{0}\"".format(par.styles[self.id0_]), end="", file=res, flush=True)
            fr = self.get_styled_fragment(-1)
            if (fr is not None and fr.typ != UnitextStyledFragmentType.TABLE): 
                fr = fr.parent
            if ((fr is not None and fr.typ == UnitextStyledFragmentType.TABLE and fr.style_id > 0) and fr.style is not None): 
                print(" style=\"", end="", file=res)
                fr.style.get_html(res)
                print("\"", end="", file=res)
        print(">", end="", file=res)
        if (len(self.__m_col_width) > 0): 
            print("<colgroup>", end="", file=res)
            i = 0
            while i < self.cols_count: 
                print("<col", end="", file=res)
                if ((i < len(self.__m_col_width)) and self.__m_col_width[i] is not None): 
                    print(" width=\"{0}\"".format(self.__m_col_width[i]), end="", file=res, flush=True)
                print("/>", end="", file=res)
                i += 1
            print("</colgroup>", end="", file=res)
        r = 0
        while r < len(self.__m_cells): 
            print("\r\n <tr>", end="", file=res)
            c = 0
            first_pass720 = True
            while True:
                if first_pass720: first_pass720 = False
                else: c += 1
                if (not (c < len(self.__m_cells[r]))): break
                cel = self.__m_cells[r][c]
                if (cel is None): 
                    continue
                if (r == cel.row_begin and c == cel.col_begin): 
                    print("\r\n   ", end="", file=res)
                    cel.get_html(res, par)
            print("\r\n </tr>", end="", file=res)
            if (par is not None and res.tell() > par.max_html_size): 
                break
            r += 1
        print("\r\n</table>\r\n", end="", file=res)
        if (par is not None): 
            par._out_footnotes(res)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("table")
        self._write_xml_attrs(xml0_)
        xml0_.write_attribute_string("rows", str(self.rows_count))
        xml0_.write_attribute_string("columns", str(self.cols_count))
        if (self.width is not None): 
            xml0_.write_attribute_string("width", self.width)
        if (self.hide_borders): 
            xml0_.write_attribute_string("border", "hide")
        i = 0
        while i < len(self.__m_col_width): 
            if (self.__m_col_width[i] is not None): 
                xml0_.write_start_element("col")
                xml0_.write_attribute_string("num", str(i))
                xml0_.write_attribute_string("width", self.__m_col_width[i])
                xml0_.write_end_element()
            i += 1
        r = 0
        while r < len(self.__m_cells): 
            xml0_.write_start_element("row")
            c = 0
            first_pass721 = True
            while True:
                if first_pass721: first_pass721 = False
                else: c += 1
                if (not (c < len(self.__m_cells[r]))): break
                cel = self.__m_cells[r][c]
                if (cel is None): 
                    continue
                if (r == cel.row_begin and c == cel.col_begin): 
                    cel.get_xml(xml0_)
            xml0_.write_end_element()
            r += 1
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        super().from_xml(xml0_)
        rows = 0
        cols = 0
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "rows"): 
                    rows = int(a[1])
                elif (Utils.getXmlAttrLocalName(a) == "columns"): 
                    cols = int(a[1])
                    self.__m_cols_count = cols
                elif (Utils.getXmlAttrLocalName(a) == "width"): 
                    self.width = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "border"): 
                    if (a[1] == "hide"): 
                        self.hide_borders = True
        r = 0
        while r < rows: 
            row = list()
            c = 0
            while c < cols: 
                row.append(None)
                c += 1
            self.__m_cells.append(row)
            r += 1
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "row"): 
                for xx in x: 
                    cel = Utils.asObjectOrNull(UnitextHelper.create_item(xx), UnitextTablecell)
                    if (cel is None): 
                        continue
                    if (cel.col_end >= cols or cel.row_end >= rows): 
                        continue
                    r = cel.row_begin
                    while r <= cel.row_end: 
                        c = cel.col_begin
                        while c <= cel.col_end: 
                            self.__m_cells[r][c] = cel
                            c += 1
                        r += 1
            elif (Utils.getXmlLocalName(x) == "col"): 
                num = 0
                val = None
                if (x.attrib is not None): 
                    for a in x.attrib.items(): 
                        if (Utils.getXmlAttrLocalName(a) == "width"): 
                            val = a[1]
                        elif (Utils.getXmlAttrLocalName(a) == "num"): 
                            wrapnum588 = RefOutArgWrapper(0)
                            Utils.tryParseInt(Utils.ifNotNull(a[1], ""), wrapnum588)
                            num = wrapnum588.value
                if (val is not None): 
                    self.set_col_width(num, val)
    
    def get_all_items(self, res : typing.List['UnitextItem'], lev : int) -> None:
        if (res is not None): 
            res.append(self)
        r = 0
        while r < len(self.__m_cells): 
            c = 0
            first_pass722 = True
            while True:
                if first_pass722: first_pass722 = False
                else: c += 1
                if (not (c < len(self.__m_cells[r]))): break
                cel = self.__m_cells[r][c]
                if (cel is None): 
                    continue
                if (r == cel.row_begin and c == cel.col_begin): 
                    cel.parent = (self)
                    cel.get_all_items(res, lev + 1)
            r += 1
    
    def _add_plain_text_pos(self, d : int) -> None:
        super()._add_plain_text_pos(d)
        r = 0
        while r < len(self.__m_cells): 
            c = 0
            first_pass723 = True
            while True:
                if first_pass723: first_pass723 = False
                else: c += 1
                if (not (c < len(self.__m_cells[r]))): break
                cel = self.__m_cells[r][c]
                if (cel is None): 
                    continue
                if (r == cel.row_begin and c == cel.col_begin): 
                    cel._add_plain_text_pos(d)
            r += 1
    
    def _correct(self, typ : 'LocCorrTyp', data : object) -> None:
        r = 0
        while r < len(self.__m_cells): 
            c = 0
            first_pass724 = True
            while True:
                if first_pass724: first_pass724 = False
                else: c += 1
                if (not (c < len(self.__m_cells[r]))): break
                cel = self.__m_cells[r][c]
                if (cel is None): 
                    continue
                if (r == cel.row_begin and c == cel.col_begin): 
                    cel._correct(typ, data)
            r += 1
    
    def _set_default_text_pos(self, cp : int, res : io.StringIO) -> None:
        self.begin_char = cp.value
        r = 0
        while r < len(self.__m_cells): 
            c = 0
            first_pass725 = True
            while True:
                if first_pass725: first_pass725 = False
                else: c += 1
                if (not (c < len(self.__m_cells[r]))): break
                cel = self.__m_cells[r][c]
                if (cel is None): 
                    continue
                if (r == cel.row_begin and c == cel.col_begin): 
                    cel._set_default_text_pos(cp, res)
                    cel.parent = (self)
            r += 1
        self.end_char = (cp.value - 1)