# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import uuid

class CFDirectoryEntry:
    
    def __init__(self) -> None:
        self._name = None;
        self._name_length = 0
        self._object_type = 0
        self._color_flag = 0
        self._left_siblingid = 0
        self._right_siblingid = 0
        self._childid = 0
        self._clsid = uuid.UUID('{00000000-0000-0000-0000-000000000000}')
        self._state_bits = 0
        self._starting_sector_location = 0
        self._stream_size = 0