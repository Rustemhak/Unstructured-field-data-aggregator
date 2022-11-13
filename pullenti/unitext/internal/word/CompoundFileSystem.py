# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import datetime
import gc
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.word.CompoundFileObjectType import CompoundFileObjectType
from pullenti.unitext.internal.word.FATSectorIds import FATSectorIds
from pullenti.unitext.internal.word.ReaderUtils import ReaderUtils
from pullenti.unitext.internal.word.CompoundFileStorage import CompoundFileStorage

class CompoundFileSystem(object):
    # File System that base on Compound File structure. The class
    # provides methods read the structure and the data of the
    # Compound File.
    # See Microsoft's [MS-CFB] "Compound File Binary File Format"
    # reference for more details.
    
    @property
    def base_stream(self) -> Stream:
        return self.__m_base_stream
    
    @property
    def _header(self) -> 'CFHeader':
        return self.__m_header
    
    @property
    def _is_version3(self) -> bool:
        return self._header._major_version == (3)
    
    @property
    def created(self) -> datetime.datetime:
        return (datetime.datetime.min if Utils.isNullOrEmpty(self.__m_filename) else datetime.datetime.min)
    
    @property
    def modified(self) -> datetime.datetime:
        return (datetime.datetime.min if Utils.isNullOrEmpty(self.__m_filename) else datetime.datetime.min)
    
    def __init__(self, filename : str, data : bytearray=None, stream : Stream=None) -> None:
        self.__m_filename = None;
        self.__m_base_stream = None;
        self.__m_disposed = False
        self.__m_root_storage = None
        self.__m_header = None;
        if (stream is not None): 
            self.__m_base_stream = stream
        elif (data is not None): 
            self.__m_base_stream = (MemoryStream(data))
        else: 
            self.__m_filename = filename
            self.__m_base_stream = (FileStream(filename, "rb"))
        self.__initialize()
    
    def finalize(self) -> None:
        self._dispose(False)
    
    def __initialize(self) -> None:
        self.__m_header = ReaderUtils._read_header(self.base_stream)
        ReaderUtils._validate_header(self.__m_header)
    
    def close(self) -> None:
        try: 
            self._dispose(True)
        except Exception as ex: 
            pass
        
    
    def _dispose(self, disposing : bool) -> None:
        if (self.__m_disposed): 
            return
        self.__m_disposed = True
        self.__m_base_stream.close()
    
    def get_root_storage(self) -> 'CompoundFileStorage':
        if (self.__m_root_storage is None): 
            root_directory_streamid = 0
            self.__m_root_storage = CompoundFileStorage(self, root_directory_streamid, Utils.newArray(0, 0))
            self.__validate_root_storage()
        return self.__m_root_storage
    
    def __validate_root_storage(self) -> None:
        if (self.__m_root_storage.object_type != CompoundFileObjectType.ROOT): 
            self.__m_root_storage = (None)
            raise Utils.newException("Invalid root storage", None)
    
    def _get_sector_offset(self, sector_number : int) -> int:
        return ((((sector_number) + 1)) << self.__m_header._sector_shift)
    
    def _get_sector_size(self) -> int:
        return 1 << self.__m_header._sector_shift
    
    def _get_mini_sector_size(self) -> int:
        return 1 << self.__m_header._mini_sector_shift
    
    def _get_mini_sector_offset(self, sector_number : int) -> int:
        return self._to_physical_stream_offset(self.get_root_storage()._entry._starting_sector_location, ((sector_number) << self.__m_header._mini_sector_shift))
    
    def _to_physical_stream_offset(self, first_sector : int, offset_within_logical_stream : int) -> int:
        sector_index = (offset_within_logical_stream >> self.__m_header._sector_shift)
        if (sector_index == 0): 
            return self._get_sector_offset(first_sector) + offset_within_logical_stream
        sector = self._get_stream_next_sector(first_sector, sector_index)
        mask = ((1 << self._header._sector_shift)) - 1
        return self._get_sector_offset(sector) + ((offset_within_logical_stream & mask))
    
    def _get_stream_next_sector(self, sector : int, iterations : int) -> int:
        i = 0
        while i < iterations: 
            fat_sector_index = (((sector) >> (((self._header._sector_shift) - 2))))
            mask = ((1 << (((self._header._sector_shift) - 2)))) - 1
            entry_index = ((sector) & mask)
            fat_sector = self.__getfatsector(fat_sector_index)
            sector = ReaderUtils._read_uint32(self.base_stream, self._get_sector_offset(fat_sector) + ((entry_index << 2)))
            if (sector > FATSectorIds._maxregsect): 
                raise Utils.newException("Short chain", None)
            i += 1
        return sector
    
    def _get_mini_stream_next_sector(self, sector : int, iterations : int) -> int:
        i = 0
        while i < iterations: 
            entry_offset = (sector) << 2
            if ((entry_offset >> self._header._sector_shift) >= (self._header._minifatsectors_count)): 
                raise Utils.newException("Mini FAT sector index out of range", None)
            offset = self._to_physical_stream_offset(self._header._first_minifatsector_location, entry_offset)
            sector = ReaderUtils._read_uint32(self.base_stream, offset)
            if (sector > FATSectorIds._maxregsect): 
                raise Utils.newException("Short chain", None)
            i += 1
        return sector
    
    def __getfatsector(self, fat_sector_index : int) -> int:
        if (fat_sector_index < ReaderUtils._headerdifatsectors_count): 
            return self._header._difat[fat_sector_index]
        else: 
            items_per_page = ((self._get_sector_size() >> 2)) - 1
            page_index = math.floor(((fat_sector_index - ReaderUtils._headerdifatsectors_count)) / items_per_page)
            if (page_index >= (self._header._fatsectors_count)): 
                raise Utils.newException("FAT sector index out of range", None)
            current_sector = self._header._firstdifatsector_location
            i = 0
            while i < page_index: 
                offset = self._get_sector_offset(current_sector) + ((items_per_page << 2))
                current_sector = ReaderUtils._read_uint32(self.base_stream, offset)
                i += 1
            entry_index = ((fat_sector_index - ReaderUtils._headerdifatsectors_count)) % items_per_page
            return ReaderUtils._read_uint32(self.base_stream, self._get_sector_offset(current_sector) + ((entry_index << 2)))
    def __enter__(self): return self
    def __exit__(self, typ, val, traceback): self.close()