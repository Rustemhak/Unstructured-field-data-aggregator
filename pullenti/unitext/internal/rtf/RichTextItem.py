# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class RichTextItem:
    
    def __init__(self) -> None:
        self.text = None;
        self.children = list()
        self.owner = None;
        self.tag = None;
        self.begin_char = 0
        self.end_char = 0
        self.is_page_break = False
        self.new_lines = 0
    
    def add_child(self, it : 'RichTextItem') -> None:
        if (self.children is None): 
            self.children = list()
        self.children.append(it)
        it.owner = self
    
    def __str__(self) -> str:
        res = io.StringIO()
        print(type(self)[8:], end="", file=res)
        if (self.text is not None): 
            print(" '{0}'".format(self.text), end="", file=res, flush=True)
        elif (self.children is not None): 
            print(" {0} items".format(len(self.children)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)