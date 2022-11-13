# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.zip.ITaggedData import ITaggedData

class RawTaggedData(ITaggedData):
    # A raw binary tagged value
    
    def __init__(self, tag : int) -> None:
        self.__tag = 0
        self.__m_data = None;
        self.__tag = tag
    
    @property
    def tagid(self) -> int:
        return self.__tag
    @tagid.setter
    def tagid(self, value) -> int:
        self.__tag = value
        return value
    
    def set_data(self, data : bytearray, offset : int, count : int) -> None:
        if (data is None): 
            raise Exception("data")
        self.__m_data = Utils.newArrayOfBytes(count, 0)
        Utils.copyArray(data, offset, self.__m_data, 0, count)
    
    def get_data(self) -> bytearray:
        return self.__m_data
    
    @property
    def _data(self) -> bytearray:
        return self.__m_data
    @_data.setter
    def _data(self, value) -> bytearray:
        self.__m_data = value
        return value