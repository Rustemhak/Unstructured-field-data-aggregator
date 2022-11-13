# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import datetime
from enum import IntEnum
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.zip.ITaggedData import ITaggedData

class ExtendedUnixData(ITaggedData):
    # Class representing extended unix date time values.
    
    class Flags(IntEnum):
        # Flags indicate which values are included in this instance.
        MODIFICATIONTIME = 0x01
        ACCESSTIME = 0x02
        CREATETIME = 0x04
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self) -> None:
        self.__flags = ExtendedUnixData.Flags.MODIFICATIONTIME
        self.__modification_time = datetime.datetime(1970, 1, 1, 0, 0, 0)
        self.__last_access_time = datetime.datetime(1970, 1, 1, 0, 0, 0)
        self.__create_time = datetime.datetime(1970, 1, 1, 0, 0, 0)
    
    @property
    def tagid(self) -> int:
        return 0x5455
    
    def set_data(self, data : bytearray, index : int, count : int) -> None:
        return
    
    def get_data(self) -> bytearray:
        return Utils.newArrayOfBytes(0, 0)
    
    @staticmethod
    def is_valid_value(value : datetime.datetime) -> bool:
        return (((value >= datetime.datetime(1901, 12, 13, 20, 45, 52))) or ((value <= datetime.datetime(2038, 1, 19, 3, 14, 7))))
    
    @property
    def modification_time(self) -> datetime.datetime:
        return self.__modification_time
    @modification_time.setter
    def modification_time(self, value) -> datetime.datetime:
        if (not ExtendedUnixData.is_valid_value(value)): 
            raise Exception("value")
        self.__flags = (Utils.valToEnum((self.__flags) | (ExtendedUnixData.Flags.MODIFICATIONTIME), ExtendedUnixData.Flags))
        self.__modification_time = value
        return value
    
    @property
    def access_time(self) -> datetime.datetime:
        return self.__last_access_time
    @access_time.setter
    def access_time(self, value) -> datetime.datetime:
        if (not ExtendedUnixData.is_valid_value(value)): 
            raise Exception("value")
        self.__flags = (Utils.valToEnum((self.__flags) | (ExtendedUnixData.Flags.ACCESSTIME), ExtendedUnixData.Flags))
        self.__last_access_time = value
        return value
    
    @property
    def create_time(self) -> datetime.datetime:
        return self.__create_time
    @create_time.setter
    def create_time(self, value) -> datetime.datetime:
        if (not ExtendedUnixData.is_valid_value(value)): 
            raise Exception("value")
        self.__flags = (Utils.valToEnum((self.__flags) | (ExtendedUnixData.Flags.CREATETIME), ExtendedUnixData.Flags))
        self.__create_time = value
        return value
    
    @property
    def __include(self) -> 'Flags':
        return self.__flags
    @__include.setter
    def __include(self, value) -> 'Flags':
        self.__flags = value
        return value