# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import math
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.UnitextItem import UnitextItem
from pullenti.unitext.UnitextTable import UnitextTable
from pullenti.unitext.FileFormat import FileFormat
from pullenti.unitext.internal.uni.UnitextGen import UnitextGen
from pullenti.unitext.UnitextDocument import UnitextDocument

class CsvHelper:
    
    @staticmethod
    def check_delim(text : str) -> 'char':
        delims = [',', ';', ' ', '\t', '|']
        stat = Utils.newArray(len(delims), 0)
        rows = Utils.newArray(len(delims), 0)
        columns = Utils.newArray(len(delims), 0)
        cells = list()
        tmp = io.StringIO()
        i = 0
        while (i < len(delims)) and (i < 100000): 
            rows[i] = 0
            cols = 0
            j = 0
            while j < len(text): 
                cells.clear()
                jj = CsvHelper.read_record(text, j, delims[i], cells, None)
                if (jj < 0): 
                    break
                if (len(cells) > 1): 
                    if (cols == 0): 
                        cols = len(cells)
                    elif (cols == len(cells)): 
                        stat[i] += 1
                    else: 
                        stat[i] -= 1
                    rows[i] += 1
                if (jj > j): 
                    j = jj
                else: 
                    break
            columns[i] = cols
            i += 1
        delim = chr(0)
        bestcou = 0
        i = 0
        while i < len(delims): 
            if (stat[i] > 0 and (stat[i] + 1) >= (math.floor(((rows[i]) * 0.96)))): 
                if (bestcou == 0 or columns[i] > bestcou): 
                    bestcou = columns[i]
                    delim = delims[i]
            i += 1
        return delim
    
    @staticmethod
    def _create(text : str) -> 'UnitextDocument':
        delim = CsvHelper.check_delim(text)
        cells = list()
        tmp = io.StringIO()
        doc = UnitextDocument._new41(FileFormat.CSV)
        tab = UnitextTable()
        gen = UnitextGen()
        doc.content = (tab)
        row = 0
        j = 0
        while j < len(text): 
            cells.clear()
            jj = CsvHelper.read_record(text, j, delim, cells, tmp)
            if (jj < 0): 
                break
            if (len(cells) > 0): 
                i = 0
                first_pass631 = True
                while True:
                    if first_pass631: first_pass631 = False
                    else: i += 1
                    if (not (i < len(cells))): break
                    cel = tab.add_cell(row, row, i, i, None)
                    val = cells[i]
                    if (Utils.isNullOrEmpty(val)): 
                        continue
                    gen.clear_all()
                    gen.append_text(val, False)
                    cel.content = gen.finish(True, None)
                row += 1
            if (jj > j): 
                j = jj
            else: 
                break
        r = 0
        r = 0
        while r < tab.rows_count: 
            cel = tab.get_cell(r, tab.cols_count - 1)
            if (cel is not None and cel.content is not None): 
                break
            r += 1
        if (r >= tab.rows_count): 
            tab._remove_last_column()
        return doc
    
    @staticmethod
    def read_record(text : str, pos : int, delim : 'char', res : typing.List[str], tmp : io.StringIO) -> int:
        if (pos >= len(text)): 
            return -1
        if (tmp is not None): 
            Utils.setLengthStringIO(tmp, 0)
        is_qu = False
        new_cell = False
        len0_ = 0
        i = 0
        i = pos
        first_pass632 = True
        while True:
            if first_pass632: first_pass632 = False
            else: i += 1
            if (not (i < len(text))): break
            ch = text[i]
            if (is_qu): 
                if (ch == '"'): 
                    if (((i + 1) < len(text)) and text[i + 1] == '"'): 
                        if (tmp is not None): 
                            print('"', end="", file=tmp)
                        i += 1
                        len0_ += 1
                        continue
                    is_qu = False
                    continue
                if (tmp is not None): 
                    print(ch, end="", file=tmp)
                len0_ += 1
                continue
            if (ch == delim and (ord(delim)) != 0): 
                if (tmp is not None): 
                    res.append(Utils.toStringStringIO(tmp).strip())
                    Utils.setLengthStringIO(tmp, 0)
                else: 
                    res.append(None)
                new_cell = True
                len0_ = 0
                continue
            if ((ord(ch)) == 0xD or (ord(ch)) == 0xA): 
                i += 1
                if (i < len(text)): 
                    ch = text[i]
                    if ((ord(ch)) == 0xD or (ord(ch)) == 0xA): 
                        i += 1
                break
            if (ch == '"' and len0_ == 0): 
                if (((i + 1) < len(text)) and text[i + 1] == '"'): 
                    i += 1
                else: 
                    is_qu = True
            else: 
                if (tmp is not None): 
                    print(ch, end="", file=tmp)
                len0_ += 1
        if (len0_ > 0 or new_cell): 
            if (tmp is not None): 
                res.append(Utils.toStringStringIO(tmp).strip())
            else: 
                res.append(None)
        return i