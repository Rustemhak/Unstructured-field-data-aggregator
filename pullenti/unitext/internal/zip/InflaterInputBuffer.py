# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

class InflaterInputBuffer:
    # An input buffer customised for use by <see cref="InflaterInputStream"/>
    
    def __init__(self, stream : Stream, buffer_size : int=4096) -> None:
        self.__m_raw_length = 0
        self.__m_raw_data = None;
        self.__m_clear_text_length = 0
        self.__m_clear_text = None;
        self.__m_available = 0
        self.__input_stream = None;
        self.__input_stream = stream
        if (buffer_size < 1024): 
            buffer_size = 1024
        self.__m_raw_data = Utils.newArrayOfBytes(buffer_size, 0)
        self.__m_clear_text = self.__m_raw_data
    
    @property
    def raw_length(self) -> int:
        return self.__m_raw_length
    
    @property
    def raw_data(self) -> bytearray:
        return self.__m_raw_data
    
    @property
    def clear_text_length(self) -> int:
        return self.__m_clear_text_length
    
    @property
    def clear_text(self) -> bytearray:
        return self.__m_clear_text
    
    @property
    def available(self) -> int:
        return self.__m_available
    @available.setter
    def available(self, value) -> int:
        self.__m_available = value
        return value
    
    def set_inflater_input(self, inflater : 'Inflater') -> None:
        if (self.__m_available > 0): 
            inflater.set_input_ex(self.__m_clear_text, self.__m_clear_text_length - self.__m_available, self.__m_available)
            self.__m_available = 0
    
    def fill(self) -> None:
        self.__m_raw_length = 0
        to_read = len(self.__m_raw_data)
        while to_read > 0:
            count = self.__input_stream.read(self.__m_raw_data, self.__m_raw_length, to_read)
            if (count <= 0): 
                break
            self.__m_raw_length += count
            to_read -= count
        self.__m_clear_text_length = self.__m_raw_length
        self.__m_available = self.__m_clear_text_length
    
    def read_raw_buffer(self, buffer : bytearray) -> int:
        return self.read_raw_buffer_ex(buffer, 0, len(buffer))
    
    def read_raw_buffer_ex(self, out_buffer : bytearray, offset : int, length : int) -> int:
        if (length < 0): 
            raise Exception("length")
        current_offset = offset
        current_length = length
        while current_length > 0:
            if (self.__m_available <= 0): 
                self.fill()
                if (self.__m_available <= 0): 
                    return 0
            to_copy = min(current_length, self.__m_available)
            Utils.copyArray(self.__m_raw_data, self.__m_raw_length - (self.__m_available), out_buffer, current_offset, to_copy)
            current_offset += to_copy
            current_length -= to_copy
            self.__m_available -= to_copy
        return length
    
    def read_clear_text_buffer(self, out_buffer : bytearray, offset : int, length : int) -> int:
        if (length < 0): 
            raise Exception("length")
        current_offset = offset
        current_length = length
        while current_length > 0:
            if (self.__m_available <= 0): 
                self.fill()
                if (self.__m_available <= 0): 
                    return 0
            to_copy = min(current_length, self.__m_available)
            Utils.copyArray(self.__m_clear_text, self.__m_clear_text_length - (self.__m_available), out_buffer, current_offset, to_copy)
            current_offset += to_copy
            current_length -= to_copy
            self.__m_available -= to_copy
        return length
    
    def read_le_byte(self) -> int:
        if (self.__m_available <= 0): 
            self.fill()
            if (self.__m_available <= 0): 
                raise Utils.newException("EOF in header", None)
        result = self.__m_raw_data[self.__m_raw_length - self.__m_available]
        self.__m_available -= 1
        return result
    
    def read_le_short(self) -> int:
        return self.read_le_byte() | ((self.read_le_byte() << 8))
    
    def read_le_int(self) -> int:
        return self.read_le_short() | ((self.read_le_short() << 16))