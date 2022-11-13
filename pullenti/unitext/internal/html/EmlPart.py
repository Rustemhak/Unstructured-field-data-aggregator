# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import base64
from pullenti.unisharp.Utils import Utils

from pullenti.util.EncodingStandard import EncodingStandard
from pullenti.util.EncodingWrapper import EncodingWrapper

class EmlPart:
    
    def __init__(self) -> None:
        self.attrs = dict()
        self.data = None;
        self.string_data = None;
        self.string_data_pos = 0
        self.content_type = None;
        self.content_charset = None;
        self.content_location = None;
        self.content_id = None;
        self.filename = None;
        self.boundary_ref = None;
        self.boundary_id = None;
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.boundary_id is None): 
            print("(*) ", end="", file=tmp)
        print("Attrs: {0}, String: {1}, Data: {2}".format(len(self.attrs), (0 if self.string_data is None else len(self.string_data)), (0 if self.data is None else len(self.data))), end="", file=tmp, flush=True)
        if (self.content_type is not None): 
            print(" {0}".format(self.content_type), end="", file=tmp, flush=True)
        if (self.content_charset is not None): 
            print(" {0}".format(self.content_charset), end="", file=tmp, flush=True)
        if (self.string_data is not None): 
            print("  ", end="", file=tmp)
            if (len(self.string_data) < 40): 
                print(self.string_data, end="", file=tmp)
            else: 
                print(self.string_data[0:0+40] + "...", end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def try_parse(txt : str, pos : int) -> 'EmlPart':
        from pullenti.unitext.internal.html.MhtHelper import MhtHelper
        while pos.value < len(txt): 
            if (not Utils.isWhitespace(txt[pos.value])): 
                break
            pos.value += 1
        if ((pos.value + 1) >= len(txt)): 
            return None
        res = EmlPart()
        if (txt[pos.value] == '-' and txt[pos.value + 1] == '-'): 
            p0 = pos.value + 2
            pos.value += 2
            while pos.value < len(txt): 
                if (Utils.isWhitespace(txt[pos.value])): 
                    break
                pos.value += 1
            res.boundary_id = txt[p0:p0+pos.value - p0]
            while pos.value < len(txt): 
                if (not Utils.isWhitespace(txt[pos.value])): 
                    break
                pos.value += 1
        attr_value = io.StringIO()
        while pos.value < len(txt): 
            p0 = pos.value
            is_attr = False
            while pos.value < len(txt): 
                if (Utils.isWhitespace(txt[pos.value])): 
                    break
                elif (txt[pos.value] == ':'): 
                    is_attr = True
                    break
                pos.value += 1
            if (not is_attr): 
                break
            attr_name = txt[p0:p0+pos.value - p0].strip()
            if (attr_name == "From"): 
                pass
            pos.value += 1
            Utils.setLengthStringIO(attr_value, 0)
            first_pass614 = True
            while True:
                if first_pass614: first_pass614 = False
                else: pos.value += 1
                if (not (pos.value < len(txt))): break
                ch = txt[pos.value]
                if (ch == ' ' or (ord(ch)) == 9): 
                    if (attr_value.tell() == 0 or Utils.getCharAtStringIO(attr_value, attr_value.tell() - 1) == ' '): 
                        continue
                    print(' ', end="", file=attr_value)
                    continue
                if ((ord(ch)) != 0xD and (ord(ch)) != 0xA): 
                    print(ch, end="", file=attr_value)
                    continue
                if (((pos.value + 1) < len(txt)) and (ord(ch)) == 0xD and (ord(txt[pos.value + 1])) == 0xA): 
                    pos.value += 1
                if (((pos.value + 1) < len(txt)) and (((ord(txt[pos.value + 1])) == 0xD or (ord(txt[pos.value + 1])) == 0xA or not Utils.isWhitespace(txt[pos.value + 1])))): 
                    break
            if (not attr_name in res.attrs): 
                res.attrs[attr_name] = MhtHelper._decode_string(Utils.toStringStringIO(attr_value))
            pos.value += 1
        transf_enc = None
        for a in res.attrs.items(): 
            if (Utils.compareStrings(a[0], "CONTENT-TYPE", True) == 0): 
                res.content_type = a[1]
                i = a[1].find(';')
                if (i > 0): 
                    res.content_type = res.content_type[0:0+i]
                res.content_type = MhtHelper._corr_string(res.content_type)
                i = a[1].find("boundary=")
                if (i > 0): 
                    res.boundary_ref = MhtHelper._corr_string(a[1][i + 9:].strip())
                i = a[1].find("charset=")
                if (i > 0): 
                    res.content_charset = MhtHelper._corr_string(a[1][i + 8:].strip())
            elif (Utils.compareStrings(a[0], "CONTENT-TRANSFER-ENCODING", True) == 0): 
                transf_enc = MhtHelper._corr_string(a[1]).lower()
            elif (Utils.compareStrings(a[0], "CONTENT-ID", True) == 0): 
                res.content_id = (Utils.ifNotNull(MhtHelper._corr_string(a[1]), ""))
                if (len(res.content_id) > 2 and res.content_id[0] == '<'): 
                    res.content_id = res.content_id[1:1+len(res.content_id) - 2]
            elif (Utils.compareStrings(a[0], "CONTENT-LOCATION", True) == 0): 
                res.content_location = MhtHelper._corr_string(a[1])
            elif (Utils.compareStrings(a[0], "CONTENT-DISPOSITION", True) == 0): 
                i = a[1].find("filename=")
                if (i > 0): 
                    res.filename = MhtHelper._corr_string(a[1][i + 9:].strip())
        if (transf_enc is None and ((res.content_type == "text/plain" or res.content_type == "text/html"))): 
            transf_enc = "7bit"
        if (transf_enc is None): 
            return res
        isqp = transf_enc == "quoted-printable"
        is64 = transf_enc == "base64"
        if (res.boundary_id is None): 
            if (not isqp and not is64): 
                return res
        enc = None
        if (isqp and res.content_charset is not None): 
            try: 
                enc = EncodingWrapper(EncodingStandard.UNDEFINED, res.content_charset)
            except Exception as ex: 
                pass
        if (isqp and enc is None): 
            enc = EncodingWrapper(EncodingStandard.ACSII)
        buf = bytearray()
        res.string_data_pos = pos.value
        data_ = io.StringIO()
        first_pass615 = True
        while True:
            if first_pass615: first_pass615 = False
            else: pos.value += 1
            if (not (pos.value < len(txt))): break
            ch = txt[pos.value]
            if ((ch == '-' and ((pos.value + 1) < len(txt)) and txt[pos.value + 1] == '-') and (((ord(txt[pos.value - 1])) == 0xD or (ord(txt[pos.value - 1])) == 0xA)) and not Utils.isNullOrEmpty(res.boundary_id)): 
                j = 0
                j = 0
                while (j < len(res.boundary_id)) and ((pos.value + 2 + j) < len(txt)): 
                    if (res.boundary_id[j] != txt[pos.value + 2 + j]): 
                        break
                    j += 1
                if (j >= len(res.boundary_id)): 
                    if (((pos.value + 4 + j) < len(txt)) and txt[pos.value + j + 2] == '-' and txt[pos.value + j + 3] == '-'): 
                        pos.value += (j + 4)
                    break
            if (isqp and ch == '=' and ((pos.value + 2) < len(txt))): 
                if (EmlPart._to_int(txt[pos.value + 1]) >= 0 and EmlPart._to_int(txt[pos.value + 2]) >= 0): 
                    k = (EmlPart._to_int(txt[pos.value + 1]) * 16) + EmlPart._to_int(txt[pos.value + 2])
                    buf.append(k)
                    pos.value += 2
                    continue
                if ((ord(txt[pos.value + 1])) == 0xD or (ord(txt[pos.value + 1])) == 0xA): 
                    pos.value += 1
                    if ((ord(txt[pos.value + 1])) == 0xD or (ord(txt[pos.value + 1])) == 0xA): 
                        pos.value += 1
                    continue
            if (is64 and Utils.isWhitespace(ch)): 
                continue
            if (isqp): 
                if (len(buf) > 0): 
                    print(enc.get_string(bytearray(buf), 0, -1), end="", file=data_)
                    buf.clear()
                print(ch, end="", file=data_)
            else: 
                print(ch, end="", file=data_)
        if (is64): 
            if (data_.tell() > 0): 
                str0_ = Utils.toStringStringIO(data_)
                ii = str0_.find("--")
                if (ii > 0): 
                    str0_ = str0_[0:0+ii]
                try: 
                    res.data = base64.decodestring((str0_).encode('utf-8', 'ignore'))
                except Exception as ex: 
                    pass
        elif (isqp): 
            if (len(buf) > 0): 
                print(enc.get_string(bytearray(buf), 0, -1), end="", file=data_)
                buf.clear()
            if (data_.tell() > 0): 
                res.string_data = Utils.toStringStringIO(data_)
        else: 
            if (transf_enc != "7bit"): 
                pass
            res.string_data = Utils.toStringStringIO(data_)
        return res
    
    @staticmethod
    def _to_int(ch : 'char') -> int:
        if (ch >= '0' and ch <= '9'): 
            return (ord(ch)) - (ord('0'))
        if (ch >= 'A' and ch <= 'F'): 
            return 10 + (((ord(ch)) - (ord('A'))))
        if (ch >= 'a' and ch <= 'f'): 
            return 10 + (((ord(ch)) - (ord('a'))))
        return -1