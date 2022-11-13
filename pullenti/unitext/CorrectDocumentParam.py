# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class CorrectDocumentParam:
    """ Параметры корректировки (оптимизации) представления в параметрах создания CreateDocumentParam.CorrextParams.
    Параметры корректировки документа
    """
    
    def __init__(self) -> None:
        self.remove_page_break_numeration = True
        self.remove_false_new_lines = True
        self.restore_text_footnotes = True
        self.restore_tables = True
        self.replace_nbsp_by_space = True
        self.optimize_structure = True
    
    @property
    def choose_all(self) -> bool:
        """ Установить все опции в true или false. """
        return ((self.remove_page_break_numeration & self.remove_false_new_lines & self.restore_text_footnotes) & self.restore_tables & self.replace_nbsp_by_space) & self.optimize_structure
    @choose_all.setter
    def choose_all(self, value) -> bool:
        self.remove_page_break_numeration = value
        self.remove_false_new_lines = value
        self.restore_text_footnotes = value
        self.restore_tables = value
        self.replace_nbsp_by_space = value
        self.optimize_structure = value
        return value