# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

class StreamManipulator:
    # This class allows us to retrieve a specified number of bits from
    # the input buffer, as well as copy big byte blocks.
    # It uses an int buffer to store up to 31 bits for direct
    # manipulation.  This guarantees that we can get at least 16 bits,
    # but we only need at most 15, so this is all safe.
    # There are some optimizations in this class, for example, you must
    # never peek more than 8 bits more than needed, and you must first
    # peek bits before you may drop them.  This is not a general purpose
    # class but optimized for the behaviour of the Inflater.
    
    def __init__(self) -> None:
        self.__window_ = None;
        self.__window_start_ = 0
        self.__window_end_ = 0
        self.__buffer_ = 0
        self.__bits_in_buffer_ = 0
    
    def peek_bits(self, bit_count : int) -> int:
        if (self.__bits_in_buffer_ < bit_count): 
            if (self.__window_start_ == self.__window_end_): 
                return -1
            self.__buffer_ |= ((((((self.__window_[self.__window_start_]) & 0xff) | (((self.__window_[self.__window_start_ + 1]) & 0xff)) << 8)) << self.__bits_in_buffer_))
            self.__window_start_ += 2
            self.__bits_in_buffer_ += 16
        return ((self.__buffer_) & ((((1 << bit_count)) - 1)))
    
    def drop_bits(self, bit_count : int) -> None:
        self.__buffer_ >>= (bit_count)
        self.__bits_in_buffer_ -= bit_count
    
    def get_bits(self, bit_count : int) -> int:
        bits = self.peek_bits(bit_count)
        if (bits >= 0): 
            self.drop_bits(bit_count)
        return bits
    
    @property
    def available_bits(self) -> int:
        return self.__bits_in_buffer_
    
    @property
    def available_bytes(self) -> int:
        return (self.__window_end_ - self.__window_start_) + ((self.__bits_in_buffer_ >> 3))
    
    def skip_to_byte_boundary(self) -> None:
        self.__buffer_ >>= ((self.__bits_in_buffer_ & 7))
        self.__bits_in_buffer_ &= (~ 7)
    
    @property
    def is_needing_input(self) -> bool:
        return self.__window_start_ == self.__window_end_
    
    def copy_bytes(self, output : bytearray, offset : int, length : int) -> int:
        if (length < 0): 
            raise Exception("length")
        if (((self.__bits_in_buffer_ & 7)) != 0): 
            raise Exception("Bit buffer is not byte aligned!")
        count = 0
        while ((self.__bits_in_buffer_ > 0)) and ((length > 0)):
            output[offset] = (self.__buffer_)
            offset += 1
            self.__buffer_ >>= (8)
            self.__bits_in_buffer_ -= 8
            length -= 1
            count += 1
        if (length == 0): 
            return count
        avail = self.__window_end_ - self.__window_start_
        if (length > avail): 
            length = avail
        Utils.copyArray(self.__window_, self.__window_start_, output, offset, length)
        self.__window_start_ += length
        if (((((self.__window_start_ - self.__window_end_)) & 1)) != 0): 
            self.__buffer_ = (((self.__window_[self.__window_start_]) & 0xff))
            self.__window_start_ += 1
            self.__bits_in_buffer_ = 8
        return count + length
    
    def reset(self) -> None:
        self.__buffer_ = (0)
        self.__bits_in_buffer_ = 0
        self.__window_end_ = self.__bits_in_buffer_
        self.__window_start_ = self.__window_end_
    
    def set_input(self, buffer : bytearray, offset : int, count : int) -> None:
        if (buffer is None): 
            raise Exception("buffer")
        if (offset < 0): 
            raise Exception("offset", "Cannot be negative")
        if (count < 0): 
            raise Exception("count", "Cannot be negative")
        if (self.__window_start_ < self.__window_end_): 
            raise Exception("Old input was not completely processed")
        end = offset + count
        if (((offset > end)) or ((end > len(buffer)))): 
            raise Exception("count")
        if (((count & 1)) != 0): 
            self.__buffer_ |= (((((buffer[offset]) & 0xff)) << self.__bits_in_buffer_))
            offset += 1
            self.__bits_in_buffer_ += 8
        self.__window_ = buffer
        self.__window_start_ = offset
        self.__window_end_ = end