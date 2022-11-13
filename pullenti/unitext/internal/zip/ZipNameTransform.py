# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.unitext.internal.zip.INameTransform import INameTransform

class ZipNameTransform(INameTransform):
    """ ZipNameTransform transforms names as per the Zip file naming convention. """
    
    def __init__(self, trim_prefix_ : str=None) -> None:
        """ Initialize a new instance of <see cref="ZipNameTransform"></see>
        
        Args:
            trim_prefix_(str): The string to trim from the front of paths if found.
        """
        self.__trim_prefix_ = None;
        self.trim_prefix = trim_prefix_
    
    def transform_directory(self, name : str) -> str:
        """ Transform a windows directory name according to the Zip file naming conventions.
        
        Args:
            name(str): The directory name to transform.
        
        Returns:
            str: The transformed name.
        """
        name = self.transform_file(name)
        if (len(name) > 0): 
            if (not name.endswith("/")): 
                name += "/"
        else: 
            raise Utils.newException("Cannot have an empty directory name", None)
        return name
    
    def transform_file(self, name : str) -> str:
        """ Transform a windows file name according to the Zip file naming conventions.
        
        Args:
            name(str): The file name to transform.
        
        Returns:
            str: The transformed name.
        """
        if (name is not None): 
            lower_name = name.lower()
            if (((self.__trim_prefix_ is not None)) and ((lower_name.find(self.__trim_prefix_) == 0))): 
                name = name[len(self.__trim_prefix_):]
            name = name.replace("\\", "/")
            while ((len(name) > 0)) and ((name[0] == '/')):
                name = name[1:]
            while ((len(name) > 0)) and ((name[len(name) - 1] == '/')):
                name = name[0:0+len(name) - 1]
            index = name.find("//")
            while index >= 0:
                name = (name[0:0+index] + name[index + 1:])
                index = name.find("//")
            name = ZipNameTransform.__make_valid_name(name, '_')
        else: 
            name = ""
        return name
    
    @property
    def trim_prefix(self) -> str:
        """ Get/set the path prefix to be trimmed from paths if present. """
        return self.__trim_prefix_
    @trim_prefix.setter
    def trim_prefix(self, value) -> str:
        self.__trim_prefix_ = value
        if (self.__trim_prefix_ is not None): 
            self.__trim_prefix_ = self.__trim_prefix_.lower()
        return value
    
    @staticmethod
    def __make_valid_name(name : str, replacement : 'char') -> str:
        """ Force a name to be valid by replacing invalid characters with a fixed value
        
        Args:
            name(str): The name to force valid
            replacement('char'): The replacement character to use.
        
        Returns:
            str: Returns a valid name
        """
        index = Utils.indexOfAny(name, ZipNameTransform.__invalid_entry_chars, 0, 0)
        if (index >= 0): 
            builder = Utils.newStringIO(name)
            while index >= 0:
                Utils.setCharAtStringIO(builder, index, replacement)
                if (index >= len(name)): 
                    index = -1
                else: 
                    index = Utils.indexOfAny(name, ZipNameTransform.__invalid_entry_chars, index + 1, 0)
            name = Utils.toStringStringIO(builder)
        if (len(name) > 0xffff): 
            raise Utils.newException("PathTooLong", None)
        return name
    
    @staticmethod
    def is_valid_name_ex(name : str, relaxed : bool) -> bool:
        """ Test a name to see if it is a valid name for a zip entry.
        
        Args:
            name(str): The name to test.
            relaxed(bool): If true checking is relaxed about windows file names and absolute paths.
        
        Returns:
            bool: Returns true if the name is a valid zip name; false otherwise.
        """
        result = (name is not None)
        if (result): 
            if (relaxed): 
                result = (Utils.indexOfAny(name, ZipNameTransform.__invalid_entry_chars_relaxed, 0, 0) < 0)
            else: 
                result = (((Utils.indexOfAny(name, ZipNameTransform.__invalid_entry_chars, 0, 0) < 0)) and ((name.find('/') != 0)))
        return result
    
    @staticmethod
    def is_valid_name(name : str) -> bool:
        """ Test a name to see if it is a valid name for a zip entry.
        
        Args:
            name(str): The name to test.
        
        Returns:
            bool: Returns true if the name is a valid zip name; false otherwise.
        """
        result = ((name is not None)) and ((Utils.indexOfAny(name, ZipNameTransform.__invalid_entry_chars, 0, 0) < 0)) and ((name.find('/') != 0))
        return result
    
    __invalid_entry_chars = None
    
    __invalid_entry_chars_relaxed = None
    
    # static constructor for class ZipNameTransform
    @staticmethod
    def _static_ctor():
        invalid_path_chars = [ ]
        invalid_path_chars = Utils.newArray(0, None)
        how_many = len(invalid_path_chars) + 2
        ZipNameTransform.__invalid_entry_chars_relaxed = Utils.newArray(how_many, None)
        Utils.copyArray(invalid_path_chars, 0, ZipNameTransform.__invalid_entry_chars_relaxed, 0, len(invalid_path_chars))
        ZipNameTransform.__invalid_entry_chars_relaxed[how_many - 1] = '*'
        ZipNameTransform.__invalid_entry_chars_relaxed[how_many - 2] = '?'
        how_many = (len(invalid_path_chars) + 4)
        ZipNameTransform.__invalid_entry_chars = Utils.newArray(how_many, None)
        Utils.copyArray(invalid_path_chars, 0, ZipNameTransform.__invalid_entry_chars, 0, len(invalid_path_chars))
        ZipNameTransform.__invalid_entry_chars[how_many - 1] = ':'
        ZipNameTransform.__invalid_entry_chars[how_many - 2] = '\\'
        ZipNameTransform.__invalid_entry_chars[how_many - 3] = '*'
        ZipNameTransform.__invalid_entry_chars[how_many - 4] = '?'

ZipNameTransform._static_ctor()