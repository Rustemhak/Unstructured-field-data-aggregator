# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.pdf.PdfObject import PdfObject
from pullenti.unitext.internal.pdf.PdfArray import PdfArray
from pullenti.unitext.internal.pdf.PdfStringValue import PdfStringValue
from pullenti.unitext.internal.pdf.PdfBoolValue import PdfBoolValue
from pullenti.unitext.internal.pdf.PdfNull import PdfNull
from pullenti.unitext.internal.pdf.PdfReference import PdfReference
from pullenti.unitext.internal.pdf.PdfIntValue import PdfIntValue
from pullenti.unitext.internal.pdf.PdfName import PdfName
from pullenti.unitext.internal.pdf.PdfRealValue import PdfRealValue
from pullenti.unitext.internal.pdf.PdfDictionary import PdfDictionary

class PdfStream(object):
    
    def __init__(self, file_name : str, file_content : bytearray) -> None:
        self.__m_stream = None
        if (file_content is not None): 
            self.__m_stream = (MemoryStream(file_content))
        else: 
            self.__m_stream = (FileStream(file_name, "rb"))
    
    def close(self) -> None:
        if (self.__m_stream is not None): 
            self.__m_stream.close()
        self.__m_stream = (None)
    
    def __is_space(self, ch : int) -> bool:
        if ((ch == (0x20) or ch == (0xD) or ch == (0xA)) or ch == (9)): 
            return True
        return False
    
    def __is_delimiter(self, ch : int) -> bool:
        if (((chr(ch)) == '(' or (chr(ch)) == ')' or (chr(ch)) == '<') or (chr(ch)) == '>'): 
            return True
        if (((chr(ch)) == '[' or (chr(ch)) == ']' or (chr(ch)) == '{') or (chr(ch)) == '}'): 
            return True
        if ((chr(ch)) == '/'): 
            return True
        return False
    
    def __hex_to_int(self, ch : int) -> int:
        if ((chr(ch)) >= '0' and (chr(ch)) <= '9'): 
            return ((ch) - (ord('0')))
        if ((chr(ch)) >= 'A' and (chr(ch)) <= 'F'): 
            return (((ch) - (ord('A'))) + 10)
        if ((chr(ch)) >= 'a' and (chr(ch)) <= 'f'): 
            return (((ch) - (ord('a'))) + 10)
        return -1
    
    def __to_hex(self, val : int) -> int:
        if (val < 10): 
            return ((ord('0')) + val)
        return (((ord('A')) + val) - 10)
    
    @property
    def position(self) -> int:
        return self.__m_stream.position
    @position.setter
    def position(self, value) -> int:
        self.__m_stream.position = value
        return value
    
    @property
    def length(self) -> int:
        return self.__m_stream.length
    
    def read_byte(self) -> int:
        return self.__m_stream.readbyte()
    
    def read(self, arr : bytearray, off : int, len0_ : int) -> int:
        return self.__m_stream.read(arr, off, len0_)
    
    def peek_solid_byte(self) -> int:
        cmt = False
        i = self.__m_stream.readbyte()
        while i >= 0: 
            ch = i
            if ((chr(ch)) == '%'): 
                cmt = True
            elif (ch == (0xD) or ch == (0xA)): 
                cmt = False
            elif (ch != (0x20) and ch != (9) and not cmt): 
                self.__m_stream.position = self.__m_stream.position - (1)
                return i
            i = self.__m_stream.readbyte()
        return -1
    
    def read_head(self) -> bytearray:
        head = Utils.newArrayOfBytes(4, 0)
        p0 = self.__m_stream.position
        i = 0
        self.__m_stream.read(head, 0, 4)
        if ((len(head) != 4 or (chr(head[0])) != '%' or (chr(head[1])) != 'P') or (chr(head[2])) != 'D' or (chr(head[3])) != 'F'): 
            raise Utils.newException("File not in PDF format", None)
        i = 4
        while i < (self.__m_stream.length - (4)): 
            self.__m_stream.position = i
            self.__m_stream.read(head, 0, 4)
            if (((chr(head[0])) == ' ' and (chr(head[1])) == 'o' and (chr(head[2])) == 'b') and (chr(head[3])) == 'j'): 
                break
            i += 1
        if (i >= (self.__m_stream.length - (4))): 
            raise Utils.newException("Bad PDF format", None)
        while i > 4: 
            self.__m_stream.position = i
            b = self.__m_stream.readbyte()
            if ((chr(b)) != ' ' and (((b < (0x30)) or b > (0x39)))): 
                i += 1
                break
            i -= 1
        self.__m_stream.position = p0
        head = Utils.newArrayOfBytes(i, 0)
        self.__m_stream.read(head, 0, len(head))
        return head
    
    def read_lexem_string(self) -> bytearray:
        ch = self.__m_stream.readbyte()
        p0 = self.__m_stream.position
        i = 0
        val = bytearray()
        if ((chr(ch)) == '<'): 
            while True:
                i = self.__m_stream.readbyte()
                if (((i)) > 0): pass
                else: 
                    break
                ch = (i)
                if ((chr(ch)) == '>'): 
                    break
                if (self.__is_space(ch)): 
                    continue
                i1 = self.__hex_to_int(ch)
                ch = (self.__m_stream.readbyte())
                i2 = (0 if (chr(ch)) == '>' else self.__hex_to_int(ch))
                if ((i1 < 0) or (i2 < 0)): 
                    val.append(0)
                else: 
                    val.append((((i1 << 4)) + i2))
                if ((chr(ch)) == '>'): 
                    break
            return bytearray(val)
        if ((chr(ch)) != '('): 
            return None
        lev = 0
        is_unicode = 0
        while True:
            i = self.__m_stream.readbyte()
            if (((i)) >= 0): pass
            else: 
                break
            ch = (i)
            if ((len(val) < 2) and ((ch == (0xFE) or ch == (0xFF)))): 
                is_unicode += 1
            if (is_unicode > 1): 
                if ((chr(ch)) == ')' and ((((len(val) % 2)) == 0))): 
                    break
                val.append(ch)
                continue
            val.append(ch)
            if ((chr(ch)) == '('): 
                lev += 1
                continue
            if ((chr(ch)) == ')'): 
                lev -= 1
                if (lev < 0): 
                    del val[len(val) - 1]
                    break
                continue
            if ((chr(ch)) != '\\'): 
                continue
            del val[len(val) - 1]
            ch = (self.__m_stream.readbyte())
            if ((chr(ch)) >= '0' and (chr(ch)) <= '7'): 
                res = ((ch) - (ord('0')))
                for k in range(2):
                    ch = (self.__m_stream.readbyte())
                    if ((chr(ch)) >= '0' and (chr(ch)) <= '7'): 
                        res = ((res * 8) + (((ch) - (ord('0')))))
                    else: 
                        self.__m_stream.position = self.__m_stream.position - (1)
                        break
                val.append(res)
                continue
            if (ch == (0xD) or ch == (0xA)): 
                continue
            if ((chr(ch)) == 'r'): 
                ch = (0xD)
            elif ((chr(ch)) == 'n'): 
                ch = (0xA)
            elif ((chr(ch)) == 't'): 
                ch = (9)
            elif ((chr(ch)) == 'b'): 
                ch = (8)
            elif ((chr(ch)) == 'f'): 
                ch = (12)
            elif ((chr(ch)) == '\\' or (chr(ch)) == '(' or (chr(ch)) == ')'): 
                pass
            else: 
                pass
            val.append(ch)
        return bytearray(val)
    
    def read_name(self) -> bytearray:
        i = self.__m_stream.readbyte()
        if ((chr(i)) != '/'): 
            return None
        res = bytearray()
        while True:
            i = self.__m_stream.readbyte()
            if (((i)) >= 0): pass
            else: 
                break
            ch = i
            if (self.__is_space(ch)): 
                break
            if (self.__is_delimiter(ch)): 
                self.__m_stream.position = self.__m_stream.position - (1)
                break
            if ((chr(ch)) != '#'): 
                res.append(ch)
                continue
            i1 = self.__hex_to_int(self.__m_stream.readbyte())
            i2 = self.__hex_to_int(self.__m_stream.readbyte())
            if ((i1 < 0) or (i2 < 0)): 
                res.append(0)
            else: 
                res.append((((i1 << 4)) + i2))
        if (len(res) == 0): 
            return None
        return bytearray(res)
    
    def read_word(self, not_null : bool=False) -> str:
        i = 0
        res = io.StringIO()
        while True:
            i = self.__m_stream.readbyte()
            if (((i)) >= 0): pass
            else: 
                break
            ch = i
            if (self.__is_space(ch)): 
                if (res.tell() > 0): 
                    break
            elif (self.__is_delimiter(ch)): 
                if (res.tell() == 0 and not_null): 
                    print(chr(ch), end="", file=res)
                    break
                self.__m_stream.position = self.__m_stream.position - (1)
                break
            else: 
                print(chr(ch), end="", file=res)
        if (res.tell() == 0): 
            return None
        return Utils.toStringStringIO(res)
    
    def try_read_id_and_version(self, must_be_ref : bool, id0_ : int, vers : int) -> bool:
        id0_.value = 0
        vers.value = (0)
        p0 = self.__m_stream.position
        inoutres222 = Utils.tryParseInt(self.read_word(False), id0_)
        if (not inoutres222): 
            self.__m_stream.position = p0
            return False
        inoutres221 = Utils.tryParseInt(self.read_word(False), vers)
        if (not inoutres221): 
            self.__m_stream.position = p0
            return False
        str0_ = self.read_word(False)
        if (must_be_ref): 
            if (str0_ == "R"): 
                return True
        elif (str0_ == "obj"): 
            return True
        self.__m_stream.position = p0
        return False
    
    def parse_object(self, file : 'PdfFile', text : bool) -> 'PdfObject':
        res = None
        i = self.peek_solid_byte()
        if (i < 0): 
            return res
        ch = i
        p0 = self.__m_stream.position
        if ((chr(ch)) >= '0' and (chr(ch)) <= '9' and not text): 
            id0_ = 0
            ver = 0
            wrapid223 = RefOutArgWrapper(0)
            wrapver224 = RefOutArgWrapper(0)
            inoutres225 = self.try_read_id_and_version(True, wrapid223, wrapver224)
            id0_ = wrapid223.value
            ver = wrapver224.value
            if (inoutres225): 
                res = (PdfReference())
                res.source_file = file
                res.id0_ = id0_
                res.version = ver
                return res
        if (((((chr(ch)) >= '0' and (chr(ch)) <= '9')) or (chr(ch)) == '+' or (chr(ch)) == '-') or (chr(ch)) == '.'): 
            str0_ = self.read_word(False)
            if (str0_ is None): 
                return None
            if (str0_.find('.') < 0): 
                v = 0
                wrapv226 = RefOutArgWrapper(0)
                inoutres227 = Utils.tryParseInt(str0_, wrapv226)
                v = wrapv226.value
                if (not inoutres227): 
                    return None
                ires = PdfIntValue()
                ires.val = v
                return ires
            else: 
                fres = PdfRealValue()
                fres.val = str0_
                return fres
        if ((chr(ch)) == '/'): 
            nres = PdfName()
            nres.name = PdfStringValue.get_string_by_bytes(self.read_name())
            if (nres.name is None): 
                return None
            return nres
        elif ((chr(ch)) == '('): 
            sres = PdfStringValue()
            sres.val = self.read_lexem_string()
            if (sres.val is None): 
                return None
            return sres
        elif ((chr(ch)) == '['): 
            res = (PdfArray())
        elif ((chr(ch)) == '<'): 
            self.__m_stream.position = p0 + 1
            ch = (self.__m_stream.readbyte())
            if ((chr(ch)) == '<'): 
                res = (PdfDictionary._new228(p0))
            else: 
                sres = PdfStringValue()
                self.__m_stream.position = p0
                sres.val = self.read_lexem_string()
                if (sres.val is None): 
                    return None
                return sres
        elif ((((chr(ch)) == '\'' or (chr(ch)) == '\"')) and text): 
            nres = PdfName()
            nres.name = ("\'" if (chr(ch)) == '\'' else "\"")
            self.__m_stream.position = self.__m_stream.position + (1)
            return nres
        else: 
            str0_ = self.read_word(False)
            swichVal = str0_
            if (swichVal == "null"): 
                return PdfNull()
            elif (swichVal == "true"): 
                bres1 = PdfBoolValue()
                bres1.val = True
                return bres1
            elif (swichVal == "false"): 
                bres2 = PdfBoolValue()
                bres2.val = False
                return bres2
            elif (swichVal == "endobj"): 
                return None
            if (text and str0_ is not None): 
                nres = PdfName()
                nres.name = str0_
                return nres
            return None
        res.source_file = file
        if (isinstance(res, PdfDictionary)): 
            res._post_parse(self)
        elif (isinstance(res, PdfArray)): 
            res._post_parse(self)
        return res
    
    def parse_content(self) -> typing.List['PdfObject']:
        res = list()
        while True:
            i = self.peek_solid_byte()
            if (i < 0): 
                break
            try: 
                obj = self.parse_object(None, True)
                if (obj is not None): 
                    res.append(obj)
                else: 
                    self.read_byte()
            except Exception as ex229: 
                break
        return res
    def __enter__(self): return self
    def __exit__(self, typ, val, traceback): self.close()