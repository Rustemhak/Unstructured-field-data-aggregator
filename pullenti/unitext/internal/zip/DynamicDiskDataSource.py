# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import pathlib
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.IDynamicDataSource import IDynamicDataSource

class DynamicDiskDataSource(IDynamicDataSource):
    """ Default implementation of <see cref="IDynamicDataSource"/> for files stored on disk. """
    
    def __init__(self) -> None:
        """ Initialise a default instance of <see cref="DynamicDiskDataSource"/>. """
        pass
    
    def get_source(self, entry : 'ZipEntry', name : str) -> Stream:
        """ Get a <see cref="Stream"/> providing data for an entry.
        
        Args:
            entry(ZipEntry): The entry to provide data for.
            name(str): The file name for data if known.
        
        Returns:
            Stream: Returns a stream providing data; or null if not available
        """
        result = None
        if (name is not None): 
            result = (FileStream(name, "rb"))
        return result