# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.UnitextTable import UnitextTable
from pullenti.unitext.UnitextExcelSourceInfo import UnitextExcelSourceInfo
from pullenti.unitext.UnitextNewline import UnitextNewline
from pullenti.unitext.UnitextPagebreak import UnitextPagebreak
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.UnitextDocument import UnitextDocument
from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from pullenti.unitext.internal.misc.MyXmlNodeType import MyXmlNodeType
from pullenti.unitext.internal.misc.BorderInfo import BorderInfo
from pullenti.unitext.UnitextContainer import UnitextContainer
from pullenti.unitext.UnitextTablecell import UnitextTablecell

class ExcelHelper:
    
    @staticmethod
    def __get_rows(xml0_ : 'MyXmlReader', shared_strings : typing.List['UnitextItem'], cell_borders : typing.List[tuple], hidden_cols : typing.List[int]) -> typing.List[typing.List['UnitextTablecell']]:
        rows = list()
        cols = 0
        all_cols = 0
        while xml0_.read():
            if (xml0_.node_type != MyXmlNodeType.ELEMENT): 
                continue
            if (xml0_.local_name == "col" or xml0_.local_name == "Column"): 
                if (xml0_.get_attribute("hidden") == "1"): 
                    hidden_cols.append(all_cols)
                all_cols += 1
                continue
            if (Utils.compareStrings(xml0_.local_name, "row", True) == 0): 
                rn = len(rows)
                nnn = 0
                wrapnnn76 = RefOutArgWrapper(0)
                inoutres77 = Utils.tryParseInt(Utils.ifNotNull(xml0_.get_attribute("r"), ""), wrapnnn76)
                nnn = wrapnnn76.value
                if (inoutres77): 
                    rn = (nnn - 1)
                while len(rows) <= rn:
                    rows.append(list())
                row = rows[rn]
                if (xml0_.is_empty_element): 
                    continue
                while xml0_.read():
                    if (xml0_.node_type == MyXmlNodeType.ENDELEMENT and Utils.compareStrings(xml0_.local_name, "row", True) == 0): 
                        break
                    if (xml0_.node_type == MyXmlNodeType.ELEMENT and ((xml0_.local_name == "c" or xml0_.local_name == "Cell"))): 
                        num = -1
                        is_ext = False
                        brd = None
                        val = None
                        v = xml0_.get_attribute("r")
                        if (v is not None and len(v) >= 2): 
                            num = (((ord(v[0])) - (ord('A'))))
                        else: 
                            v = xml0_.get_attribute("ss:Index")
                            if ((v) is not None): 
                                wrapnum65 = RefOutArgWrapper(0)
                                inoutres66 = Utils.tryParseInt(v, wrapnum65)
                                num = wrapnum65.value
                                if (inoutres66): 
                                    num -= 1
                        v = xml0_.get_attribute("t")
                        if (((v)) == "s"): 
                            is_ext = True
                        v = xml0_.get_attribute("s")
                        if ((v) is not None): 
                            wrapbrd67 = RefOutArgWrapper(None)
                            Utils.tryGetValue(cell_borders, v, wrapbrd67)
                            brd = wrapbrd67.value
                        merge_across = -1
                        merge_down = -1
                        v = xml0_.get_attribute("ss:MergeAcross")
                        if ((v) is not None): 
                            wrapmerge_across68 = RefOutArgWrapper(0)
                            Utils.tryParseInt(v, wrapmerge_across68)
                            merge_across = wrapmerge_across68.value
                        v = xml0_.get_attribute("ss:MergeDown")
                        if ((v) is not None): 
                            wrapmerge_down69 = RefOutArgWrapper(0)
                            Utils.tryParseInt(v, wrapmerge_down69)
                            merge_down = wrapmerge_down69.value
                        if (not xml0_.is_empty_element): 
                            while xml0_.read():
                                if (xml0_.node_type == MyXmlNodeType.ELEMENT and xml0_.local_name == "v"): 
                                    if (xml0_.is_empty_element): 
                                        break
                                    if (not xml0_.read()): 
                                        break
                                    if (xml0_.node_type == MyXmlNodeType.TEXT): 
                                        if (not is_ext): 
                                            val = (UnitextPlaintext._new51(xml0_.value))
                                            continue
                                        nu = 0
                                        wrapnu72 = RefOutArgWrapper(0)
                                        inoutres73 = Utils.tryParseInt(xml0_.value, wrapnu72)
                                        nu = wrapnu72.value
                                        if (inoutres73): 
                                            if (nu >= 0 and (nu < len(shared_strings))): 
                                                ss = shared_strings[nu]
                                                if (isinstance(ss, UnitextPlaintext)): 
                                                    val = (UnitextPlaintext._new51(ss.text))
                                                else: 
                                                    val = ss
                                elif (xml0_.node_type == MyXmlNodeType.ELEMENT and xml0_.local_name == "Data"): 
                                    if (not xml0_.is_empty_element): 
                                        xml0_.read()
                                        try: 
                                            if (xml0_.node_type == MyXmlNodeType.TEXT): 
                                                val = (UnitextPlaintext._new51(xml0_.value))
                                        except Exception as eee: 
                                            break
                                if (xml0_.node_type == MyXmlNodeType.ENDELEMENT and ((xml0_.local_name == "c" or xml0_.local_name == "Cell"))): 
                                    break
                        if (num < 0): 
                            num = len(row)
                        if ((num + 1) > cols): 
                            cols = (num + 1)
                        while len(row) <= num:
                            row.append(None)
                        row[num] = UnitextTablecell._new75(num, num, rn, rn, brd)
                        if (val is not None): 
                            row[num].content = val
                        if (merge_across > 0): 
                            row[num].col_end = row[num].col_end + merge_across
                        if (merge_down > 0): 
                            row[num].row_end = row[num].row_end + merge_down
            elif (xml0_.local_name == "mergeCell"): 
                val = xml0_.get_attribute("ref")
                if (val is None): 
                    continue
                ii = val.find(':')
                if (ii < 2): 
                    continue
                v1 = val[0:0+ii]
                v2 = val[ii + 1:]
                if (len(v2) < 2): 
                    continue
                col1 = ((ord(v1[0])) - (ord('A')))
                col2 = ((ord(v2[0])) - (ord('A')))
                if (((col1 < 0) or (col2 < 0) or col1 >= cols) or col2 >= cols): 
                    continue
                row1 = 0
                row2 = 0
                wraprow178 = RefOutArgWrapper(0)
                inoutres79 = Utils.tryParseInt(v1[1:], wraprow178)
                wraprow280 = RefOutArgWrapper(0)
                inoutres81 = Utils.tryParseInt(v2[1:], wraprow280)
                row1 = wraprow178.value
                row2 = wraprow280.value
                if (not inoutres79 or not inoutres81): 
                    continue
                row1 -= 1
                row2 -= 1
                if (((row1 < 0) or (row2 < 0) or row1 >= len(rows)) or row2 >= len(rows)): 
                    continue
                if (col2 > col1): 
                    if ((col1 < len(rows[row1])) and rows[row1][col1] is not None): 
                        rows[row1][col1].col_end = col2
                    jj = row1
                    while jj <= row2: 
                        ii = (col1 + 1)
                        while ii <= col2 and (ii < len(rows[jj])): 
                            rows[jj][ii] = (None)
                            ii += 1
                        jj += 1
                if (row2 > row1): 
                    if ((col1 < len(rows[row1])) and rows[row1][col1] is not None): 
                        rows[row1][col1].row_end = row2
                    jj = row1 + 1
                    while jj <= row2: 
                        kk = col1
                        while kk <= col2: 
                            if (kk < len(rows[jj])): 
                                rows[jj][kk] = (None)
                            kk += 1
                        jj += 1
        return rows
    
    @staticmethod
    def _read_sheet(xml0_ : 'MyXmlReader', shared_strings : typing.List['UnitextItem'], cell_borders : typing.List[tuple], sheet_name : str) -> 'UnitextItem':
        hidden_cols = list()
        rows = ExcelHelper.__get_rows(xml0_, shared_strings, cell_borders, hidden_cols)
        hidden_cols.clear()
        return ExcelHelper.create_table(rows, hidden_cols, sheet_name)
    
    @staticmethod
    def create_table(rows : typing.List[typing.List['UnitextTablecell']], hidden_cols : typing.List[int], sheet_name : str) -> 'UnitextItem':
        cnt = UnitextContainer()
        tab = None
        rnu = 0
        rnu0 = 0
        rempty_max = 0
        all_rows_no_border = True
        rn = 0
        while rn < len(rows): 
            row = list()
            cn = 0
            first_pass633 = True
            while True:
                if first_pass633: first_pass633 = False
                else: cn += 1
                if (not (cn < len(rows[rn]))): break
                if (rows[rn][cn] is not None): 
                    if (cn in hidden_cols): 
                        continue
                    c = rows[rn][cn]
                    row.append(c)
                    if (isinstance(c.tag, BorderInfo)): 
                        if (not c.tag.is_empty): 
                            all_rows_no_border = False
                            break
            if (not all_rows_no_border): 
                break
            rn += 1
        rn = 0
        first_pass634 = True
        while True:
            if first_pass634: first_pass634 = False
            else: rn += 1
            if (not (rn < len(rows))): break
            row = list()
            has_border = False
            has_data = False
            cn = 0
            first_pass635 = True
            while True:
                if first_pass635: first_pass635 = False
                else: cn += 1
                if (not (cn < len(rows[rn]))): break
                if (rows[rn][cn] is not None): 
                    if (cn in hidden_cols): 
                        continue
                    c = rows[rn][cn]
                    row.append(c)
                    if (isinstance(c.tag, BorderInfo)): 
                        if (not c.tag.is_empty): 
                            has_border = True
                    if (c.content is not None): 
                        has_data = True
            if (not has_data): 
                if (rn <= rempty_max): 
                    continue
                if (not has_border or tab is None): 
                    tab = (None)
                    if (len(cnt.children) > 0 and (isinstance(cnt.children[len(cnt.children) - 1], UnitextNewline))): 
                        cnt.children[len(cnt.children) - 1].count += 1
                    else: 
                        cnt.children.append(UnitextNewline())
                    continue
                continue
            if (not has_border and not all_rows_no_border): 
                if ((len(row) < 3) or tab is None): 
                    tab = (None)
                    fi = True
                    cn = 0
                    while cn < len(row): 
                        if (row[cn] is not None and row[cn].content is not None and not cn in hidden_cols): 
                            if (fi): 
                                fi = False
                            else: 
                                cnt.children.append(UnitextPlaintext._new51(" "))
                            cnt.children.append(row[cn].content)
                            row[cn].content.source_info = (UnitextExcelSourceInfo._new83(sheet_name, rn, rn, cn, cn))
                        cn += 1
                    if (len(cnt.children) > 0 and (isinstance(cnt.children[len(cnt.children) - 1], UnitextNewline))): 
                        cnt.children[len(cnt.children) - 1].count += 1
                    else: 
                        cnt.children.append(UnitextNewline())
                    continue
            if (tab is None): 
                cnt.children.append(UnitextNewline())
                tab = UnitextTable()
                cnt.children.append(tab)
                rnu = 0
                rnu0 = rn
                rempty_max = rn
                tab.source_info = (UnitextExcelSourceInfo._new84(sheet_name))
            cn = 0
            while cn < len(row): 
                if (row[cn] is not None and not cn in hidden_cols): 
                    rr = row[cn]
                    if (rr.row_end > rempty_max): 
                        rempty_max = rr.row_end
                    si = UnitextExcelSourceInfo._new83(sheet_name, rr.row_begin, rr.row_end, rr.col_begin, rr.col_end)
                    rr.row_begin = rr.row_begin - rnu0
                    rr.row_end = rr.row_end - rnu0
                    cc = tab.add_cell(rr.row_begin, rr.row_end, rr.col_begin, rr.col_end, rr.content)
                    if (cc is not None and cc.source_info is None): 
                        cc.source_info = (si)
                        if (rr.content is not None): 
                            rr.content.source_info = (si)
                cn += 1
            rnu += 1
        return cnt.optimize(True, None)
    
    @staticmethod
    def _create_doc_for_xml(xml0_ : 'MyXmlReader') -> 'UnitextDocument':
        res = UnitextDocument._new41(FileFormat.XLSX)
        cnt = UnitextContainer()
        borders = dict()
        sheet_name = None
        while xml0_.read():
            if (xml0_.node_type != MyXmlNodeType.ELEMENT): 
                continue
            if (xml0_.local_name == "Worksheet"): 
                if (len(cnt.children) > 0): 
                    cnt.children.append(UnitextPagebreak())
                if (len(xml0_.attributes) > 0): 
                    for a in xml0_.attributes.items(): 
                        name = a[1]
                        sheet_name = name
                        cnt.children.append(UnitextPlaintext._new87(name, "SheetName"))
                        cnt.children.append(UnitextNewline())
                        break
                continue
            if (xml0_.local_name == "Table"): 
                tab = ExcelHelper._read_sheet(xml0_, None, borders, sheet_name)
                if (tab is not None): 
                    cnt.children.append(tab)
        res.content = (cnt)
        res.optimize(False, None)
        return res