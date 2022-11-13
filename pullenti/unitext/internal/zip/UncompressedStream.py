# SDK Pullenti Unitext, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Streams import Stream

class UncompressedStream(Stream):
    """ An <see cref="UncompressedStream"/> is a stream that you can write uncompressed data
    to and flush, but cannot read, seek or do anything else to. """
    
    def __init__(self, base_stream : Stream) -> None:
        super().__init__()
        self.__base_stream_ = None;
        self.__base_stream_ = base_stream
    
    def close(self) -> None:
        """ Close this stream instance. """
        pass
    
    @property
    def can_read(self) -> bool:
        """ Gets a value indicating whether the current stream supports reading. """
        return False
    
    def flush(self) -> None:
        """ Write any buffered data to underlying storage. """
        self.__base_stream_.flush()
    
    @property
    def can_write(self) -> bool:
        """ Gets a value indicating whether the current stream supports writing. """
        return self.__base_stream_.writable
    
    @property
    def can_seek(self) -> bool:
        """ Gets a value indicating whether the current stream supports seeking. """
        return False
    
    @property
    def length(self) -> int:
        """ Get the length in bytes of the stream. """
        return 0
    
    @property
    def position(self) -> int:
        """ Gets or sets the position within the current stream. """
        return self.__base_stream_.position
    @position.setter
    def position(self, value) -> int:
        return value
    
    def read(self, buffer : bytearray, offset : int, count : int) -> int:
        """ Reads a sequence of bytes from the current stream and advances the position within the stream by the number of bytes read.
        
        Args:
            buffer(bytearray): An array of bytes. When this method returns, the buffer contains the specified byte array with the values between offset and (offset + count - 1) replaced by the bytes read from the current source.
            offset(int): The zero-based byte offset in buffer at which to begin storing the data read from the current stream.
            count(int): The maximum number of bytes to be read from the current stream.
        
        Returns:
            int: The total number of bytes read into the buffer. This can be less than the number of bytes requested if that many bytes are not currently available, or zero (0) if the end of the stream has been reached.
        """
        return 0
    
    def seek(self, offset : int, origin : int) -> int:
        """ Sets the position within the current stream.
        
        Args:
            offset(int): A byte offset relative to the origin parameter.
            origin(int): A value of type <see cref="T:System.IO.SeekOrigin"></see> indicating the reference point used to obtain the new position.
        
        Returns:
            int: The new position within the current stream.
        """
        return 0
    
    def set_length(self, value : int) -> None:
        """ Sets the length of the current stream.
        
        Args:
            value(int): The desired length of the current stream in bytes.
        """
        pass
    
    def write(self, buffer : bytearray, offset : int, count : int) -> None:
        """ Writes a sequence of bytes to the current stream and advances the current position within this stream by the number of bytes written.
        
        Args:
            buffer(bytearray): An array of bytes. This method copies count bytes from buffer to the current stream.
            offset(int): The zero-based byte offset in buffer at which to begin copying bytes to the current stream.
            count(int): The number of bytes to be written to the current stream.
        """
        self.__base_stream_.write(buffer, offset, count)