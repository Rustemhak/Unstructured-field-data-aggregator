# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.IArchiveStorage import IArchiveStorage
from pullenti.unitext.internal.zip.FileUpdateMode import FileUpdateMode

class BaseArchiveStorage(IArchiveStorage):
    """ An abstract <see cref="IArchiveStorage"/> suitable for extension by inheritance. """
    
    def __init__(self, update_mode_ : 'FileUpdateMode') -> None:
        """ Initializes a new instance of the <see cref="BaseArchiveStorage"/> class.
        
        Args:
            update_mode_(FileUpdateMode): The update mode.
        """
        self.__update_mode_ = FileUpdateMode.SAFE
        self.__update_mode_ = update_mode_
    
    def get_temporary_output(self) -> Stream:
        """ Gets a temporary output <see cref="Stream"/>
        
        Returns:
            Stream: Returns the temporary output stream.
        """
        return None
    
    def convert_temporary_to_final(self) -> Stream:
        """ Converts the temporary <see cref="Stream"/> to its final form.
        
        Returns:
            Stream: Returns a <see cref="Stream"/> that can be used to read
        the final storage for the archive.
        """
        return None
    
    def make_temporary_copy(self, stream : Stream) -> Stream:
        """ Make a temporary copy of a <see cref="Stream"/>.
        
        Args:
            stream(Stream): The <see cref="Stream"/> to make a copy of.
        
        Returns:
            Stream: Returns a temporary output <see cref="Stream"/> that is a copy of the input.
        """
        return None
    
    def open_for_direct_update(self, stream : Stream) -> Stream:
        """ Return a stream suitable for performing direct updates on the original source.
        
        Args:
            stream(Stream): The <see cref="Stream"/> to open for direct update.
        
        Returns:
            Stream: Returns a stream suitable for direct updating.
        """
        return None
    
    def close(self) -> None:
        """ Disposes this instance. """
        pass
    
    @property
    def update_mode(self) -> 'FileUpdateMode':
        """ Gets the update mode applicable. """
        return self.__update_mode_