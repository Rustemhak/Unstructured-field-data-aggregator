# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

class OutputWindow:
    # Contains the output from the Inflation process.
    # We need to have a window so that we can refer backwards into the output stream
    # to repeat stuff.<br/>
    
    def __init__(self) -> None:
        self.__window = Utils.newArrayOfBytes(OutputWindow.__window_size, 0)
        self.__window_end = 0
        self.__window_filled = 0
    
    __window_size = 1 << 15
    
    __window_mask = __window_size - 1
    
    def write0_(self, value : int) -> None:
        self.__window_filled += 1
        if ((self.__window_filled - 1) == OutputWindow.__window_size): 
            raise Exception("Window full")
        self.__window[self.__window_end] = (value)
        self.__window_end += 1
        self.__window_end &= OutputWindow.__window_mask
    
    def __slow_repeat(self, rep_start : int, length : int, distance : int) -> None:
        while True:
            if (length > 0): pass
            else: 
                break
            length -= 1
            
            self.__window[self.__window_end] = self.__window[rep_start]
            self.__window_end += 1
            rep_start += 1
            self.__window_end &= OutputWindow.__window_mask
            rep_start &= OutputWindow.__window_mask
    
    def repeat(self, length : int, distance : int) -> None:
        self.__window_filled += length
        if (((self.__window_filled)) > OutputWindow.__window_size): 
            raise Exception("Window full")
        rep_start = ((self.__window_end - distance)) & OutputWindow.__window_mask
        border = OutputWindow.__window_size - length
        if (((rep_start <= border)) and ((self.__window_end < border))): 
            if (length <= distance): 
                Utils.copyArray(self.__window, rep_start, self.__window, self.__window_end, length)
                self.__window_end += length
            else: 
                while True:
                    if (length > 0): pass
                    else: 
                        break
                    length -= 1
                    
                    self.__window[self.__window_end] = self.__window[rep_start]
                    self.__window_end += 1
                    rep_start += 1
        else: 
            self.__slow_repeat(rep_start, length, distance)
    
    def copy_stored(self, input0_ : 'StreamManipulator', length : int) -> int:
        length = min(min(length, OutputWindow.__window_size - self.__window_filled), input0_.available_bytes)
        copied = 0
        tail_len = OutputWindow.__window_size - self.__window_end
        if (length > tail_len): 
            copied = input0_.copy_bytes(self.__window, self.__window_end, tail_len)
            if (copied == tail_len): 
                copied += input0_.copy_bytes(self.__window, 0, length - tail_len)
        else: 
            copied = input0_.copy_bytes(self.__window, self.__window_end, length)
        self.__window_end = (((self.__window_end + copied)) & OutputWindow.__window_mask)
        self.__window_filled += copied
        return copied
    
    def copy_dict(self, dictionary : bytearray, offset : int, length : int) -> None:
        if (dictionary is None): 
            raise Exception("dictionary")
        if (self.__window_filled > 0): 
            raise Exception()
        if (length > OutputWindow.__window_size): 
            offset += (length - OutputWindow.__window_size)
            length = OutputWindow.__window_size
        Utils.copyArray(dictionary, offset, self.__window, 0, length)
        self.__window_end = (length & OutputWindow.__window_mask)
    
    def get_free_space(self) -> int:
        return OutputWindow.__window_size - self.__window_filled
    
    def get_available(self) -> int:
        return self.__window_filled
    
    def copy_output(self, output : bytearray, offset : int, len0_ : int) -> int:
        copy_end = self.__window_end
        if (len0_ > self.__window_filled): 
            len0_ = self.__window_filled
        else: 
            copy_end = ((((self.__window_end - self.__window_filled) + len0_)) & OutputWindow.__window_mask)
        copied = len0_
        tail_len = len0_ - copy_end
        if (tail_len > 0): 
            Utils.copyArray(self.__window, OutputWindow.__window_size - tail_len, output, offset, tail_len)
            offset += tail_len
            len0_ = copy_end
        Utils.copyArray(self.__window, copy_end - len0_, output, offset, len0_)
        self.__window_filled -= copied
        if (self.__window_filled < 0): 
            raise Exception()
        return copied
    
    def reset(self) -> None:
        self.__window_end = 0
        self.__window_filled = self.__window_end