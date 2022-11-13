# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.util.ArchiveHelper import ArchiveHelper
from pullenti.unitext.internal.misc.PngChunk import PngChunk
from pullenti.unitext.internal.misc.PngHead import PngHead

class PngWrapper:
    
    def __init__(self, width : int, height : int, is_gray : bool, color_map : bytearray) -> None:
        self.__m_head = None;
        self.__m_row_size = 0
        self.__m_color_map = None;
        self.__m_data = None;
        self.__m_row = None;
        self.__m_row_pos = 0
        self.__m_chunks = None;
        self.__m_data = list()
        self.__m_row_size = width
        if (not is_gray): 
            if (color_map is None): 
                self.__m_row_size *= 3
        self.__m_row_size += 1
        self.__m_chunks = list()
        self.__m_head = PngHead()
        self.__m_chunks.append(self.__m_head)
        self.__m_head.width = width
        self.__m_head.height = height
        self.__m_head.color_type = ((0 if is_gray else 2))
        if (color_map is not None): 
            self.__m_color_map = color_map
            if (not is_gray): 
                self.__m_head.color_type = 3
                mmm = PngChunk("PLTE")
                mmm.data = color_map
                if (not is_gray and ((len(color_map) % 3)) != 0 and len(color_map) >= 6): 
                    ii = len(color_map) % 3
                    dat = Utils.newArrayOfBytes(len(color_map) - ii, 0)
                    j = 0
                    while j < len(dat): 
                        dat[j] = color_map[j]
                        j += 1
                    mmm.data = dat
                self.__m_chunks.append(mmm)
    
    def begin_row(self) -> None:
        self.__m_row = Utils.newArrayOfBytes(self.__m_row_size, 0)
        self.__m_row_pos = 1
    
    def end_row(self) -> None:
        self.__m_data.append(self.__m_row)
    
    def add_pixel_rgb(self, r : int, g : int, b : int) -> None:
        if ((self.__m_row_pos + 2) >= self.__m_row_size): 
            return
        self.__m_row[self.__m_row_pos] = r
        if (self.__m_head.color_type == (0)): 
            self.__m_row_pos += 1
        else: 
            self.__m_row[self.__m_row_pos + 1] = g
            self.__m_row[self.__m_row_pos + 2] = b
            self.__m_row_pos += 3
    
    def add_pixel_gray(self, gr : int) -> None:
        if (self.__m_row_pos >= self.__m_row_size): 
            return
        self.__m_row[self.__m_row_pos] = gr
        self.__m_row_pos += 1
    
    def add_pixel_index(self, gr : int) -> None:
        if (self.__m_row_pos >= self.__m_row_size): 
            return
        if (self.__m_color_map is not None and self.__m_head.color_type == (0)): 
            i = gr
            if (i >= 0 and (i < len(self.__m_color_map))): 
                self.__m_row[self.__m_row_pos] = self.__m_color_map[i]
                self.__m_row_pos += 1
        else: 
            self.__m_row[self.__m_row_pos] = gr
            self.__m_row_pos += 1
    
    def commit(self) -> None:
        dat = PngChunk("IDAT")
        with MemoryStream() as body: 
            r = 0
            while r < len(self.__m_data): 
                body.write(self.__m_data[r], 0, self.__m_row_size)
                r += 1
            src0 = body.toarray()
            dat.data = ArchiveHelper.compress_zlib(src0)
            self.__m_head.height = len(self.__m_data)
        self.__m_chunks.append(dat)
        self.__m_chunks.append(PngChunk("IEND"))
    
    def get_bytes(self) -> bytearray:
        if (len(self.__m_chunks) < 1): 
            self.commit()
        with MemoryStream() as res: 
            res.writebyte(137)
            res.writebyte(80)
            res.writebyte(78)
            res.writebyte(71)
            res.writebyte(13)
            res.writebyte(10)
            res.writebyte(26)
            res.writebyte(10)
            for ch in self.__m_chunks: 
                ch.write0_(res)
            return res.toarray()
    
    @staticmethod
    def filter_byte(typ : int, encode : bool, x : int, a : int, b : int, c : int) -> int:
        if (typ == 1): 
            return (((x) - (a)) if encode else ((x) + (a)))
        if (typ == 2): 
            return (((x) - (b)) if encode else ((x) + (b)))
        if (typ == 3): 
            i = a
            i += (b)
            i = math.floor(i / 2)
            return (((x) - i) if encode else ((x) + i))
        if (typ == 4): 
            p = a
            p += (b)
            p -= (c)
            pa = p - (a)
            if (pa < 0): 
                pa = (- pa)
            pb = p - (b)
            if (pb < 0): 
                pb = (- pb)
            pc = p - (c)
            if (pc < 0): 
                pc = (- pc)
            i = 0
            if (pa <= pb and pa <= pc): 
                i = (a)
            elif (pb <= pc): 
                i = (b)
            else: 
                i = (c)
            return (((x) - i) if encode else ((x) + i))
        return x