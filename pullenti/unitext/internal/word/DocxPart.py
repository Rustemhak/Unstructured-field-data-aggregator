# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
import io
from pullenti.unisharp.Utils import Utils

from pullenti.util.MiscHelper import MiscHelper

class DocxPart:
    """ Это блок данных """
    
    def __init__(self) -> None:
        self.name = None;
        self.xml0_ = None;
        self.data = None;
        self.zip_entry = None;
    
    def is_name(self, name_ : str) -> bool:
        if (Utils.compareStrings(name_, self.name, True) == 0): 
            return True
        if (self.name.startswith("/")): 
            if (Utils.compareStrings(name_, self.name[1:], True) == 0): 
                return True
        return False
    
    def is_name_starts(self, name_ : str) -> bool:
        if (Utils.startsWithString(self.name, name_, True)): 
            return True
        return False
    
    def __str__(self) -> str:
        return self.name
    
    @staticmethod
    def __start_of_ins(dat : bytearray, i : int) -> bool:
        if ((i + 7) >= len(dat)): 
            return False
        if ((((chr(dat[i])) == '<' and (chr(dat[i + 1])) == 'w' and (chr(dat[i + 2])) == ':') and (chr(dat[i + 3])) == 'i' and (chr(dat[i + 4])) == 'n') and (chr(dat[i + 5])) == 's'): 
            if ((chr(dat[i + 6])) == ' ' or (chr(dat[i + 6])) == '>'): 
                return True
        if ((((chr(dat[i])) == '<' and (chr(dat[i + 1])) == '/' and (chr(dat[i + 2])) == 'w') and (chr(dat[i + 3])) == ':' and (chr(dat[i + 4])) == 'i') and (chr(dat[i + 5])) == 'n' and (chr(dat[i + 6])) == 's'): 
            if ((chr(dat[i + 7])) == ' ' or (chr(dat[i + 7])) == '>'): 
                return True
        return False
    
    def get_xml_node(self, correct : bool=False) -> xml.etree.ElementTree.Element:
        if (self.xml0_ is not None): 
            return self.xml0_
        if (self.data is not None): 
            return None
        xml0__ = None # new XmlDocument
        dat = self.zip_entry.get_data()
        if (dat is None): 
            return None
        has_ins = False
        i = 0
        while i < (len(dat) - 6): 
            if (DocxPart.__start_of_ins(dat, i)): 
                has_ins = True
                break
            i += 1
        if (has_ins): 
            buf = bytearray()
            i = 0
            while i < len(dat): 
                if (not DocxPart.__start_of_ins(dat, i)): 
                    buf.append(dat[i])
                else: 
                    while i < len(dat): 
                        if ((chr(dat[i])) == '>'): 
                            break
                        i += 1
                i += 1
            dat = (bytearray(buf))
        str0_ = MiscHelper.decode_string_utf8(dat, 0, -1)
        if (str0_ is None): 
            return None
        ins_begin = list()
        ins_end = list()
        i = 0
        first_pass690 = True
        while True:
            if first_pass690: first_pass690 = False
            else: i += 1
            if (not (i < len(str0_))): break
            ch = str0_[i]
            if (ch != '<'): 
                continue
            j = 0
            j = (i + 1)
            while j < len(str0_): 
                if (str0_[j] == '>'): 
                    break
                j += 1
            if (j >= len(str0_)): 
                break
            t0 = j + 1
            has_not_ws = False
            i1 = 0
            i1 = t0
            while i1 < len(str0_): 
                if (str0_[i1] == '<'): 
                    break
                elif (not Utils.isWhitespace(str0_[i1])): 
                    has_not_ws = True
                i1 += 1
            if (not has_not_ws or i1 >= len(str0_)): 
                i = (i1 - 1)
                continue
            if (str0_[i1 + 1] == '/' and str0_[j - 1] != '/'): 
                nam1 = DocxPart.__get_tag_name(str0_, i + 1)
                nam2 = DocxPart.__get_tag_name(str0_, i1 + 2)
                if (nam1 is not None and nam1 == nam2): 
                    i = (i1 - 1)
                    continue
            ins_begin.append(t0)
            ins_end.append(i1)
            i = (i1 - 1)
        if (len(ins_begin) > 0): 
            tmp = io.StringIO()
            print(str0_, end="", file=tmp)
            for i in range(len(ins_begin) - 1, -1, -1):
                Utils.insertStringIO(tmp, ins_end[i], "</text:span>")
                Utils.insertStringIO(tmp, ins_begin[i], "<text:span>")
            str0_ = Utils.toStringStringIO(tmp)
        xml0__ = Utils.parseXmlFromString(str0_)
        return xml0__.getroot()
    
    @staticmethod
    def __get_tag_name(xml0__ : str, i : int) -> str:
        j = i
        while j < len(xml0__): 
            if (not str.isalpha(xml0__[j]) and xml0__[j] != ':'): 
                if (j == i): 
                    return None
                return xml0__[i:i+j - i]
            j += 1
        return None
    
    def get_bytes(self) -> bytearray:
        if (self.data is not None): 
            return self.data
        if (self.xml0_ is not None): 
            return None
        try: 
            return self.zip_entry.get_data()
        except Exception as ex: 
            return None
    
    @staticmethod
    def _new445(_arg1 : str, _arg2 : 'MyZipEntry') -> 'DocxPart':
        res = DocxPart()
        res.name = _arg1
        res.zip_entry = _arg2
        return res
    
    @staticmethod
    def _new446(_arg1 : str, _arg2 : xml.etree.ElementTree.Element) -> 'DocxPart':
        res = DocxPart()
        res.name = _arg1
        res.xml0_ = _arg2
        return res