# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

class ExtendedName:
    # Provides name class for Compound File Storage.
    
    @property
    def name(self) -> typing.List['char']:
        return self.__m_name
    
    def __init__(self, sname : str, name_ : typing.List['char'], offset : int=0, count : int=-1) -> None:
        self.__m_name = None;
        if (sname is not None): 
            self.__m_name = sname
        else: 
            if (name_ is None): 
                raise Exception("name")
            if (count < 0): 
                count = len(name_)
            self.__m_name = Utils.newArray(count, None)
            Utils.copyArray(name_, offset, self.__m_name, 0, count)
    
    def __str__(self) -> str:
        return str(self.__m_name)
    
    def to_char_array(self) -> typing.List['char']:
        return self.__m_name.clone()
    
    def to_escaped_string(self) -> str:
        sb = io.StringIO()
        for ch in self.__m_name: 
            if ((ch < ' ') or ch == '\\'): 
                print("{:4X}".format(ord(ch)), end="", file=print("\\u", end="", file=sb))
            else: 
                print(ch, end="", file=sb)
        return Utils.toStringStringIO(sb)
    
    @staticmethod
    def from_string(name_ : str) -> 'ExtendedName':
        return ExtendedName(name_, None, 0, -1)
    
    @staticmethod
    def from_escaped_string(name_ : str) -> 'ExtendedName':
        sb = io.StringIO()
        i = 0
        while i < len(name_):
            if (name_[i] != '\\'): 
                print(name_[i], end="", file=sb)
            else: 
                if ((i + 6) > len(name_) or name_[i + 1] != 'u'): 
                    raise Exception("Invalid escaped string format")
                code = int(name_[i + 2:i + 2+4])
                print(chr(code), end="", file=sb)
        return ExtendedName(Utils.toStringStringIO(sb), None, 0, -1)
    
    def __hash__(self) -> int:
        hash0_ = len(self.__m_name)
        i = 0
        while i < len(self.__m_name): 
            hash0_ ^= (ord(self.__m_name[i]))
            i += 1
        return hash0_
    
    def equals(self, obj : object) -> bool:
        return self == (obj)
    
    def __eq__(self : 'ExtendedName', n2 : 'ExtendedName') -> bool:
        if (len(self.__m_name) != len(n2.__m_name)): 
            return False
        i = 0
        while i < len(self.__m_name): 
            if (self.__m_name[i] != n2.__m_name[i]): 
                return False
            i += 1
        return True
    
    def __ne__(self : 'ExtendedName', n2 : 'ExtendedName') -> bool:
        return not ((self == n2))