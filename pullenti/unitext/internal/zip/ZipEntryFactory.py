# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import datetime
import pathlib
from enum import IntEnum

from pullenti.unitext.internal.zip.IEntryFactory import IEntryFactory
from pullenti.unitext.internal.zip.INameTransform import INameTransform
from pullenti.unitext.internal.zip.ZipEntry import ZipEntry
from pullenti.unitext.internal.zip.ZipNameTransform import ZipNameTransform

class ZipEntryFactory(IEntryFactory):
    # Basic implementation of <see cref="IEntryFactory"></see>
    
    class TimeSetting(IntEnum):
        """ Defines the possible values to be used for the <see cref="ZipEntry.DateTime"/>. """
        LASTWRITETIME = 0
        """ Use the recorded LastWriteTime value for the file. """
        LASTWRITETIMEUTC = 1
        """ Use the recorded LastWriteTimeUtc value for the file """
        CREATETIME = 2
        """ Use the recorded CreateTime value for the file. """
        CREATETIMEUTC = 3
        """ Use the recorded CreateTimeUtc value for the file. """
        LASTACCESSTIME = 4
        """ Use the recorded LastAccessTime value for the file. """
        LASTACCESSTIMEUTC = 5
        """ Use the recorded LastAccessTimeUtc value for the file. """
        FIXED = 6
        """ Use a fixed value. """
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, time_setting : 'TimeSetting'=TimeSetting.LASTWRITETIME) -> None:
        self.__name_transform_ = None;
        self.__fixed_date_time_ = datetime.datetime.now()
        self.__time_setting_ = ZipEntryFactory.TimeSetting.LASTWRITETIME
        self.__is_unicode_text_ = True
        self.__get_attributes_ = -1
        self.__set_attributes_ = 0
        self.__time_setting_ = time_setting
        self.__name_transform_ = (ZipNameTransform())
    
    @property
    def name_transform(self) -> 'INameTransform':
        return self.__name_transform_
    @name_transform.setter
    def name_transform(self, value) -> 'INameTransform':
        if (value is None): 
            self.__name_transform_ = (ZipNameTransform())
        else: 
            self.__name_transform_ = value
        return value
    
    @property
    def setting(self) -> 'TimeSetting':
        return self.__time_setting_
    @setting.setter
    def setting(self, value) -> 'TimeSetting':
        self.__time_setting_ = value
        return value
    
    @property
    def fixed_date_time(self) -> datetime.datetime:
        return self.__fixed_date_time_
    @fixed_date_time.setter
    def fixed_date_time(self, value) -> datetime.datetime:
        if (value.year < 1970): 
            raise Exception("Value is too old to be valid", "value")
        self.__fixed_date_time_ = value
        return value
    
    @property
    def get_attributes(self) -> int:
        return self.__get_attributes_
    @get_attributes.setter
    def get_attributes(self, value) -> int:
        self.__get_attributes_ = value
        return value
    
    @property
    def set_attributes(self) -> int:
        return self.__set_attributes_
    @set_attributes.setter
    def set_attributes(self, value) -> int:
        self.__set_attributes_ = value
        return value
    
    @property
    def is_unicode_text(self) -> bool:
        return self.__is_unicode_text_
    @is_unicode_text.setter
    def is_unicode_text(self, value) -> bool:
        self.__is_unicode_text_ = value
        return value
    
    def make_file_entry(self, file_name : str) -> 'ZipEntry':
        return self.make_file_entry_ex(file_name, True)
    
    def make_file_entry_ex(self, file_name : str, use_file_system : bool) -> 'ZipEntry':
        result = ZipEntry(self.__name_transform_.transform_file(file_name))
        result.is_unicode_text = self.__is_unicode_text_
        external_attributes = 0
        use_attributes = (self.__set_attributes_ != 0)
        fi = None
        if (use_file_system): 
            fi = pathlib.Path(file_name)
        if (((fi is not None)) and fi.is_file()): 
            result.size = fi.stat().st_size
            use_attributes = True
        elif (self.__time_setting_ == ZipEntryFactory.TimeSetting.FIXED): 
            result.date_time = self.__fixed_date_time_
        if (use_attributes): 
            external_attributes |= self.__set_attributes_
            result.external_file_attributes = external_attributes
        return result
    
    def make_directory_entry(self, directory_name : str) -> 'ZipEntry':
        return self.make_directory_entry_ex(directory_name, True)
    
    def make_directory_entry_ex(self, directory_name : str, use_file_system : bool) -> 'ZipEntry':
        result = ZipEntry(self.__name_transform_.transform_directory(directory_name))
        result.is_unicode_text = self.__is_unicode_text_
        result.size = 0
        external_attributes = 0
        di = None
        if (use_file_system): 
            di = pathlib.Path(directory_name)
        external_attributes |= ((self.__set_attributes_ | 16))
        result.external_file_attributes = external_attributes
        return result