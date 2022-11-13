# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Streams import Stream

class IDynamicDataSource:
    """ Represents a source of data that can dynamically provide
    multiple <see cref="Stream">data sources</see> based on the parameters passed. """
    
    def get_source(self, entry : 'ZipEntry', name : str) -> Stream:
        """ Get a data source.
        
        Args:
            entry(ZipEntry): The <see cref="ZipEntry"/> to get a source for.
            name(str): The name for data if known.
        
        Returns:
            Stream: Returns a <see cref="Stream"/> to use for compression input.
        """
        return None