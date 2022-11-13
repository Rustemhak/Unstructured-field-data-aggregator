# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.internal.misc.MyZipEntry import MyZipEntry

class MyZipFile(object):
    
    def __init__(self, file_name : str, content : bytearray) -> None:
        self.entries = list()
        self.__m_stream = None;
        self.__m_buf = None;
        if (content is not None): 
            self.__m_stream = (MemoryStream(content))
        else: 
            self.__m_stream = (FileStream(file_name, "rb"))
        self.__m_buf = Utils.newArrayOfBytes(4, 0)
        while True:
            i = self.__m_stream.read(self.__m_buf, 0, 4)
            if ((i != 4 or self.__m_buf[0] != (0x50) or self.__m_buf[1] != (0x4B)) or self.__m_buf[2] != (3) or self.__m_buf[3] != (4)): 
                break
            e0_ = MyZipEntry(self)
            self.__read_short()
            flags = self.__read_short()
            if (((flags & 1)) != 0): 
                e0_.encrypted = True
            e0_.method = self.__read_short()
            self.__read_short()
            self.__read_short()
            crc = self.__read_int()
            e0_.compress_data_size = self.__read_int()
            e0_.uncompress_data_size = self.__read_int()
            flen = self.__read_short()
            extr = self.__read_short()
            fnam = Utils.newArrayOfBytes(flen, 0)
            self.__m_stream.read(fnam, 0, flen)
            try: 
                if (((flags & 0x800)) != 0): 
                    e0_.name = MiscHelper.decode_string_utf8(fnam, 0, -1)
                else: 
                    i = 0
                    while i < len(fnam): 
                        j = fnam[i]
                        if (j >= 0xE0 and j <= 0xEF): 
                            j -= 0x30
                        if (j >= 0x80 and j <= 0xDF): 
                            fnam[i] = ((j + 0x40))
                        if (j == 0xF1): 
                            fnam[i] = (0xB8)
                        if (j == 0xF0): 
                            fnam[i] = (0xA8)
                        i += 1
                    e0_.name = MiscHelper.decode_string1251(fnam, 0, -1)
            except Exception as ex: 
                e0_.name = MiscHelper.decode_string1251(fnam, 0, -1)
            e0_.pos = ((self.__m_stream.position) + extr)
            if (extr > 10 and (e0_.compress_data_size < 0)): 
                ii = self.__read_short()
                if (ii == 1): 
                    self.__read_short()
                    e0_.uncompress_data_size = self.__read_int()
                    self.__read_int()
                    e0_.compress_data_size = self.__read_int()
                    self.__read_int()
            self.__m_stream.position = e0_.pos
            if (e0_.compress_data_size > 0): 
                self.__m_stream.position = self.__m_stream.position + (e0_.compress_data_size)
            if (((flags & 8)) != 0 and e0_.compress_data_size == 0): 
                buf = Utils.newArrayOfBytes(10000, 0)
                while self.__m_stream.position < self.__m_stream.length:
                    p0 = self.__m_stream.position
                    i = self.__m_stream.read(buf, 0, len(buf))
                    if (i < 6): 
                        break
                    j = 0
                    while j < (i - 4): 
                        if (buf[j] == (0x50) and buf[j + 1] == (0x4B)): 
                            if (((buf[j + 2] == (3) and buf[j + 3] == (4))) or ((buf[j + 2] == (1) and buf[j + 3] == (2))) or ((buf[j + 2] == (5) and buf[j + 3] == (6)))): 
                                p0 += j
                                e0_.compress_data_size = (p0 - 12 - e0_.pos)
                                self.__m_stream.position = p0 - 4
                                e0_.uncompress_data_size = self.__read_int()
                                break
                        j += 1
                    if (e0_.compress_data_size > 0): 
                        break
                    self.__m_stream.position = self.__m_stream.position - (4)
            self.entries.append(e0_)
    
    def __read_short(self) -> int:
        i = self.__m_stream.read(self.__m_buf, 0, 2)
        if (i != 2): 
            return -1
        i = (self.__m_buf[1])
        i <<= 8
        i |= (self.__m_buf[0])
        return i
    
    def __read_int(self) -> int:
        i = self.__m_stream.read(self.__m_buf, 0, 4)
        if (i != 4): 
            return -1
        i = (self.__m_buf[3])
        i <<= 8
        i |= (self.__m_buf[2])
        i <<= 8
        i |= (self.__m_buf[1])
        i <<= 8
        i |= (self.__m_buf[0])
        return i
    
    def close(self) -> None:
        if (self.__m_stream is not None): 
            self.__m_stream.close()
    
    def unzip(self, e0_ : 'MyZipEntry') -> bytearray:
        from pullenti.util.ArchiveHelper import ArchiveHelper
        if (e0_.compress_data_size == 0): 
            return None
        if (e0_.method == 8 or e0_.method == 0): 
            pass
        else: 
            return None
        buf = Utils.newArrayOfBytes(e0_.compress_data_size, 0)
        self.__m_stream.position = e0_.pos
        self.__m_stream.read(buf, 0, len(buf))
        if (e0_.method == 0): 
            return buf
        return ArchiveHelper.decompress_deflate(buf)
    def __enter__(self): return self
    def __exit__(self, typ, val, traceback): self.close()