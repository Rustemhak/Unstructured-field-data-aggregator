# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Streams import Stream

class IStaticDataSource:
    """ Provides a static way to obtain a source of data for an entry. """
    
    def get_source(self) -> Stream:
        """ Get a source of data by creating a new stream.
        
        Returns:
            Stream: Returns a <see cref="Stream"/> to use for compression input.
        """
        return None