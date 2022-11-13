# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

class PendingBuffer:
    # This class is general purpose class for writing data to a buffer.
    # It allows you to write bits as well as bytes
    # Based on DeflaterPending.java
    
    def __init__(self, buffer_size : int=4096) -> None:
        self.__buffer_ = None;
        self.__start = 0
        self.__end = 0
        self.__bits = 0
        self.__m_bit_count = 0
        self.__buffer_ = Utils.newArrayOfBytes(buffer_size, 0)
    
    def reset(self) -> None:
        self.__m_bit_count = 0
        self.__end = self.__m_bit_count
        self.__start = self.__end
    
    def write_byte(self, value : int) -> None:
        self.__buffer_[self.__end] = (value)
        self.__end += 1
    
    def write_short(self, value : int) -> None:
        self.__buffer_[self.__end] = (value)
        self.__end += 1
        self.__buffer_[self.__end] = ((value >> 8))
        self.__end += 1
    
    def write_int(self, value : int) -> None:
        self.__buffer_[self.__end] = (value)
        self.__end += 1
        self.__buffer_[self.__end] = ((value >> 8))
        self.__end += 1
        self.__buffer_[self.__end] = ((value >> 16))
        self.__end += 1
        self.__buffer_[self.__end] = ((value >> 24))
        self.__end += 1
    
    def write_block(self, block : bytearray, offset : int, length : int) -> None:
        Utils.copyArray(block, offset, self.__buffer_, self.__end, length)
        self.__end += length
    
    @property
    def bit_count(self) -> int:
        return self.__m_bit_count
    
    def align_to_byte(self) -> None:
        if (self.__m_bit_count > 0): 
            self.__buffer_[self.__end] = (self.__bits)
            self.__end += 1
            if (self.__m_bit_count > 8): 
                self.__buffer_[self.__end] = (((self.__bits) >> 8))
                self.__end += 1
        self.__bits = (0)
        self.__m_bit_count = 0
    
    def write_bits(self, b : int, count : int) -> None:
        self.__bits |= ((b << self.__m_bit_count))
        self.__m_bit_count += count
        if (self.__m_bit_count >= 16): 
            self.__buffer_[self.__end] = (self.__bits)
            self.__end += 1
            self.__buffer_[self.__end] = (((self.__bits) >> 8))
            self.__end += 1
            self.__bits >>= (16)
            self.__m_bit_count -= 16
    
    def write_shortmsb(self, s : int) -> None:
        self.__buffer_[self.__end] = ((s >> 8))
        self.__end += 1
        self.__buffer_[self.__end] = (s)
        self.__end += 1
    
    @property
    def is_flushed(self) -> bool:
        return self.__end == 0
    
    def flush(self, output : bytearray, offset : int, length : int) -> int:
        if (self.__m_bit_count >= 8): 
            self.__buffer_[self.__end] = (self.__bits)
            self.__end += 1
            self.__bits >>= (8)
            self.__m_bit_count -= 8
        if (length > (self.__end - self.__start)): 
            length = (self.__end - self.__start)
            Utils.copyArray(self.__buffer_, self.__start, output, offset, length)
            self.__start = 0
            self.__end = 0
        else: 
            Utils.copyArray(self.__buffer_, self.__start, output, offset, length)
            self.__start += length
        return length
    
    def to_byte_array(self) -> bytearray:
        result = Utils.newArrayOfBytes(self.__end - self.__start, 0)
        Utils.copyArray(self.__buffer_, self.__start, result, 0, len(result))
        self.__start = 0
        self.__end = 0
        return result