# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

class ReadUtils:
    
    _byte_size = 1
    
    _word_size = 2
    
    _dword_size = 4
    
    @staticmethod
    def _read_byte(s : Stream) -> int:
        b = s.readbyte()
        if (b < 0): 
            raise Utils.newException("Unexpected EOF", None)
        return b
    
    @staticmethod
    def _read_byte_ref(s : Stream, read : int) -> int:
        b = ReadUtils._read_byte(s)
        read.value += 1
        return b
    
    __buf = None
    
    @staticmethod
    def _read_int(s : Stream) -> int:
        res = 0
        i = s.read(ReadUtils.__buf, 0, 4)
        if (i < 0): 
            return -1
        if (i < 4): 
            return 0
        for i in range(3, -1, -1):
            res = (((res << 8)) | (ReadUtils.__buf[i]))
        else: i = -1
        return res
    
    @staticmethod
    def _read_short(s : Stream) -> int:
        res = 0
        i = s.read(ReadUtils.__buf, 0, 2)
        if (i < 2): 
            return 0
        for i in range(1, -1, -1):
            res = (((((res) << 8)) | (ReadUtils.__buf[i])))
        else: i = -1
        return res
    
    @staticmethod
    def _read_exact(s : Stream, count : int) -> bytearray:
        data = Utils.newArrayOfBytes(count, 0)
        read = s.read(data, 0, count)
        if (read != count): 
            raise Utils.newException("Unexpected EOF", None)
        return data
    
    @staticmethod
    def _read_exact_ref(s : Stream, count : int, read : int) -> bytearray:
        data = ReadUtils._read_exact(s, count)
        read.value += len(data)
        return data
    
    @staticmethod
    def _skip(s : Stream, count : int) -> None:
        s.seek(count, 1)
    
    # static constructor for class ReadUtils
    @staticmethod
    def _static_ctor():
        ReadUtils.__buf = Utils.newArrayOfBytes(32, 0)

ReadUtils._static_ctor()