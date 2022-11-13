# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class RftItemTyp(IntEnum):
    UNDEFINED = 0
    TEXT = 1
    BRACKETOPEN = 2
    BRACKETCLOSE = 3
    COMMAND = 4
    IMAGE = 5
    PROXY = 6
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)