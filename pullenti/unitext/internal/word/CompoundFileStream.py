# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

class CompoundFileStream(Stream):
    # Base stream for retrival data from a Compound File.
    
    @property
    def _storage(self) -> 'CompoundFileStorage':
        return self.__m_storage
    
    @property
    def _system(self) -> 'CompoundFileSystem':
        return self._storage._system
    
    @property
    def _page_size(self) -> int:
        return self.__m_page_size
    
    def __init__(self, storage : 'CompoundFileStorage', page_size : int) -> None:
        super().__init__()
        self.__m_storage = None;
        self.__m_position = 0
        self.__m_length = 0
        self.__m_page_size = 0
        self.__m_page = None
        self.__m_page_index = -1
        self.__m_storage = storage
        self.__m_position = 0
        self.__m_length = storage.length
        self.__m_page_size = page_size
    
    @property
    def can_read(self) -> bool:
        return True
    
    @property
    def can_seek(self) -> bool:
        return True
    
    @property
    def can_write(self) -> bool:
        return False
    
    def flush(self) -> None:
        pass
    
    @property
    def length(self) -> int:
        return self.__m_length
    
    @property
    def position(self) -> int:
        return self.__m_position
    @position.setter
    def position(self, value) -> int:
        self.seek(value, 0)
        return value
    
    def read(self, buffer : bytearray, offset : int, count : int) -> int:
        if (count <= 0): 
            return count
        if (self.__m_position >= self.__m_length): 
            return 0
        can_read_ = ((self.__m_length - self.__m_position) if count > ((self.__m_length - self.__m_position)) else count)
        try: 
            page_start_position = self.__m_page_size * self.__m_page_index
            page_end_position = page_start_position
            if (self.__m_page is not None): 
                page_end_position += len(self.__m_page)
            if ((self.__m_position < page_start_position) or (self.__m_position + can_read_) > page_end_position): 
                cached_page = self.__m_page
                cached_page_index = self.__m_page_index
                start_page_index = (math.floor(self.__m_position / self.__m_page_size))
                last_page_index = (math.floor((((self.__m_position + can_read_) - 1)) / self.__m_page_size))
                if (start_page_index != cached_page_index): 
                    self.__m_page = self._get_page_data(start_page_index)
                    self.__m_page_index = start_page_index
                start_page_offset = (self.__m_position - (start_page_index * self.__m_page_size))
                start_page_tail = len(self.__m_page) - start_page_offset
                if (start_page_tail >= can_read_): 
                    Utils.copyArray(self.__m_page, start_page_offset, buffer, offset, can_read_)
                    self.__m_position += can_read_
                else: 
                    Utils.copyArray(self.__m_page, start_page_offset, buffer, offset, start_page_tail)
                    offset += start_page_tail
                    self.__m_position += start_page_tail
                    left_to_read = can_read_ - start_page_tail
                    i = start_page_index + 1
                    while i < last_page_index: 
                        if (cached_page_index == i): 
                            self.__m_page = cached_page
                            self.__m_page_index = cached_page_index
                        else: 
                            self.__m_page = self._get_page_data(i)
                            self.__m_page_index = i
                        Utils.copyArray(self.__m_page, 0, buffer, offset, len(self.__m_page))
                        offset += len(self.__m_page)
                        self.__m_position += len(self.__m_page)
                        left_to_read -= len(self.__m_page)
                        i += 1
                    if (cached_page_index == last_page_index): 
                        self.__m_page = cached_page
                        self.__m_page_index = cached_page_index
                    else: 
                        self.__m_page = self._get_page_data(last_page_index)
                        self.__m_page_index = last_page_index
                    Utils.copyArray(self.__m_page, 0, buffer, offset, left_to_read)
                    self.__m_position += left_to_read
            else: 
                Utils.copyArray(self.__m_page, (self.__m_position - page_start_position), buffer, offset, can_read_)
                self.__m_position += can_read_
        except Exception as ex: 
            return -1
        return can_read_
    
    def _get_page_data(self, page_index : int) -> bytearray:
        return None
    
    def seek(self, offset : int, origin : int) -> int:
        swichVal = origin
        if (swichVal == 0): 
            self.__m_position = (offset)
        elif (swichVal == 1): 
            self.__m_position += (offset)
        elif (swichVal == 2): 
            self.__m_position = ((self.length + offset))
        return self.__m_position
    
    def set_length(self, value : int) -> None:
        pass
    
    def write(self, buffer : bytearray, offset : int, count : int) -> None:
        pass
    
    def _dispose(self, disposing : bool) -> None:
        super()._dispose(disposing)
        if (disposing): 
            self.__m_storage = (None)
            self.__m_page = (None)