# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

class FcCompressedMapping:
    
    __map0_ = None
    
    @staticmethod
    def _get_char(code : int) -> 'char':
        if (code < (0x80)): 
            return chr(code)
        else: 
            value = 0
            wrapvalue481 = RefOutArgWrapper(0)
            inoutres482 = Utils.tryGetValue(FcCompressedMapping.__map0_, code, wrapvalue481)
            value = wrapvalue481.value
            if (inoutres482): 
                return chr(value)
            else: 
                return chr(code)
    
    @staticmethod
    def _get_chars_arr(data : bytearray, offset : int, count : int) -> typing.List['char']:
        result = Utils.newArray(count, None)
        FcCompressedMapping._get_chars(data, offset, count, result, 0)
        return result
    
    @staticmethod
    def _get_chars(data : bytearray, offset : int, count : int, output : typing.List['char'], output_offset : int) -> None:
        i = 0
        while i < count: 
            output[output_offset + i] = FcCompressedMapping._get_char(data[offset + i])
            i += 1
    
    # static constructor for class FcCompressedMapping
    @staticmethod
    def _static_ctor():
        FcCompressedMapping.__map0_ = dict()
        FcCompressedMapping.__map0_[0x82] = 0x201A
        FcCompressedMapping.__map0_[0x83] = 0x0192
        FcCompressedMapping.__map0_[0x84] = 0x201E
        FcCompressedMapping.__map0_[0x85] = 0x2026
        FcCompressedMapping.__map0_[0x86] = 0x2020
        FcCompressedMapping.__map0_[0x87] = 0x2021
        FcCompressedMapping.__map0_[0x88] = 0x02C6
        FcCompressedMapping.__map0_[0x89] = 0x2030
        FcCompressedMapping.__map0_[0x8A] = 0x0160
        FcCompressedMapping.__map0_[0x8B] = 0x2039
        FcCompressedMapping.__map0_[0x8C] = 0x0152
        FcCompressedMapping.__map0_[0x91] = 0x2018
        FcCompressedMapping.__map0_[0x92] = 0x2019
        FcCompressedMapping.__map0_[0x93] = 0x201C
        FcCompressedMapping.__map0_[0x94] = 0x201D
        FcCompressedMapping.__map0_[0x95] = 0x2022
        FcCompressedMapping.__map0_[0x96] = 0x2013
        FcCompressedMapping.__map0_[0x97] = 0x2014
        FcCompressedMapping.__map0_[0x98] = 0x02DC
        FcCompressedMapping.__map0_[0x99] = 0x2122
        FcCompressedMapping.__map0_[0x9A] = 0x0161
        FcCompressedMapping.__map0_[0x9B] = 0x203A
        FcCompressedMapping.__map0_[0x9C] = 0x0153
        FcCompressedMapping.__map0_[0x9F] = 0x0178

FcCompressedMapping._static_ctor()