# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.UnitextTable import UnitextTable

class UnitextGenTable:
    """ Это для поддержки генерации таблиц из модели COLSPAN + ROWSPAN """
    
    def __init__(self) -> None:
        self.cells = list()
        self.m_col_width = list()
        self.may_has_error = False
    
    def convert(self) -> 'UnitextTable':
        res = UnitextTable()
        res.may_has_error = self.may_has_error
        c = 0
        while c < len(self.m_col_width): 
            res.set_col_width(c, self.m_col_width[c])
            c += 1
        r = 0
        while r < len(self.cells): 
            cn = 0
            for cc in self.cells[r]: 
                while True: 
                    if (res.get_cell(r, cn) is None): 
                        break
                    cn += 1
                res.add_cell(r, (r + cc.row_span) - 1, cn, (cn + cc.col_span) - 1, cc.content)
                if (cc.width is not None and cc.col_span <= 1 and res.get_col_width(cn) is None): 
                    if (cc.width is not None): 
                        res.set_col_width(cn, cc.width)
                    elif ((isinstance(cc.content, UnitextTable)) and cc.content.width is not None): 
                        res.set_col_width(cn, cc.content.width)
                cn += cc.col_span
            r += 1
        return res