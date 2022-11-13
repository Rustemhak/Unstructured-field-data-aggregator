# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class FtsWidthType(IntEnum):
    NONE = 0
    AUTO = 1
    PERCENT = 2
    DXA = 3
    DXASYS = 19
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)