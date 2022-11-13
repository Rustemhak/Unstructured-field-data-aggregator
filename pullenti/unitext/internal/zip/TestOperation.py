# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class TestOperation(IntEnum):
    """ The operation in progress reported by a <see cref="ZipTestResultHandler"/> during testing. """
    INITIALISING = 0
    """ Setting up testing. """
    ENTRYHEADER = 1
    """ Testing an individual entries header """
    ENTRYDATA = 2
    """ Testing an individual entries data """
    ENTRYCOMPLETE = 3
    """ Testing an individual entry has completed. """
    MISCELLANEOUSTESTS = 4
    """ Running miscellaneous tests """
    COMPLETE = 5
    """ Testing is complete """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)