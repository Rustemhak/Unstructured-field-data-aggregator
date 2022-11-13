# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import Stream

from pullenti.util.ArchiveHelper import ArchiveHelper
from pullenti.unitext.internal.pdf.PdfReference import PdfReference
from pullenti.unitext.internal.misc.PngWrapper import PngWrapper
from pullenti.unitext.internal.pdf.PdfObject import PdfObject
from pullenti.unitext.internal.pdf.PdfStringValue import PdfStringValue
from pullenti.unitext.internal.pdf.PdfRealValue import PdfRealValue
from pullenti.unitext.internal.pdf.PdfBoolValue import PdfBoolValue
from pullenti.unitext.internal.pdf.PdfName import PdfName
from pullenti.unitext.internal.pdf.PdfArray import PdfArray
from pullenti.unitext.internal.pdf.PdfIntValue import PdfIntValue

class PdfDictionary(PdfObject):
    
    def __init__(self) -> None:
        super().__init__()
        self.__m_items = dict()
        self.__m_stream_data = None
        self.__m_stream_in = None
        self.__m_stream_pos = 0
        self.__m_stream_length = 0
        self._m_file_pos = 0
    
    @property
    def data(self) -> bytearray:
        if (self.__m_stream_data is None): 
            if (self.__m_stream_length == 0): 
                return None
            self.__m_stream_data = Utils.newArrayOfBytes(self.__m_stream_length, 0)
            self.__m_stream_in.position = self.__m_stream_pos
            self.__m_stream_in.read(self.__m_stream_data, 0, self.__m_stream_length)
        return self.__m_stream_data
    @data.setter
    def data(self, value) -> bytearray:
        self.__m_stream_data = value
        return value
    
    @property
    def keys(self) -> typing.List[str]:
        return list(self.__m_items.keys())
    
    def is_simple(self, lev : int) -> bool:
        if (len(self.__m_items) > 10 or lev > 10): 
            return False
        for key in self.keys: 
            if (key == "Parent"): 
                continue
            it = self.get_object(key, False)
            if (it is not None and not it.is_simple(lev + 1)): 
                return False
        return True
    
    def to_string_ex(self, lev : int) -> str:
        if (lev > 5): 
            return "<<...{0}>>".format(len(self.__m_items))
        res = io.StringIO()
        it = self.get_object("Type", False)
        if (it is not None): 
            print(str(it), end="", file=res)
        print("<<", end="", file=res)
        fi = True
        partial = False
        for key in self.keys: 
            if (key == "Parent" or key == "Type"): 
                continue
            it = self.get_object(key, False)
            if (it is None): 
                indir = self.__m_items[key]
                if (not fi): 
                    print(", ", end="", file=res)
                else: 
                    fi = False
                print("{0}={1}".format(key, ("NULL" if indir is None else str(indir))), end="", file=res, flush=True)
                if (res.tell() > 100): 
                    break
                continue
            if (not it.is_simple(lev + 1)): 
                partial = True
                continue
            if (not fi): 
                print(", ", end="", file=res)
            else: 
                fi = False
            if (res.tell() > 100): 
                partial = True
                break
            str0_ = it.to_string_ex(lev + 1)
            if (len(str0_) > 50): 
                str0_ = (str0_[0:0+50] + "...")
            print("{0}={1}".format(key, str0_), end="", file=res, flush=True)
        if (partial): 
            print("...{0}".format(len(self.__m_items)), end="", file=res, flush=True)
        print(">>", end="", file=res)
        if (self.__m_stream_length > 0): 
            print(" DATA:{0}".format(self.__m_stream_length), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def has_data_stream(self) -> bool:
        return self.__m_stream_length > 0
    
    def _post_parse(self, stream : 'PdfStream') -> None:
        self.__m_items.clear()
        self.__m_stream_in = (None)
        self.__m_stream_length = 0
        self.__m_stream_data = (None)
        p0 = stream.position
        ch = 0
        i = 0
        str0_ = None
        while True:
            i = stream.peek_solid_byte()
            if (((i)) >= 0): pass
            else: 
                break
            ch = (i)
            if ((chr(ch)) == '/'): 
                str0_ = PdfStringValue.get_string_by_bytes(stream.read_name())
                if (str0_ is None): 
                    break
                if (str0_ == "Contents"): 
                    pass
                obj = stream.parse_object(self.source_file, False)
                if (obj is None): 
                    break
                if (not str0_ in self.__m_items): 
                    self.__m_items[str0_] = obj
                continue
            if ((chr(ch)) != '>'): 
                break
            stream.position = stream.position + 1
            ch = (stream.read_byte())
            if ((chr(ch)) != '>'): 
                break
            self.__parse_stream(stream)
            return
    
    def __parse_stream(self, stream : 'PdfStream') -> None:
        p0 = stream.position
        str0_ = stream.read_word(False)
        if (str0_ != "stream"): 
            stream.position = p0
            return
        stream_tag = Utils.newArrayOfBytes(6, 0)
        ch = stream.read_byte()
        if (ch != (0xD)): 
            stream.position = stream.position - 1
        ch = (stream.read_byte())
        if (ch != (0xA)): 
            stream.position = stream.position - 1
        self.__m_stream_in = stream
        self.__m_stream_pos = stream.position
        self.__m_stream_length = (self.get_int_item("Length"))
        if (self.__m_stream_length > 0 and ((self.__m_stream_pos + self.__m_stream_length) < stream.length)): 
            stream.position = self.__m_stream_pos + self.__m_stream_length
        len0_ = 0
        i = 0
        while True:
            i = stream.read_byte()
            if (((i)) >= 0): pass
            else: 
                break
            ch = (i)
            len0_ += 1
            if ((chr(ch)) != 'e'): 
                continue
            ch = (stream.read_byte())
            len0_ += 1
            if ((chr(ch)) != 'n'): 
                continue
            ch = (stream.read_byte())
            len0_ += 1
            if ((chr(ch)) != 'd'): 
                continue
            p0 = stream.position
            stream.read(stream_tag, 0, 6)
            if (PdfStringValue.get_string_by_bytes(stream_tag) == "stream"): 
                len0_ -= 3
                break
            stream.position = p0
        if (self.__m_stream_length == 0): 
            self.__m_stream_length = len0_
    
    def get_string_item(self, key : str) -> str:
        val = self.get_object(key, False)
        while True:
            if (val is None): 
                return None
            if (isinstance(val, PdfName)): 
                return val.name
            if (isinstance(val, PdfBoolValue)): 
                return ("true" if val.val else "false")
            if (isinstance(val, PdfStringValue)): 
                return PdfStringValue.get_string_by_bytes(val.val)
            if (isinstance(val, PdfIntValue)): 
                return str(val.val)
            if (isinstance(val, PdfArray)): 
                val = val.get_item(0)
                if (val is None): 
                    break
                continue
            break
        return None
    
    def is_type_item(self, type_val : str) -> bool:
        return self.get_string_item("Type") == type_val
    
    def get_int_item(self, key : str) -> int:
        val = self.get_object(key, False)
        if (val is None): 
            return 0
        if (isinstance(val, PdfIntValue)): 
            return val.val
        if (isinstance(val, PdfRealValue)): 
            return math.floor(val.get_double())
        return 0
    
    def get_object(self, key : str, keep_ref : bool=False) -> 'PdfObject':
        res = None
        wrapres174 = RefOutArgWrapper(None)
        inoutres175 = Utils.tryGetValue(self.__m_items, key, wrapres174)
        res = wrapres174.value
        if (not inoutres175): 
            return None
        if ((isinstance(res, PdfReference)) and not keep_ref): 
            res = self.source_file.get_object(res.id0_)
            if (res is None): 
                return None
            self.__m_items[key] = res
        return res
    
    def get_dictionary(self, key : str, typ_val : str=None) -> 'PdfDictionary':
        obj = self.get_object(key, False)
        if (isinstance(obj, PdfArray)): 
            obj = obj.get_item(0)
        if (isinstance(obj, PdfDictionary)): 
            res = Utils.asObjectOrNull(obj, PdfDictionary)
            if (typ_val is not None): 
                if (not res.is_type_item(typ_val)): 
                    return None
            return res
        return None
    
    def get_all_pages(self, res : typing.List['PdfDictionary']) -> None:
        if (self.is_type_item("Page")): 
            res.append(self)
            return
        dic = self.get_dictionary("Pages", "Pages")
        if (dic is not None): 
            dic.get_all_pages(res)
        else: 
            kids = Utils.asObjectOrNull(self.get_object("Kids", False), PdfArray)
            if (kids is not None): 
                i = 0
                while i < kids.items_count: 
                    it = kids.get_item(i)
                    if (isinstance(it, PdfDictionary)): 
                        it.get_all_pages(res)
                    i += 1
    
    def extract_data(self) -> bytearray:
        stream_data = self.data
        if (stream_data is None): 
            return Utils.newArrayOfBytes(0, 0)
        str0_ = self.get_string_item("Filter")
        if (Utils.isNullOrEmpty(str0_)): 
            return stream_data
        if (str0_ != "FlateDecode"): 
            return None
        if (len(stream_data) < 10): 
            return None
        res = ArchiveHelper.decompress_zlib(stream_data)
        if (res is None): 
            return None
        dparms = self.get_dictionary("DecodeParms", None)
        predict = 0
        n = 0
        columns = 0
        if (dparms is not None): 
            iv = Utils.asObjectOrNull(dparms.get_object("Predictor", False), PdfIntValue)
            if (iv is not None and iv.val > 1): 
                predict = iv.val
            iv = (Utils.asObjectOrNull(dparms.get_object("Columns", False), PdfIntValue))
            if (iv is not None): 
                columns = iv.val
            iv = (Utils.asObjectOrNull(dparms.get_object("Colors", False), PdfIntValue))
            if (iv is not None): 
                n = iv.val
        if ((predict >= 10 and predict <= 15 and n > 0) and columns > 0): 
            row_size = columns * n
            if (predict == 15): 
                row_size += 1
            pos0 = 0
            while (pos0 + row_size) < len(res): 
                cod = predict - 10
                pos = pos0
                if (predict == 15): 
                    cod = (res[pos0])
                    pos += 1
                j = pos
                while j < (pos0 + row_size): 
                    val_left = 0
                    val_top = 0
                    val_corner = 0
                    k = j - n
                    kk = j - row_size
                    if (kk >= 0): 
                        val_top = res[kk]
                    if (k >= pos): 
                        val_left = res[k]
                        if (kk >= 0): 
                            val_corner = res[kk - n]
                    res[j] = PngWrapper.filter_byte(cod, False, res[j], val_left, val_top, val_corner)
                    j += 1
                pos0 += row_size
            if (predict == 15): 
                p = 0
                i = 0
                while i < len(res): 
                    if (((i % row_size)) == 0): 
                        pass
                    else: 
                        res[p] = res[i]
                        p += 1
                    i += 1
                res1 = Utils.newArrayOfBytes(p, 0)
                i = 0
                while i < p: 
                    res1[i] = res[i]
                    i += 1
                res = res1
        return res
    
    def get_total_data_stream(self, key : str) -> bytearray:
        obj = self.get_object(key, False)
        if (obj is None): 
            return None
        if (isinstance(obj, PdfDictionary)): 
            return obj.extract_data()
        arr = Utils.asObjectOrNull(obj, PdfArray)
        if (arr is None): 
            return None
        res = None
        i = 0
        first_pass639 = True
        while True:
            if first_pass639: first_pass639 = False
            else: i += 1
            if (not (i < arr.items_count)): break
            obj = arr.get_item(i)
            if (obj is None): 
                continue
            if (not (isinstance(obj, PdfDictionary))): 
                continue
            tmp = obj.extract_data()
            if (tmp is None): 
                continue
            if (len(tmp) < 1): 
                continue
            if (res is None): 
                res = bytearray(tmp)
            else: 
                res.append(0xD)
                res.append(0xA)
                res.extend(tmp)
        return bytearray(res)
    
    @staticmethod
    def _new228(_arg1 : int) -> 'PdfDictionary':
        res = PdfDictionary()
        res._m_file_pos = _arg1
        return res