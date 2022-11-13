# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class IEntryFactory:
    # Defines factory methods for creating new <see cref="ZipEntry"></see> values.
    
    def make_file_entry(self, file_name : str) -> 'ZipEntry':
        return None
    
    def make_file_entry_ex(self, file_name : str, use_file_system : bool) -> 'ZipEntry':
        return None
    
    def make_directory_entry(self, directory_name : str) -> 'ZipEntry':
        return None
    
    def make_directory_entry_ex(self, directory_name : str, use_file_system : bool) -> 'ZipEntry':
        return None
    
    @property
    def name_transform(self) -> 'INameTransform':
        return None
    @name_transform.setter
    def name_transform(self, value) -> 'INameTransform':
        return value