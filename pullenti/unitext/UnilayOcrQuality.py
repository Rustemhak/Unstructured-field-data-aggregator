# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class UnilayOcrQuality(IntEnum):
    # Уравень качества распознавания
    UNDEFINED = 0
    VERYBAD = 1
    BAD = 2
    MEDIUM = 3
    GOOD = 4
    FINE = 5
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)