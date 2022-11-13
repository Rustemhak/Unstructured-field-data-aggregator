# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.unitext.internal.zip.ZipConstants import ZipConstants

class ZipString:
    # Represents a string from a <see cref="ZipFile"/> which is stored as an array of bytes.
    
    def __init__(self, comment : str) -> None:
        self.__comment_ = None;
        self.__raw_comment_ = None;
        self.__is_source_string_ = False
        self.__comment_ = comment
        self.__is_source_string_ = True
    
    @property
    def is_source_string(self) -> bool:
        return self.__is_source_string_
    
    @property
    def raw_length(self) -> int:
        self.__make_bytes_available()
        return len(self.__raw_comment_)
    
    @property
    def raw_comment(self) -> bytearray:
        self.__make_bytes_available()
        return self.__raw_comment_
    
    def reset(self) -> None:
        if (self.__is_source_string_): 
            self.__raw_comment_ = (None)
        else: 
            self.__comment_ = (None)
    
    def __make_text_available(self) -> None:
        if (self.__comment_ is None): 
            self.__comment_ = ZipConstants.convert_to_string0(self.__raw_comment_)
    
    def __make_bytes_available(self) -> None:
        if (self.__raw_comment_ is None): 
            self.__raw_comment_ = ZipConstants.convert_to_array_str(self.__comment_)
    
    @staticmethod
    def ooString(zip_string : 'ZipString') -> str:
        zip_string.__make_text_available()
        return zip_string.__comment_