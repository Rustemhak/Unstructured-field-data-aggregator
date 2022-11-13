# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class EntryPatchData:
    
    def __init__(self) -> None:
        self.__size_patch_offset_ = 0
        self.__crc_patch_offset_ = 0
    
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