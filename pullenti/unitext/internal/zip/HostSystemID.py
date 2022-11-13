# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class HostSystemID(IntEnum):
    # Defines known values for the <see cref="HostSystemID"/> property.
    MSDOS = 0
    AMIGA = 1
    OPENVMS = 2
    UNIX = 3
    VMCMS = 4
    ATARIST = 5
    OS2 = 6
    MACINTOSH = 7
    ZSYSTEM = 8
    CPM = 9
    WINDOWSNT = 10
    MVS = 11
    VSE = 12
    ACORNRISC = 13
    VFAT = 14
    ALTERNATEMVS = 15
    BEOS = 16
    TANDEM = 17
    OS400 = 18
    OSX = 19
    WINZIPAES = 99
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)