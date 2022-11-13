# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import uuid

class CFHeader:
    
    def __init__(self) -> None:
        self._signature1 = 0
        self._signature2 = 0
        self._clsid = uuid.UUID('{00000000-0000-0000-0000-000000000000}')
        self._minor_version = 0
        self._major_version = 0
        self._byte_order = 0
        self._sector_shift = 0
        self._mini_sector_shift = 0
        self._reserved = None;
        self._directory_sectors_count = 0
        self._fatsectors_count = 0
        self._first_directory_sector_location = 0
        self._transaction_signature_number = 0
        self._mini_stream_cutoff_size = 0
        self._first_minifatsector_location = 0
        self._minifatsectors_count = 0
        self._firstdifatsector_location = 0
        self._difatsectors_count = 0
        self._difat = None;
    
    _default_signature1 = 0xE011CFD0
    
    _default_signature2 = 0xE11AB1A1