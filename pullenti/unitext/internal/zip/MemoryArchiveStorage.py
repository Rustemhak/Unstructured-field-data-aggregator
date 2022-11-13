# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.unitext.internal.zip.BaseArchiveStorage import BaseArchiveStorage
from pullenti.unitext.internal.zip.StreamUtils import StreamUtils
from pullenti.unitext.internal.zip.FileUpdateMode import FileUpdateMode

class MemoryArchiveStorage(BaseArchiveStorage):
    """ An <see cref="IArchiveStorage"/> implementation suitable for in memory streams. """
    
    def __init__(self, update_mode_ : 'FileUpdateMode'=FileUpdateMode.DIRECT) -> None:
        """ Initializes a new instance of the <see cref="MemoryArchiveStorage"/> class.
        
        Args:
            update_mode_(FileUpdateMode): The <see cref="FileUpdateMode"/> to use
        """
        super().__init__(update_mode_)
        self.__temporary_stream_ = None;
        self.__final_stream_ = None;
    
    @property
    def final_stream(self) -> MemoryStream:
        """ Get the stream returned by <see cref="ConvertTemporaryToFinal"/> if this was in fact called. """
        return self.__final_stream_
    
    def get_temporary_output(self) -> Stream:
        """ Gets the temporary output <see cref="Stream"/>
        
        Returns:
            Stream: Returns the temporary output stream.
        """
        self.__temporary_stream_ = MemoryStream()
        return self.__temporary_stream_
    
    def convert_temporary_to_final(self) -> Stream:
        """ Converts the temporary <see cref="Stream"/> to its final form.
        
        Returns:
            Stream: Returns a <see cref="Stream"/> that can be used to read
        the final storage for the archive.
        """
        if (self.__temporary_stream_ is None): 
            raise Utils.newException("No temporary stream has been created", None)
        self.__final_stream_ = MemoryStream(self.__temporary_stream_.toarray())
        return self.__final_stream_
    
    def make_temporary_copy(self, stream : Stream) -> Stream:
        """ Make a temporary copy of the original stream.
        
        Args:
            stream(Stream): The <see cref="Stream"/> to copy.
        
        Returns:
            Stream: Returns a temporary output <see cref="Stream"/> that is a copy of the input.
        """
        self.__temporary_stream_ = MemoryStream()
        stream.position = 0
        StreamUtils.copy(stream, self.__temporary_stream_, Utils.newArrayOfBytes(4096, 0))
        return self.__temporary_stream_
    
    def open_for_direct_update(self, stream : Stream) -> Stream:
        """ Return a stream suitable for performing direct updates on the original source.
        
        Args:
            stream(Stream): The original source stream
        
        Returns:
            Stream: Returns a stream suitable for direct updating.
        """
        if (((stream is None)) or not stream.writable): 
            result = MemoryStream()
            if (stream is not None): 
                stream.position = 0
                StreamUtils.copy(stream, result, Utils.newArrayOfBytes(4096, 0))
                stream.close()
            return result
        else: 
            return stream
    
    def close(self) -> None:
        """ Disposes this instance. """
        if (self.__temporary_stream_ is not None): 
            self.__temporary_stream_.close()
            self.__temporary_stream_ = (None)