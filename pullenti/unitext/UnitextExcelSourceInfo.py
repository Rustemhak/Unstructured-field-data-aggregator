# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class UnitextExcelSourceInfo:
    """ Дополнительная информация при выделении из MsExcel """
    
    def __init__(self) -> None:
        self.sheet_name = None;
        self.begin_row = 0
        self.end_row = 0
        self.begin_column = 0
        self.end_column = 0
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.sheet_name is not None): 
            print("'{0}': ".format(self.sheet_name), end="", file=res, flush=True)
        if (self.begin_row == self.end_row): 
            print("Row {0} ".format(self.begin_row), end="", file=res, flush=True)
        else: 
            print("Rows {0}..{1}".format(self.begin_row, self.end_row), end="", file=res, flush=True)
        if (self.begin_column == self.end_column): 
            print("Cell {0}".format(self.begin_column), end="", file=res, flush=True)
        else: 
            print("Cells {0}..{1}".format(self.begin_column, self.end_column), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def _new83(_arg1 : str, _arg2 : int, _arg3 : int, _arg4 : int, _arg5 : int) -> 'UnitextExcelSourceInfo':
        res = UnitextExcelSourceInfo()
        res.sheet_name = _arg1
        res.begin_row = _arg2
        res.end_row = _arg3
        res.begin_column = _arg4
        res.end_column = _arg5
        return res
    
    @staticmethod
    def _new84(_arg1 : str) -> 'UnitextExcelSourceInfo':
        res = UnitextExcelSourceInfo()
        res.sheet_name = _arg1
        return res