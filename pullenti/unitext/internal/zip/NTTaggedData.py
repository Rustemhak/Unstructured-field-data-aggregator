# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import datetime

from pullenti.unitext.internal.zip.ITaggedData import ITaggedData

class NTTaggedData(ITaggedData):
    # Class handling NT date time values.
    
    def __init__(self) -> None:
        self.__last_access_time = datetime.datetime.min
        self.__last_modification_time = datetime.datetime.min
        self.__create_time = datetime.datetime.min
    
    @property
    def tagid(self) -> int:
        return 10
    
    def set_data(self, data : bytearray, index : int, count : int) -> None:
        pass
    
    def get_data(self) -> bytearray:
        return None
    
    @staticmethod
    def is_valid_value(value : datetime.datetime) -> bool:
        return True
    
    @property
    def last_modification_time(self) -> datetime.datetime:
        return self.__last_modification_time
    @last_modification_time.setter
    def last_modification_time(self, value) -> datetime.datetime:
        if (not NTTaggedData.is_valid_value(value)): 
            raise Exception("value")
        self.__last_modification_time = value
        return value
    
    @property
    def create_time(self) -> datetime.datetime:
        return self.__create_time
    @create_time.setter
    def create_time(self, value) -> datetime.datetime:
        if (not NTTaggedData.is_valid_value(value)): 
            raise Exception("value")
        self.__create_time = value
        return value
    
    @property
    def last_access_time(self) -> datetime.datetime:
        return self.__last_access_time
    @last_access_time.setter
    def last_access_time(self, value) -> datetime.datetime:
        if (not NTTaggedData.is_valid_value(value)): 
            raise Exception("value")
        self.__last_access_time = value
        return value