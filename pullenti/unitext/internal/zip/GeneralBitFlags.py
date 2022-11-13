# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class GeneralBitFlags(IntEnum):
    # Defines the contents of the general bit flags field for an archive entry.
    ENCRYPTED = 0x0001
    METHOD = 0x0006
    DESCRIPTOR = 0x0008
    RESERVEDPKWARE4 = 0x0010
    PATCHED = 0x0020
    STRONGENCRYPTION = 0x0040
    UNUSED7 = 0x0080
    UNUSED8 = 0x0100
    UNUSED9 = 0x0200
    UNUSED10 = 0x0400
    UNICODETEXT = 0x0800
    ENHANCEDCOMPRESS = 0x1000
    HEADERMASKED = 0x2000
    RESERVEDPKWARE14 = 0x4000
    RESERVEDPKWARE15 = 0x8000
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)