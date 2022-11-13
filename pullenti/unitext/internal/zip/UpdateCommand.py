# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class UpdateCommand(IntEnum):
    # The kind of update to apply.
    COPY = 0
    MODIFY = 1
    ADD = 2
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)