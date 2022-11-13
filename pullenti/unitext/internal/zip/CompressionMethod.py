# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class CompressionMethod(IntEnum):
    # The kind of compression used for an entry in an archive
    STORED = 0
    DEFLATED = 8
    DEFLATE64 = 9
    BZIP2 = 11
    WINZIPAES = 99
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)