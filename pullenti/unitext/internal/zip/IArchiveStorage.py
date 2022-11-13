# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Streams import Stream

class IArchiveStorage(object):
    """ Defines facilities for data storage when updating Zip Archives. """
    
    @property
    def update_mode(self) -> 'FileUpdateMode':
        """ Get the <see cref="FileUpdateMode"/> to apply during updates. """
        return None
    
    def get_temporary_output(self) -> Stream:
        """ Get an empty <see cref="Stream"/> that can be used for temporary output.
        
        Returns:
            Stream: Returns a temporary output <see cref="Stream"/>
        """
        return None
    
    def convert_temporary_to_final(self) -> Stream:
        """ Convert a temporary output stream to a final stream.
        
        Returns:
            Stream: The resulting final <see cref="Stream"/>
        """
        return None
    
    def make_temporary_copy(self, stream : Stream) -> Stream:
        """ Make a temporary copy of the original stream.
        
        Args:
            stream(Stream): The <see cref="Stream"/> to copy.
        
        Returns:
            Stream: Returns a temporary output <see cref="Stream"/> that is a copy of the input.
        """
        return None
    
    def open_for_direct_update(self, stream : Stream) -> Stream:
        """ Return a stream suitable for performing direct updates on the original source.
        
        Args:
            stream(Stream): The current stream.
        
        Returns:
            Stream: Returns a stream suitable for direct updating.
        """
        return None
    def __enter__(self): return self
    def __exit__(self, typ, val, traceback): pass # ERROR: Dispose method not found in class