# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.IStaticDataSource import IStaticDataSource

class StaticDiskDataSource(IStaticDataSource):
    """ Default implementation of a <see cref="IStaticDataSource"/> for use with files stored on disk. """
    
    def __init__(self, file_name : str) -> None:
        """ Initialise a new instnace of <see cref="StaticDiskDataSource"/>
        
        Args:
            file_name(str): The name of the file to obtain data from.
        """
        self.__file_name_ = None;
        self.__file_name_ = file_name
    
    def get_source(self) -> Stream:
        """ Get a <see cref="Stream"/> providing data.
        
        Returns:
            Stream: Returns a <see cref="Stream"/> provising data.
        """
        return FileStream(self.__file_name_, "rb")