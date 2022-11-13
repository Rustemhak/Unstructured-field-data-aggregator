# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.UnitextDocblock import UnitextDocblock

class HtmlSectionItem:
    
    def __init__(self) -> None:
        self.head = list()
        self.tail = list()
        self.has_body = False
        self.stack = list()
    
    def generate(self, hg : 'UnitextHtmlGen') -> 'UnitextItem':
        doc = UnitextDocblock._new32("Document")
        self.stack[0]._generate(doc, 0, hg)
        return doc