# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.unitext.internal.misc.MyXmlNodeType import MyXmlNodeType
from pullenti.util.EncodingStandard import EncodingStandard
from pullenti.util.EncodingWrapper import EncodingWrapper

class MyXmlReader:
    
    def __init__(self) -> None:
        self.__m_tmp = io.StringIO()
        self.__m_tmp2 = None;
        self.__m_text = None;
        self.__m_pos = 0
        self.node_type = MyXmlNodeType.NONE
        self.local_name = None;
        self.value = None;
        self.attributes = dict()
        self.is_empty_element = False
    
    @staticmethod
    def create(data : bytearray) -> 'MyXmlReader':
        res = MyXmlReader()
        hlen = 0
        wraphlen99 = RefOutArgWrapper(0)
        enc = EncodingWrapper.check_encoding(data, wraphlen99)
        hlen = wraphlen99.value
        if (enc is None): 
            enc = EncodingWrapper(EncodingStandard.ACSII)
        res.__m_text = enc.get_string(data, hlen, len(data) - hlen)
        res.__m_pos = 0
        while True:
            if (not res.__read_head()): 
                break
        return res
    
    def __goto_nonsp(self) -> None:
        while self.__m_pos < len(self.__m_text): 
            if (not Utils.isWhitespace(self.__m_text[self.__m_pos])): 
                break
            self.__m_pos += 1
    
    def __read_head(self) -> bool:
        self.__goto_nonsp()
        if (((self.__m_pos + 10) < len(self.__m_text)) and self.__m_text[self.__m_pos] == '<' and self.__m_text[self.__m_pos + 1] == '?'): 
            self.__m_pos += 2
            while self.__m_pos < len(self.__m_text): 
                if (self.__m_text[self.__m_pos] == '>' and self.__m_text[self.__m_pos - 1] == '?'): 
                    self.__m_pos += 1
                    return True
                self.__m_pos += 1
        return False
    
    __m_char0 = chr(0)
    
    def __read_name(self) -> str:
        self.__goto_nonsp()
        Utils.setLengthStringIO(self.__m_tmp, 0)
        while self.__m_pos < len(self.__m_text): 
            ch = self.__m_text[self.__m_pos]
            if (str.isalpha(ch) or ch == '_'): 
                print(ch, end="", file=self.__m_tmp)
            elif (self.__m_tmp.tell() > 0 and ((str.isdigit(ch) or ch == '-' or ch == ':'))): 
                print(ch, end="", file=self.__m_tmp)
            else: 
                break
            self.__m_pos += 1
        if (self.__m_tmp.tell() > 0): 
            return Utils.toStringStringIO(self.__m_tmp)
        return None
    
    def __read_char(self) -> 'char':
        if (self.__m_pos >= len(self.__m_text)): 
            return MyXmlReader.__m_char0
        ch = self.__m_text[self.__m_pos]
        self.__m_pos += 1
        if (ch != '&'): 
            return ch
        if (self.__m_pos >= len(self.__m_text)): 
            return ch
        if (self.__m_tmp2 is None): 
            self.__m_tmp2 = io.StringIO()
        Utils.setLengthStringIO(self.__m_tmp2, 0)
        while self.__m_pos < len(self.__m_text): 
            if (self.__m_text[self.__m_pos] == ';'): 
                self.__m_pos += 1
                break
            else: 
                print(self.__m_text[self.__m_pos], end="", file=self.__m_tmp2)
            self.__m_pos += 1
        txt = Utils.toStringStringIO(self.__m_tmp2).upper()
        if (txt == "LT"): 
            return '<'
        if (txt == "GT"): 
            return '>'
        if (txt == "AMP"): 
            return '&'
        if (txt == "QUOT"): 
            return '"'
        if (txt == "APOS"): 
            return '\''
        if (txt == "NBSP"): 
            return chr(0xA0)
        if (len(txt) == 0): 
            return MyXmlReader.__m_char0
        if (txt[0] == 'X'): 
            cod = 0
            i = 1
            while i < len(txt): 
                if (str.isdigit(txt[i])): 
                    cod = (((cod * 16) + (ord(txt[i]))) - 0x30)
                elif ((ord(txt[i])) >= 0x41 and (ord(txt[i])) <= 0x46): 
                    cod = ((((cod * 16) + (ord(txt[i]))) - 0x41) + 10)
                i += 1
            return chr(cod)
        if (str.isdigit(txt[0])): 
            cod = 0
            i = 1
            while i < len(txt): 
                if (str.isdigit(txt[i])): 
                    cod = (((cod * 10) + (ord(txt[i]))) - 0x30)
                i += 1
            return chr(cod)
        return txt[0]
    
    def __read_value(self, attr_char : 'char') -> str:
        Utils.setLengthStringIO(self.__m_tmp, 0)
        while self.__m_pos < len(self.__m_text): 
            ch = self.__m_text[self.__m_pos]
            if (attr_char == ch): 
                self.__m_pos += 1
                break
            if (attr_char == MyXmlReader.__m_char0): 
                if (ch == '<'): 
                    break
            ch = self.__read_char()
            if (ch != MyXmlReader.__m_char0): 
                print(ch, end="", file=self.__m_tmp)
            else: 
                break
        return Utils.toStringStringIO(self.__m_tmp)
    
    def __read_attr(self, nam : str, val : str) -> bool:
        val.value = (None)
        pos = self.__m_pos
        nam.value = self.__read_name()
        if (nam.value is None): 
            return False
        self.__goto_nonsp()
        if (self.__m_pos >= len(self.__m_text) or self.__m_text[self.__m_pos] != '='): 
            return False
        self.__m_pos += 1
        self.__goto_nonsp()
        if (self.__m_pos < len(self.__m_text)): 
            ch = self.__m_text[self.__m_pos]
            if (ch == '"' or ch == '\''): 
                self.__m_pos += 1
                val.value = self.__read_value(ch)
                if (val.value is not None): 
                    if ((self.__m_pos < len(self.__m_text)) and self.__m_text[self.__m_pos] == ch): 
                        self.__m_pos += 1
                    return True
        self.__m_pos = pos
        return False
    
    def read(self) -> bool:
        self.attributes.clear()
        self.is_empty_element = False
        self.local_name = (None)
        self.value = (None)
        self.node_type = MyXmlNodeType.NONE
        if (self.__m_pos >= len(self.__m_text)): 
            return False
        ch = self.__m_text[self.__m_pos]
        if (ch != '<'): 
            self.value = self.__read_value(MyXmlReader.__m_char0)
            if (self.value is not None): 
                self.node_type = MyXmlNodeType.TEXT
                self.local_name = "#text"
                return True
            return False
        self.__m_pos += 1
        if ((self.__m_pos + 3) > len(self.__m_text)): 
            return False
        ch = self.__m_text[self.__m_pos]
        if (ch == '/'): 
            self.__m_pos += 1
            self.local_name = self.__read_name()
            self.__goto_nonsp()
            if (self.local_name is not None and (self.__m_pos < len(self.__m_text)) and self.__m_text[self.__m_pos] == '>'): 
                self.node_type = MyXmlNodeType.ENDELEMENT
                self.__m_pos += 1
                return True
            return False
        self.local_name = self.__read_name()
        if (self.local_name is None): 
            return False
        self.node_type = MyXmlNodeType.ELEMENT
        while self.__m_pos < len(self.__m_text): 
            self.__goto_nonsp()
            if (self.__m_pos >= len(self.__m_text)): 
                break
            ch = self.__m_text[self.__m_pos]
            if (ch == '>'): 
                self.__m_pos += 1
                break
            if (ch == '/' and ((self.__m_pos + 1) < len(self.__m_text)) and self.__m_text[self.__m_pos + 1] == '>'): 
                self.is_empty_element = True
                self.__m_pos += 2
                break
            nam = None
            val = None
            wrapnam100 = RefOutArgWrapper(None)
            wrapval101 = RefOutArgWrapper(None)
            inoutres102 = self.__read_attr(wrapnam100, wrapval101)
            nam = wrapnam100.value
            val = wrapval101.value
            if (inoutres102): 
                if (not nam in self.attributes): 
                    self.attributes[nam] = val
            else: 
                break
        return True
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.node_type == MyXmlNodeType.ELEMENT): 
            print("<{0}".format(self.local_name), end="", file=tmp, flush=True)
            for kp in self.attributes.items(): 
                print(" {0}=\"{1}\"".format(kp[0], kp[1]), end="", file=tmp, flush=True)
            if (self.is_empty_element): 
                print(" />", end="", file=tmp)
            else: 
                print(">", end="", file=tmp)
        elif (self.node_type == MyXmlNodeType.ENDELEMENT): 
            print("</{0}>".format(self.local_name), end="", file=tmp, flush=True)
        elif (self.node_type == MyXmlNodeType.TEXT): 
            print("#text: {0}".format(Utils.ifNotNull(self.value, "")), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    def get_attribute(self, nam : str) -> str:
        if (nam in self.attributes): 
            return self.attributes[nam]
        return None