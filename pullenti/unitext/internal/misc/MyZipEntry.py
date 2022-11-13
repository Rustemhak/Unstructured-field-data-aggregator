# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class MyZipEntry:
    
    def __init__(self, zip0__ : 'MyZipFile') -> None:
        self.zip0_ = None;
        self.name = None;
        self.data = None;
        self.uncompress_data_size = 0
        self.pos = 0
        self.compress_data_size = 0
        self.encrypted = False
        self.is_directory = False
        self.method = 0
        self.zip0_ = zip0__
    
    def __str__(self) -> str:
        return "{0} ({1})".format(self.name, self.uncompress_data_size)
    
    def get_data(self) -> bytearray:
        if (self.data is not None): 
            return self.data
        return self.zip0_.unzip(self)