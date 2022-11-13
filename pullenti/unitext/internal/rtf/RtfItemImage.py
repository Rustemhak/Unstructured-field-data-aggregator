# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.rtf.RtfItem import RtfItem

class RtfItemImage(RtfItem):
    
    def __init__(self) -> None:
        super().__init__()
        self.width = 0
        self.height = 0
    
    @staticmethod
    def _new284(_arg1 : 'RftItemTyp', _arg2 : int, _arg3 : int, _arg4 : str, _arg5 : bytearray) -> 'RtfItemImage':
        res = RtfItemImage()
        res.typ = _arg1
        res.width = _arg2
        res.height = _arg3
        res.text = _arg4
        res.codes = _arg5
        return res