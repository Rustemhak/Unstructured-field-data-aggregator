# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.UpdateCommand import UpdateCommand
from pullenti.unitext.internal.zip.ZipEntry import ZipEntry

class ZipUpdate:
    
    def __init__(self, entry_ : 'ZipEntry', command_ : 'UpdateCommand'=UpdateCommand.ADD, data_source : 'IStaticDataSource'=None, file_name : str=None, str0_ : Stream=None) -> None:
        self.__entry_ = None;
        self.__out_entry_ = None;
        self.__command_ = UpdateCommand.COPY
        self.__data_source_ = None;
        self.__stream = None;
        self.__filename_ = None;
        self.__size_patch_offset_ = -1
        self.__crc_patch_offset_ = -1
        self.__offset_based_size = -1
        self.__data_source_ = data_source
        self.__filename_ = file_name
        self.__command_ = command_
        self.__stream = str0_
        self.__entry_ = (entry_.clone())
    
    @property
    def entry(self) -> 'ZipEntry':
        return self.__entry_
    
    @property
    def out_entry(self) -> 'ZipEntry':
        if (self.__out_entry_ is None): 
            self.__out_entry_ = (self.__entry_.clone())
        return self.__out_entry_
    
    @property
    def command(self) -> 'UpdateCommand':
        return self.__command_
    
    @property
    def filename(self) -> str:
        return self.__filename_
    
    @property
    def size_patch_offset(self) -> int:
        return self.__size_patch_offset_
    @size_patch_offset.setter
    def size_patch_offset(self, value) -> int:
        self.__size_patch_offset_ = value
        return value
    
    @property
    def crc_patch_offset(self) -> int:
        return self.__crc_patch_offset_
    @crc_patch_offset.setter
    def crc_patch_offset(self, value) -> int:
        self.__crc_patch_offset_ = value
        return value
    
    @property
    def offset_based_size(self) -> int:
        return self.__offset_based_size
    @offset_based_size.setter
    def offset_based_size(self, value) -> int:
        self.__offset_based_size = value
        return value
    
    def get_source(self) -> Stream:
        if (self.__stream is not None): 
            return self.__stream
        result = None
        if (self.__data_source_ is not None): 
            result = self.__data_source_.get_source()
        return result