# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class GetPlaintextParam:
    """ Параметры генерации плоского текста функциями GetPlaintext и GetPlaintextString
    Параметры генерации плоского текста
    """
    
    def __init__(self) -> None:
        self.set_positions = True
        self.new_line = "\r\n"
        self.tab = "\t"
        self.page_break = "\f"
        self.table_start = "{0}".format(chr(0x1E))
        self.table_end = "{0}".format(chr(0x1F))
        self.table_cell_end = "{0}".format(chr(7))
        self.table_row_end = "{0}".format(chr(7))
        self.footnotes_template = " (%1)"
        self.hyperlinks_template = None
        self.sup_template = "<%1>"
        self.sub_template = "<%1>"
        self.ignore_shapes = False
        self.max_text_length = 0
        self.use_inner_documents = True
    
    @staticmethod
    def _new2(_arg1 : str, _arg2 : str, _arg3 : str) -> 'GetPlaintextParam':
        res = GetPlaintextParam()
        res.new_line = _arg1
        res.tab = _arg2
        res.page_break = _arg3
        return res
    
    @staticmethod
    def _new339(_arg1 : bool) -> 'GetPlaintextParam':
        res = GetPlaintextParam()
        res.set_positions = _arg1
        return res
    
    @staticmethod
    def _new560(_arg1 : bool, _arg2 : str, _arg3 : str, _arg4 : str, _arg5 : str, _arg6 : str) -> 'GetPlaintextParam':
        res = GetPlaintextParam()
        res.set_positions = _arg1
        res.new_line = _arg2
        res.page_break = _arg3
        res.table_start = _arg4
        res.table_cell_end = _arg5
        res.table_end = _arg6
        return res