# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import uuid
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.util.EncodingStandard import EncodingStandard
from pullenti.util.MiscHelper import MiscHelper
from pullenti.util.EncodingWrapper import EncodingWrapper

class DbfTable(object):
    # Поддержка работы с таблицами DBF
    
    def __init__(self, file_name : str) -> None:
        self.__m_stream = None;
        self.__m_first_rec_pos = 0
        self.columnn_names = list()
        self.column_lengths = list()
        self.__buf_rec = None;
        self.__m_enc = None;
        self.values = list()
        self.percent = 0
        self.__m_stream = FileStream(file_name, "rb")
        buf = Utils.newArrayOfBytes(1024, 0)
        if (self.__m_stream.read(buf, 0, 0x20) != 0x20 or buf[0] != (3)): 
            raise Utils.newException("Bad DBF format", None)
        head_len = (((buf[9]) << 8)) | (buf[8])
        rec_len = (((buf[11]) << 8)) | (buf[10])
        while (self.__m_stream.position + (0x20)) <= head_len: 
            if (self.__m_stream.read(buf, 0, 0x20) != 0x20): 
                raise Utils.newException("Bad DBF format", None)
            i = 0
            while i < 11: 
                if (buf[i] == (0)): 
                    break
                i += 1
            nam = MiscHelper.decode_string_ascii(buf, 0, i).strip()
            self.columnn_names.append(nam)
            self.column_lengths.append(buf[0x10])
            self.values.append(None)
        self.__m_stream.position = head_len - 1
        b = self.__m_stream.readbyte()
        if (b != 13): 
            raise Utils.newException("Bad DBF format (end of head not 13)", None)
        vals = list()
        le = 0
        for v in self.column_lengths: 
            le += v
            vals.append(None)
        if ((le + 1) != rec_len): 
            raise Utils.newException("Total columns length {0} != length of record {1}".format(le + 1, rec_len), None)
        self.__m_enc = EncodingWrapper(EncodingStandard.CP1251)
        self.__buf_rec = Utils.newArrayOfBytes(rec_len, 0)
        self.__m_first_rec_pos = self.__m_stream.position
    
    def close(self) -> None:
        if (self.__m_stream is not None): 
            self.__m_stream.close()
        self.__m_stream = (None)
    
    def get_string(self, column_name : str) -> str:
        i = Utils.indexOfList(self.columnn_names, column_name, 0)
        if (i < 0): 
            return None
        if (Utils.isNullOrEmpty(self.values[i])): 
            return None
        return self.values[i]
    
    def get_guid(self, column_name : str) -> uuid.UUID:
        val = self.get_string(column_name)
        if (Utils.isNullOrEmpty(val)): 
            return None
        try: 
            return uuid.UUID(val)
        except Exception as ex: 
            return None
    
    def read_next(self, only_column_index : int=-1) -> bool:
        if (self.__m_stream is None): 
            return False
        if (self.__m_stream.read(self.__buf_rec, 0, len(self.__buf_rec)) != len(self.__buf_rec)): 
            return False
        if (self.__buf_rec[0] != (0x20)): 
            return False
        d = 1
        i = 0
        i = 0
        while i < len(self.__buf_rec): 
            j = self.__buf_rec[i]
            if (j >= 0xE0 and j <= 0xEF): 
                j -= 0x30
            if (j >= 0x80 and j <= 0xDF): 
                self.__buf_rec[i] = ((j + 0x40))
            if (j == 0xF1): 
                self.__buf_rec[i] = (0xB8)
            if (j == 0xF0): 
                self.__buf_rec[i] = (0xA8)
            i += 1
        i = 0
        while i < len(self.columnn_names): 
            if ((only_column_index < 0) or only_column_index == i): 
                val = self.__m_enc.get_string(self.__buf_rec, d, self.column_lengths[i]).strip()
                self.values[i] = val
            d += self.column_lengths[i]
            i += 1
        if (self.__m_stream.length < (100000)): 
            self.percent = ((math.floor((self.__m_stream.position * (100)) / self.__m_stream.length)))
        else: 
            self.percent = ((math.floor(self.__m_stream.position / ((math.floor(self.__m_stream.length / (100)))))))
        return True
    
    def reread(self) -> None:
        if (self.__m_stream is not None): 
            self.__m_stream.position = self.__m_first_rec_pos
    def __enter__(self): return self
    def __exit__(self, typ, val, traceback): self.close()