# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class DescriptorData:
    # Holds data pertinent to a data descriptor.
    
    def __init__(self) -> None:
        self.__m_size = 0
        self.__m_compressed_size = 0
        self.__m_crc = 0
    
    @property
    def compressed_size(self) -> int:
        return self.__m_compressed_size
    @compressed_size.setter
    def compressed_size(self, value) -> int:
        self.__m_compressed_size = value
        return value
    
    @property
    def size(self) -> int:
        return self.__m_size
    @size.setter
    def size(self, value) -> int:
        self.__m_size = value
        return value
    
    @property
    def crc(self) -> int:
        return self.__m_crc
    @crc.setter
    def crc(self, value) -> int:
        self.__m_crc = value
        return value