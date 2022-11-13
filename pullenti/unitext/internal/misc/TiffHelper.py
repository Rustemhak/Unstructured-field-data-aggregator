# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.util.MiscHelper import MiscHelper
from pullenti.unitext.UnitextDocument import UnitextDocument
from pullenti.unitext.UnilayPage import UnilayPage
from pullenti.unitext.FileFormat import FileFormat

class TiffHelper:
    
    class CCITT_Types(IntEnum):
        G3_1D = 2
        G3_2D = 3
        G4 = 4
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    class Tiff:
        """ Работа с TIFF-документами """
        
        @property
        def ismdi(self) -> bool:
            return self.__m_mdi
        
        def __init__(self, stream_ : Stream) -> None:
            self.__m_buf = Utils.newArrayOfBytes(32, 0)
            self.__m_msb = False
            self.__m_mdi = False
            self.__m_ifd_offset = list()
            self.__m_stream = None
            self.__fbuf2 = Utils.newArrayOfBytes(16, 0)
            self.stream = stream_
        
        @property
        def stream(self) -> Stream:
            return self.__m_stream
        @stream.setter
        def stream(self, value) -> Stream:
            if (value is None): 
                return value
            self.__m_stream = value
            self.__m_ifd_offset.clear()
            self.__m_stream.position = 0
            self.__m_stream.read(self.__m_buf, 0, 2)
            self.__m_mdi = False
            self.__m_msb = False
            if (self.__m_buf[0] == (0x49) and self.__m_buf[1] == (0x49)): 
                self.__m_msb = False
            elif (self.__m_buf[0] == (0x4D) and self.__m_buf[1] == (0x4D)): 
                self.__m_msb = True
            elif (self.__m_buf[0] == (0x45) and self.__m_buf[1] == (0x50)): 
                self.__m_mdi = True
            else: 
                self.__m_stream = (None)
                return value
            i = self.__read_int(2)
            while True:
                i = self.__read_int(4)
                if (i <= 0): 
                    break
                self.__m_ifd_offset.append(i)
                self.__m_stream.position = i
                cou = self.__read_int(2)
                self.__m_stream.position = i + 2 + ((cou * 12))
            return value
        
        @property
        def pages_count(self) -> int:
            """ Число страниц (если 0, то это не TIFF) """
            return len(self.__m_ifd_offset)
        
        def store(self, page_index : int, fout : Stream) -> None:
            """ Сохранение страницы в отдельном файле
            
            Args:
                page_index(int): 
                FileName: 
            """
            if ((page_index < 0) or page_index >= len(self.__m_ifd_offset)): 
                raise Utils.newException("Page index error", None)
            if (self.__m_msb): 
                self.__m_buf[1] = 0x4D
                self.__m_buf[0] = self.__m_buf[1]
            else: 
                self.__m_buf[1] = 0x49
                self.__m_buf[0] = self.__m_buf[1]
            fout.write(self.__m_buf, 0, 2)
            self.__write_int(fout, 0x2A, 2)
            self.__write_int(fout, 8, 4)
            baseoff = self.__m_ifd_offset[page_index]
            self.__m_stream.position = baseoff
            i = 0
            j = 0
            ii = 0
            dircount = self.__read_int(2)
            outpos = (8 + 2 + (12 * dircount)) + 4
            stripoffpos = 0
            stripoffitemsize = 0
            direct_data = False
            direct_data_pos = 0
            direct_data_len = 0
            strip_pos = list()
            strip_len = list()
            self.__write_int(fout, dircount, 2)
            i = 0
            first_pass636 = True
            while True:
                if first_pass636: first_pass636 = False
                else: i += 1
                if (not (i < dircount)): break
                self.__m_stream.position = baseoff + (2) + (i * 12)
                tag = self.__read_int(2)
                typ = self.__read_int(2)
                cou = self.__read_int(4)
                dsp = self.__read_int(4)
                itemsize = 1
                fout.position = 8 + 2 + (ii * 12)
                ii += 1
                self.__write_int(fout, tag, 2)
                self.__write_int(fout, typ, 2)
                self.__write_int(fout, cou, 4)
                swichVal = typ
                if (swichVal == 3): 
                    itemsize = 2
                elif (swichVal == 4): 
                    itemsize = 4
                elif (swichVal == 5): 
                    itemsize = 8
                elif (swichVal == 8): 
                    itemsize = 2
                elif (swichVal == 9): 
                    itemsize = 4
                elif (swichVal == 10): 
                    itemsize = 8
                len0_ = itemsize * cou
                if (len0_ <= 4 and tag != 0x111): 
                    self.__write_int(fout, dsp, 4)
                    if (tag == 0x117): 
                        direct_data_len = dsp
                    continue
                if (tag == 0x111): 
                    stripoffpos = outpos
                    stripoffitemsize = itemsize
                    if (cou == 1): 
                        direct_data = True
                        direct_data_pos = dsp
                        stripoffpos = (fout.position)
                        self.__write_int(fout, dsp, 4)
                        continue
                    else: 
                        self.__m_stream.position = dsp
                        j = 0
                        while j < cou: 
                            strip_pos.append(self.__read_int(itemsize))
                            j += 1
                        self.__m_stream.position = dsp
                elif (tag == 0x117): 
                    if (cou != len(strip_pos)): 
                        fout.close()
                        raise Utils.newException("StripOffsetCount != StripCount", None)
                    self.__m_stream.position = dsp
                    j = 0
                    while j < cou: 
                        strip_len.append(self.__read_int(itemsize))
                        j += 1
                    self.__m_stream.position = dsp
                self.__read_buf(dsp, len0_)
                self.__write_int(fout, outpos, 4)
                fout.position = outpos
                fout.write(self.__m_buf, 0, len0_)
                outpos += len0_
                if (((outpos & 1)) == 1): 
                    outpos += 1
                    self.__write_int(fout, 0, 1)
            fout.position = 8 + 2 + (ii * 12)
            self.__write_int(fout, 0, 4)
            fout.position = 8
            self.__write_int(fout, ii, 2)
            if (direct_data): 
                self.__read_buf(direct_data_pos, direct_data_len)
                fout.position = stripoffpos
                self.__write_int(fout, outpos, 4)
                fout.position = outpos
                fout.write(self.__m_buf, 0, direct_data_len)
                outpos += direct_data_len
            else: 
                fout.position = outpos
                i = 0
                while i < len(strip_pos): 
                    self.__read_buf(strip_pos[i], strip_len[i])
                    strip_pos[i] = outpos
                    fout.write(self.__m_buf, 0, strip_len[i])
                    outpos += strip_len[i]
                    i += 1
                fout.position = stripoffpos
                i = 0
                while i < len(strip_pos): 
                    self.__write_int(fout, strip_pos[i], stripoffitemsize)
                    i += 1
        
        def get_page_text(self, page_index : int) -> str:
            """ Извлечение текста, сформированного MODI (хранится в теге 932Fh)
            
            Args:
                page_index(int): номер страницы
            
            Returns:
                str: текст (null при ошибке или отсутствии)
            """
            from pullenti.util.MiscHelper import MiscHelper
            if ((page_index < 0) or page_index >= len(self.__m_ifd_offset)): 
                raise Utils.newException("Page index error", None)
            baseoff = self.__m_ifd_offset[page_index]
            self.__m_stream.position = baseoff
            i = 0
            dircount = self.__read_int(2)
            i = 0
            first_pass637 = True
            while True:
                if first_pass637: first_pass637 = False
                else: i += 1
                if (not (i < dircount)): break
                self.__m_stream.position = baseoff + (2) + (i * 12)
                tag = self.__read_int(2)
                typ = self.__read_int(2)
                cou = self.__read_int(4)
                dsp = self.__read_int(4)
                if (tag != 0x932F): 
                    continue
                self.__m_stream.position = dsp
                if (self.__read_int(2) != 1): 
                    return None
                cou = self.__read_int(4)
                if (cou < 1): 
                    return None
                buf = Utils.newArrayOfBytes(cou, 0)
                self.__m_stream.read(buf, 0, cou)
                blen = len(buf)
                if (blen > 0 and buf[blen - 1] == (0)): 
                    blen -= 1
                if (blen == 0): 
                    return None
                return MiscHelper.decode_string_utf8(buf, 0, blen)
            return None
        
        @property
        def has_text(self) -> bool:
            """ Проверка, имеет ли файл встроенные MODI-тексты """
            p = 0
            while p < len(self.__m_ifd_offset): 
                baseoff = self.__m_ifd_offset[p]
                self.__m_stream.position = baseoff
                i = 0
                dircount = self.__read_int(2)
                i = 0
                while i < dircount: 
                    self.__m_stream.position = baseoff + (2) + (i * 12)
                    tag = self.__read_int(2)
                    typ = self.__read_int(2)
                    cou = self.__read_int(4)
                    dsp = self.__read_int(4)
                    if (tag == 0x932F): 
                        return True
                    i += 1
                p += 1
            return False
        
        def get_data_info(self, page_index : int, data_start_pos : int, data_length : int, width : int, height : int, ccitt_typ : 'CCITT_Types', page_number : int) -> bool:
            """ Это извлечение информации о самой картинке вместе с положением данных во входном потоке
            - используется для выделения CCITT-данных для PDF FaxDecode
            
            Args:
                page_index(int): 
                data_start_pos(int): 
                data_length(int): 
                width(int): 
                height(int): 
            
            """
            data_length.value = 0
            data_start_pos.value = data_length.value
            page_number.value = 0
            height.value = 0
            width.value = height.value
            ccitt_typ.value = TiffHelper.CCITT_Types.G3_1D
            if ((page_index < 0) or page_index >= len(self.__m_ifd_offset)): 
                raise Utils.newException("Page index error", None)
            baseoff = self.__m_ifd_offset[page_index]
            self.__m_stream.position = baseoff
            i = 0
            dircount = self.__read_int(2)
            i = 0
            while i < dircount: 
                self.__m_stream.position = baseoff + (2) + (i * 12)
                tag = self.__read_int(2)
                typ = self.__read_int(2)
                cou = self.__read_int(4)
                dsp = self.__read_int(4)
                if (tag == 0x100): 
                    width.value = dsp
                elif (tag == 0x101): 
                    height.value = dsp
                elif (tag == 0x111): 
                    data_start_pos.value = dsp
                elif (tag == 0x117): 
                    data_length.value = dsp
                elif (tag == 0x103): 
                    ccitt_typ.value = (Utils.valToEnum(dsp, TiffHelper.CCITT_Types))
                elif (tag == 0x129): 
                    pass
                i += 1
            return data_length.value > 0
        
        def get_page_info(self, page_index : int, width : int, height : int, dpi_x : int, dpi_y : int, is_mono : bool, has_text_ : bool) -> None:
            dpi_y.value = 0
            dpi_x.value = dpi_y.value
            height.value = dpi_x.value
            width.value = height.value
            has_text_.value = False
            is_mono.value = has_text_.value
            if ((page_index < 0) or page_index >= len(self.__m_ifd_offset)): 
                return
            baseoff = self.__m_ifd_offset[page_index]
            self.__m_stream.position = baseoff
            i = 0
            dircount = self.__read_int(2)
            mono = -1
            res_unit = 2
            res_xpos = 0
            res_ypos = 0
            i = 0
            while i < dircount: 
                self.__m_stream.position = baseoff + (2) + (i * 12)
                tag = self.__read_int(2)
                typ = self.__read_int(2)
                cou = self.__read_int(4)
                dsp = self.__read_int(4)
                if (tag == 0x100): 
                    width.value = dsp
                elif (tag == 0x101): 
                    height.value = dsp
                elif (tag == 0x106 and (mono < 0)): 
                    mono = (1 if (dsp == 0 or dsp == 1) else 0)
                elif (tag == 0x102 and dsp > 1): 
                    mono = 0
                elif (tag == 0x932F): 
                    has_text_.value = True
                elif (tag == 0x128): 
                    res_unit = dsp
                elif (tag == 0x11A): 
                    res_xpos = (dsp)
                elif (tag == 0x11B): 
                    res_ypos = (dsp)
                i += 1
            is_mono.value = mono == 1
            if (((res_unit == 2 or res_unit == 3)) and res_xpos > (0)): 
                self.__m_stream.position = res_xpos
                v1 = self.__read_int(4)
                v2 = self.__read_int(4)
                a = v1
                if (v2 > 1): 
                    a /= (v2)
                if (res_unit == 3): 
                    a *= 2.54
                dpi_x.value = (math.floor(a))
            if (((res_unit == 2 or res_unit == 3)) and res_ypos > (0)): 
                self.__m_stream.position = res_ypos
                v1 = self.__read_int(4)
                v2 = self.__read_int(4)
                a = v1
                if (v2 > 1): 
                    a /= (v2)
                if (res_unit == 3): 
                    a *= 2.54
                dpi_y.value = (math.floor(a))
        
        def write_tiff(self, res : Stream, width : int, height : int, typ : 'CCITT_Types', xresolution : float, yresolution : float, invert : bool, data : bytearray) -> None:
            """ Создание TIFF по чистым данным без заголовка (фактически обрамляет заголовком)
            
            Args:
                res(Stream): 
                width(int): 
                height(int): 
                typ(CCITT_Types): 
                xresolution(float): 
                yresolution(float): 
                data(bytearray): 
            """
            res.writebyte(0x49)
            res.writebyte(0x49)
            self.__write_int0(res, 0x2A, 2)
            self.__write_int0(res, (8 + len(data) + 8) + 8, 4)
            res.write(data, 0, len(data))
            self.__write_int0(res, math.floor(xresolution), 4)
            self.__write_int0(res, 1, 4)
            self.__write_int0(res, math.floor(yresolution), 4)
            self.__write_int0(res, 1, 4)
            dirs = 0
            self.__write_int0(res, 0, 2)
            self.__write_dir_entry(res, 0xFE, 4, 1, 0)
            dirs += 1
            self.__write_dir_entry(res, 0x100, 3, 1, width)
            dirs += 1
            self.__write_dir_entry(res, 0x101, 3, 1, height)
            dirs += 1
            self.__write_dir_entry(res, 0x102, 3, 1, 1)
            dirs += 1
            self.__write_dir_entry(res, 0x103, 3, 1, typ)
            dirs += 1
            self.__write_dir_entry(res, 0x106, 3, 1, (1 if invert else 0))
            dirs += 1
            self.__write_dir_entry(res, 0x111, 4, 1, 8)
            dirs += 1
            self.__write_dir_entry(res, 0x115, 3, 1, 1)
            dirs += 1
            self.__write_dir_entry(res, 0x116, 3, 1, height)
            dirs += 1
            self.__write_dir_entry(res, 0x117, 4, 1, len(data))
            dirs += 1
            self.__write_dir_entry(res, 0x11A, 5, 1, 8 + len(data))
            dirs += 1
            self.__write_dir_entry(res, 0x11B, 5, 1, 8 + len(data) + 8)
            dirs += 1
            self.__write_dir_entry(res, 0x128, 3, 1, 2)
            dirs += 1
            self.__write_int0(res, 0, 4)
            res.position = (8 + len(data) + 8) + 8
            self.__write_int0(res, dirs, 2)
        
        def __read_int(self, count : int) -> int:
            res = 0
            i = 0
            while i < count: 
                j = self.__m_stream.readbyte()
                if (j < 0): 
                    break
                if (self.__m_msb): 
                    res |= j << ((((count - 1 - i)) << 3))
                else: 
                    res |= j << ((i << 3))
                i += 1
            return res
        
        def __read_buf(self, pos : int, size : int) -> None:
            if (len(self.__m_buf) < size): 
                self.__m_buf = Utils.newArrayOfBytes(size, 0)
            self.__m_stream.position = pos
            self.__m_stream.read(self.__m_buf, 0, size)
        
        def __write_int(self, fout : Stream, val : int, count : int) -> None:
            i = 0
            while i < count: 
                j = 0
                if (self.__m_msb): 
                    j = (((val >> ((((count - 1 - i)) << 3)))) & 0xFF)
                else: 
                    j = (((val >> ((i << 3)))) & 0xFF)
                self.__fbuf2[i] = (j)
                i += 1
            fout.write(self.__fbuf2, 0, count)
        
        def __write_int0(self, fout : Stream, val : int, count : int) -> None:
            i = 0
            while i < count: 
                j = ((val >> ((i << 3)))) & 0xFF
                self.__fbuf2[i] = (j)
                i += 1
            fout.write(self.__fbuf2, 0, count)
        
        def __write_dir_entry(self, fout : Stream, tag : int, typ : int, count : int, data : int) -> None:
            self.__write_int0(fout, tag, 2)
            self.__write_int0(fout, typ, 2)
            self.__write_int0(fout, count, 4)
            self.__write_int0(fout, data, 4)
    
    @staticmethod
    def create_doc(content : bytearray) -> 'UnitextDocument':
        res = UnitextDocument._new41(FileFormat.TIF)
        with MemoryStream(content) as mem: 
            try: 
                ti = TiffHelper.Tiff(mem)
                wi = 0
                hei = 0
                dpx = 0
                dpy = 0
                m = False
                has_txt = False
                if (ti.pages_count == 1): 
                    p = UnilayPage._new156(content)
                    wrapwi157 = RefOutArgWrapper(0)
                    wraphei158 = RefOutArgWrapper(0)
                    wrapdpx159 = RefOutArgWrapper(0)
                    wrapdpy160 = RefOutArgWrapper(0)
                    wrapm161 = RefOutArgWrapper(False)
                    wraphas_txt162 = RefOutArgWrapper(False)
                    ti.get_page_info(0, wrapwi157, wraphei158, wrapdpx159, wrapdpy160, wrapm161, wraphas_txt162)
                    wi = wrapwi157.value
                    hei = wraphei158.value
                    dpx = wrapdpx159.value
                    dpy = wrapdpy160.value
                    m = wrapm161.value
                    has_txt = wraphas_txt162.value
                    p.width = wi
                    p.height = hei
                    res.pages.append(p)
                else: 
                    i = 0
                    while i < ti.pages_count: 
                        with MemoryStream() as pm: 
                            ti.store(i, pm)
                            p = UnilayPage._new156(pm.toarray())
                            wrapwi164 = RefOutArgWrapper(0)
                            wraphei165 = RefOutArgWrapper(0)
                            wrapdpx166 = RefOutArgWrapper(0)
                            wrapdpy167 = RefOutArgWrapper(0)
                            wrapm168 = RefOutArgWrapper(False)
                            wraphas_txt169 = RefOutArgWrapper(False)
                            ti.get_page_info(0, wrapwi164, wraphei165, wrapdpx166, wrapdpy167, wrapm168, wraphas_txt169)
                            wi = wrapwi164.value
                            hei = wraphei165.value
                            dpx = wrapdpx166.value
                            dpy = wrapdpy167.value
                            m = wrapm168.value
                            has_txt = wraphas_txt169.value
                            p.width = wi
                            p.height = hei
                            res.pages.append(p)
                        i += 1
            except Exception as ex: 
                res.error_message = ex.__str__()
        return res