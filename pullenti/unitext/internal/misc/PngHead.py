# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.misc.PngChunk import PngChunk

class PngHead(PngChunk):
    
    @property
    def width(self) -> int:
        i0 = 0
        res = self.data[i0]
        res <<= 8
        res |= (self.data[i0 + 1])
        res <<= 8
        res |= (self.data[i0 + 2])
        res <<= 8
        res |= (self.data[i0 + 3])
        return res
    @width.setter
    def width(self, value) -> int:
        i0 = 0
        self.data[i0] = ((((value >> 24)) & 0xFF))
        self.data[i0 + 1] = ((((value >> 16)) & 0xFF))
        self.data[i0 + 2] = ((((value >> 8)) & 0xFF))
        self.data[i0 + 3] = ((((value)) & 0xFF))
        return value
    
    @property
    def height(self) -> int:
        i0 = 4
        res = self.data[i0]
        res <<= 8
        res |= (self.data[i0 + 1])
        res <<= 8
        res |= (self.data[i0 + 2])
        res <<= 8
        res |= (self.data[i0 + 3])
        return res
    @height.setter
    def height(self, value) -> int:
        i0 = 4
        self.data[i0] = ((((value >> 24)) & 0xFF))
        self.data[i0 + 1] = ((((value >> 16)) & 0xFF))
        self.data[i0 + 2] = ((((value >> 8)) & 0xFF))
        self.data[i0 + 3] = ((((value)) & 0xFF))
        return value
    
    @property
    def bit_depth(self) -> int:
        return self.data[8]
    @bit_depth.setter
    def bit_depth(self, value) -> int:
        self.data[8] = value
        return value
    
    @property
    def color_type(self) -> int:
        return self.data[9]
    @color_type.setter
    def color_type(self, value) -> int:
        self.data[9] = value
        return value
    
    @property
    def compression(self) -> int:
        return self.data[10]
    @compression.setter
    def compression(self, value) -> int:
        self.data[10] = value
        return value
    
    @property
    def filter0_(self) -> int:
        return self.data[11]
    @filter0_.setter
    def filter0_(self, value) -> int:
        self.data[11] = value
        return value
    
    @property
    def interlace(self) -> int:
        return self.data[12]
    @interlace.setter
    def interlace(self, value) -> int:
        self.data[12] = value
        return value
    
    def __init__(self) -> None:
        super().__init__("IHDR")
        self.data = Utils.newArrayOfBytes(13, 0)
        self.bit_depth = 8