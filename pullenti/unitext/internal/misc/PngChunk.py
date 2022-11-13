# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

class PngChunk:
    
    def __init__(self, typ_ : str) -> None:
        self.typ = None;
        self.data = None;
        self.typ = typ_
    
    def __str__(self) -> str:
        return "{0}: {1}bytes".format(self.typ, (0 if self.data is None else len(self.data)))
    
    def write0_(self, str0_ : Stream) -> None:
        self.__write_int(str0_, ((0 if self.data is None else len(self.data))))
        for i in range(4):
            str0_.writebyte(ord(self.typ[i]))
        if (self.data is not None and len(self.data) > 0): 
            str0_.write(self.data, 0, len(self.data))
        crc = self.__calc_crc()
        self.__write_int(str0_, crc)
    
    def __write_int(self, res : Stream, val : int) -> None:
        res.writebyte(((((val) >> 24)) & 0xFF))
        res.writebyte(((((val) >> 16)) & 0xFF))
        res.writebyte(((((val) >> 8)) & 0xFF))
        res.writebyte(((val) & 0xFF))
    
    def __calc_crc(self) -> int:
        crc = 0xFFFFFFFF
        for i in range(4):
            b = ord(self.typ[i])
            crc = ((PngChunk.__m_crc_table[(((crc) ^ (b))) & 0xff]) ^ (((crc) >> 8)))
        if (self.data is not None): 
            n = 0
            while n < len(self.data): 
                crc = ((PngChunk.__m_crc_table[(((crc) ^ (self.data[n]))) & 0xff]) ^ (((crc) >> 8)))
                n += 1
        return (crc) ^ 0xFFFFFFFF
    
    __m_crc_table = None
    
    # static constructor for class PngChunk
    @staticmethod
    def _static_ctor():
        PngChunk.__m_crc_table = Utils.newArray(256, 0)
        for n in range(256):
            c = n
            for k in range(8):
                if ((((c) & 1)) != 0): 
                    c = (0xedb88320 ^ (((c) >> 1)))
                else: 
                    c = ((c) >> 1)
            PngChunk.__m_crc_table[n] = c

PngChunk._static_ctor()