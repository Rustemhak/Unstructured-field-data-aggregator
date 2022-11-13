# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import base64
import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

class MhtPart:
    
    def __init__(self, src : str) -> None:
        self.content_type = None;
        self.content_encoding = None;
        self.content_location = None;
        self.attrs = dict()
        self.data = None;
        self.string_data = None;
        i = 0
        crlf = 0
        i = 0
        while i < len(src): 
            if ((ord(src[i])) == 0xD): 
                crlf += 1
                if (((i + 1) < len(src)) and (ord(src[i + 1])) == 0xA): 
                    i += 1
            elif ((ord(src[i])) == 0xA): 
                crlf += 1
            else: 
                crlf = 0
            if (crlf >= 2): 
                break
            i += 1
        if ((crlf < 2) or i >= len(src)): 
            return
        head = src[0:0+i].strip()
        j = 0
        while len(head) > 0:
            if (not head.startswith("Content-")): 
                break
            head = head[8:]
            j = head.find("Content-")
            rec = (head if j < 0 else head[0:0+j].strip())
            if (rec.startswith("Location:")): 
                self.content_location = rec[9:].strip()
            elif (rec.startswith("Transfer-Encoding:")): 
                self.content_encoding = rec[len("Transfer-Encoding:"):].strip()
            elif (rec.startswith("Type:")): 
                self.content_type = rec[5:].strip()
            if (j < 0): 
                break
            head = head[j:]
        if (Utils.compareStrings(self.content_encoding, "base64", True) == 0): 
            self.data = base64.decodestring((src[i:].strip()).encode('utf-8', 'ignore'))
        elif (Utils.compareStrings(self.content_encoding, "quoted-printable", True) == 0): 
            tmp = io.StringIO()
            j = i
            first_pass624 = True
            while True:
                if first_pass624: first_pass624 = False
                else: j += 1
                if (not (j < len(src))): break
                if (src[j] != '='): 
                    print(src[j], end="", file=tmp)
                else: 
                    if (((j + 2) < len(src)) and MhtPart.__to_int(src[j + 1]) >= 0 and MhtPart.__to_int(src[j + 2]) >= 0): 
                        k = (MhtPart.__to_int(src[j + 1]) * 16) + MhtPart.__to_int(src[j + 2])
                        print(chr(k), end="", file=tmp)
                        j += 2
                        continue
                    j += 1
                    while j < len(src): 
                        if (src[j] != ' '): 
                            break
                        j += 1
                    while j < len(src): 
                        if ((ord(src[j])) != 0xD and (ord(src[j])) != 0xA): 
                            break
                        j += 1
                    j -= 1
            self.string_data = Utils.toStringStringIO(tmp)
    
    @staticmethod
    def __to_int(ch : 'char') -> int:
        if (ch >= '0' and ch <= '9'): 
            return (ord(ch)) - (ord('0'))
        if (ch >= 'A' and ch <= 'F'): 
            return 10 + (((ord(ch)) - (ord('A'))))
        if (ch >= 'a' and ch <= 'f'): 
            return 10 + (((ord(ch)) - (ord('a'))))
        return -1
    
    @staticmethod
    def parse_all_str(all0_ : str, i0 : int, bound : str, first : bool) -> typing.List['MhtPart']:
        res = list()
        beg = 0
        i = i0
        first_pass625 = True
        while True:
            if first_pass625: first_pass625 = False
            else: i += 1
            if (not (i < len(all0_))): break
            j = 0
            j = 0
            while j < len(bound): 
                if (bound[j] != all0_[i + j]): 
                    break
                j += 1
            if (j < len(bound)): 
                continue
            if (beg > 0): 
                pa = MhtPart(all0_[beg:beg+i - beg - 2].strip())
                if (pa.content_location is not None): 
                    res.append(pa)
                if (first): 
                    break
            i += len(bound)
            while i < len(all0_): 
                if (not Utils.isWhitespace(all0_[i])): 
                    break
                i += 1
            beg = i
        return res
    
    @staticmethod
    def parse_all(fs : FileStream, bound : bytearray) -> typing.List['MhtPart']:
        return None